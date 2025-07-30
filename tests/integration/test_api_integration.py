import asyncio
import aiohttp
import pytest
import json
import time
from typing import Dict, Any, List
import os
from concurrent.futures import ThreadPoolExecutor
import statistics

class ThinkAITestClient:
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv("THINK_AI_API_URL", "http://localhost:3000")
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
    
    async def chat(self, message: str, session_id: str = None, **kwargs) -> Dict[str, Any]:
        """Send a chat message to the API"""
        payload = {
            "message": message,
            "session_id": session_id,
            **kwargs
        }
        
        async with self.session.post(
            f"{self.base_url}/api/chat",
            json=payload
        ) as response:
            return await response.json(), response.status

    async def health_check(self) -> bool:
        """Check if the API is healthy"""
        try:
            async with self.session.get(f"{self.base_url}/health") as response:
                return response.status == 200
        except:
            return False

    async def get_metrics(self) -> Dict[str, Any]:
        """Get system metrics"""
        async with self.session.get(f"{self.base_url}/metrics") as response:
            return await response.json()


@pytest.mark.asyncio
class TestAPIIntegration:
    
    async def test_basic_chat_flow(self):
        """Test basic chat functionality"""
        async with ThinkAITestClient() as client:
            # First message
            response, status = await client.chat("Hello, I'm testing the API")
            assert status == 200
            assert "response" in response
            assert "session_id" in response
            assert len(response["response"]) > 0
            
            session_id = response["session_id"]
            
            # Follow-up message
            response2, status2 = await client.chat(
                "Do you remember what I just said?",
                session_id=session_id
            )
            assert status2 == 200
            assert response2["session_id"] == session_id

    async def test_session_isolation(self):
        """Test that sessions are properly isolated"""
        async with ThinkAITestClient() as client:
            # Create two sessions with different contexts
            response1, _ = await client.chat("My favorite color is blue", session_id="session1")
            response2, _ = await client.chat("My favorite color is red", session_id="session2")
            
            # Query each session
            check1, _ = await client.chat("What's my favorite color?", session_id="session1")
            check2, _ = await client.chat("What's my favorite color?", session_id="session2")
            
            # Verify responses mention the correct colors
            assert "blue" in check1["response"].lower()
            assert "red" in check2["response"].lower()

    async def test_concurrent_requests(self):
        """Test handling of concurrent requests"""
        async with ThinkAITestClient() as client:
            tasks = []
            
            # Create 20 concurrent requests
            for i in range(20):
                task = client.chat(
                    f"Concurrent request {i}",
                    session_id=f"concurrent-{i}"
                )
                tasks.append(task)
            
            # Execute all requests concurrently
            start_time = time.time()
            results = await asyncio.gather(*tasks)
            end_time = time.time()
            
            # Verify all requests succeeded
            for response, status in results:
                assert status == 200
                assert "response" in response
            
            # Verify reasonable performance (should handle concurrent requests efficiently)
            total_time = end_time - start_time
            assert total_time < 10  # Should complete within 10 seconds

    async def test_error_handling(self):
        """Test API error handling"""
        async with ThinkAITestClient() as client:
            # Test empty message
            response, status = await client.chat("")
            assert status == 400
            
            # Test malicious input
            response, status = await client.chat("<script>alert('xss')</script>")
            assert status == 400
            
            # Test SQL injection attempt
            response, status = await client.chat("'; DROP TABLE users; --")
            assert status == 400

    async def test_response_consistency(self):
        """Test that responses are consistent within a session"""
        async with ThinkAITestClient() as client:
            session_id = "consistency-test"
            
            # Establish context
            await client.chat("My name is Bob and I'm a software engineer", session_id=session_id)
            
            # Ask multiple times about the established context
            responses = []
            for _ in range(5):
                response, _ = await client.chat("What's my profession?", session_id=session_id)
                responses.append(response["response"])
            
            # All responses should mention software engineering
            for response in responses:
                assert any(word in response.lower() for word in ["software", "engineer", "programming", "developer"])

    async def test_performance_metrics(self):
        """Test response time metrics"""
        async with ThinkAITestClient() as client:
            response_times = []
            
            # Make 10 requests and measure response times
            for i in range(10):
                start = time.time()
                response, status = await client.chat(f"Test message {i}")
                end = time.time()
                
                assert status == 200
                response_times.append((end - start) * 1000)  # Convert to ms
                
                # Verify response includes timing information
                assert "response_time_ms" in response
            
            # Calculate statistics
            avg_time = statistics.mean(response_times)
            p95_time = statistics.quantiles(response_times, n=20)[18]  # 95th percentile
            
            # Verify reasonable performance
            assert avg_time < 1000  # Average under 1 second
            assert p95_time < 2000  # 95th percentile under 2 seconds

    async def test_mode_switching(self):
        """Test different conversation modes"""
        async with ThinkAITestClient() as client:
            # Test code mode
            response, status = await client.chat(
                "Write a Python function to reverse a string",
                mode="code"
            )
            assert status == 200
            assert "def" in response["response"] or "function" in response["response"]
            
            # Test general mode
            response, status = await client.chat(
                "What is the capital of France?",
                mode="general"
            )
            assert status == 200
            assert "paris" in response["response"].lower()

    async def test_web_search_feature(self):
        """Test web search integration"""
        async with ThinkAITestClient() as client:
            response, status = await client.chat(
                "What's the current weather?",
                use_web_search=True
            )
            assert status == 200
            # Response should indicate it would search for current information
            assert len(response["response"]) > 0

    async def test_large_context_handling(self):
        """Test handling of large conversation contexts"""
        async with ThinkAITestClient() as client:
            session_id = "large-context-test"
            
            # Build up a large context
            for i in range(15):
                await client.chat(
                    f"This is message {i}. " + "x" * 100,  # Moderately long messages
                    session_id=session_id
                )
            
            # Verify system still responds appropriately
            response, status = await client.chat(
                "Can you summarize our conversation?",
                session_id=session_id
            )
            assert status == 200
            assert len(response["response"]) > 0
            assert "compacted" in response  # Should indicate if context was compacted


# Helper function to run tests
async def run_integration_tests():
    """Run all integration tests and report results"""
    test_client = TestAPIIntegration()
    
    tests = [
        ("Basic Chat Flow", test_client.test_basic_chat_flow),
        ("Session Isolation", test_client.test_session_isolation),
        ("Concurrent Requests", test_client.test_concurrent_requests),
        ("Error Handling", test_client.test_error_handling),
        ("Response Consistency", test_client.test_response_consistency),
        ("Performance Metrics", test_client.test_performance_metrics),
        ("Mode Switching", test_client.test_mode_switching),
        ("Web Search Feature", test_client.test_web_search_feature),
        ("Large Context Handling", test_client.test_large_context_handling),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            await test_func()
            results.append((test_name, "PASSED", None))
            print(f"✅ {test_name}: PASSED")
        except Exception as e:
            results.append((test_name, "FAILED", str(e)))
            print(f"❌ {test_name}: FAILED - {str(e)}")
    
    return results


if __name__ == "__main__":
    # Run tests
    asyncio.run(run_integration_tests())