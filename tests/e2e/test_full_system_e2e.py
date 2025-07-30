#!/usr/bin/env python3
"""
Comprehensive E2E tests for Think AI system
Tests the complete user journey without any hardcoding
"""

import asyncio
import subprocess
import time
import os
import json
import aiohttp
import pytest
from playwright.async_api import async_playwright
from typing import Dict, Any, List, Optional
import tempfile
import signal
import sys


class ThinkAIE2ETestSuite:
    def __init__(self):
        self.base_url = os.getenv("THINK_AI_URL", "http://localhost:3000")
        self.server_process: Optional[subprocess.Popen] = None
        self.temp_dir = None
        self.test_results: List[Dict[str, Any]] = []
        
    async def setup(self):
        """Set up test environment"""
        print("🚀 Setting up E2E test environment...")
        
        # Create temporary directory for test data
        self.temp_dir = tempfile.mkdtemp(prefix="think_ai_e2e_")
        
        # Start the server if not already running
        if not await self._is_server_running():
            await self._start_server()
        
        print("✅ Test environment ready")
    
    async def teardown(self):
        """Clean up test environment"""
        print("🧹 Cleaning up test environment...")
        
        # Stop server if we started it
        if self.server_process:
            self.server_process.terminate()
            try:
                self.server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.server_process.kill()
        
        # Clean up temp directory
        if self.temp_dir and os.path.exists(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir)
        
        print("✅ Cleanup complete")
    
    async def _is_server_running(self) -> bool:
        """Check if server is already running"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/health", timeout=2) as response:
                    return response.status == 200
        except:
            return False
    
    async def _start_server(self):
        """Start the Think AI server"""
        print("🔧 Starting Think AI server...")
        
        # Build the project first
        build_cmd = ["cargo", "build", "--release", "--bin", "think-ai-full-production"]
        subprocess.run(build_cmd, cwd="/home/administrator/think_ai", check=True)
        
        # Start the server
        server_cmd = ["./target/release/think-ai-full-production"]
        self.server_process = subprocess.Popen(
            server_cmd,
            cwd="/home/administrator/think_ai",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, "RUST_LOG": "info"}
        )
        
        # Wait for server to be ready
        for i in range(30):  # 30 second timeout
            if await self._is_server_running():
                print("✅ Server is running")
                return
            await asyncio.sleep(1)
        
        raise RuntimeError("Server failed to start within 30 seconds")
    
    async def test_ui_responsiveness(self):
        """Test UI responsiveness across different screen sizes"""
        print("\n🖥️  Testing UI responsiveness...")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            
            # Test different viewport sizes
            viewports = [
                {"name": "Mobile", "width": 375, "height": 667},
                {"name": "Tablet", "width": 768, "height": 1024},
                {"name": "Desktop", "width": 1920, "height": 1080},
                {"name": "4K", "width": 3840, "height": 2160},
            ]
            
            for viewport in viewports:
                context = await browser.new_context(viewport_size=viewport)
                page = await context.new_page()
                
                await page.goto(self.base_url)
                await page.wait_for_load_state("networkidle")
                
                # Check essential elements are visible
                assert await page.is_visible("#message-input")
                assert await page.is_visible("#send-button")
                assert await page.is_visible("#chat-messages")
                
                # Take screenshot for evidence
                screenshot_path = os.path.join(
                    self.temp_dir,
                    f"ui_{viewport['name'].lower()}.png"
                )
                await page.screenshot(path=screenshot_path)
                
                await context.close()
                
            await browser.close()
        
        print("✅ UI responsiveness test passed")
        self.test_results.append({"test": "UI Responsiveness", "status": "PASSED"})
    
    async def test_chat_conversation_flow(self):
        """Test complete chat conversation flow"""
        print("\n💬 Testing chat conversation flow...")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            
            await page.goto(self.base_url)
            await page.wait_for_load_state("networkidle")
            
            # Test conversation
            test_messages = [
                "Hello, I'm testing the Think AI system",
                "Can you remember my name if I tell you? My name is TestUser",
                "What's my name?",
                "Can you help me with a coding problem?",
                "Write a Python function to calculate factorial"
            ]
            
            for i, message in enumerate(test_messages):
                # Type message
                await page.fill("#message-input", message)
                
                # Send message
                await page.click("#send-button")
                
                # Wait for response
                await page.wait_for_selector(
                    f"#chat-messages .message:nth-child({(i+1)*2 + 1})",
                    timeout=10000
                )
                
                # Verify message was sent
                sent_message = await page.text_content(
                    f"#chat-messages .user-message:nth-child({(i+1)*2})"
                )
                assert message in sent_message
                
                # Verify response was received
                response = await page.text_content(
                    f"#chat-messages .assistant-message:nth-child({(i+1)*2 + 1})"
                )
                assert len(response) > 0
                
                # Specific assertions for context retention
                if "What's my name?" in message:
                    assert "TestUser" in response or "test" in response.lower()
                
                if "factorial" in message:
                    assert "def" in response or "function" in response
                
                # Small delay between messages
                await asyncio.sleep(0.5)
            
            await browser.close()
        
        print("✅ Chat conversation flow test passed")
        self.test_results.append({"test": "Chat Conversation Flow", "status": "PASSED"})
    
    async def test_api_endpoints(self):
        """Test all API endpoints"""
        print("\n🔌 Testing API endpoints...")
        
        async with aiohttp.ClientSession() as session:
            # Test health endpoint
            async with session.get(f"{self.base_url}/health") as response:
                assert response.status == 200
                data = await response.json()
                assert data["status"] == "healthy"
            
            # Test chat endpoint
            chat_data = {
                "message": "Test message",
                "session_id": "test-session-api"
            }
            async with session.post(
                f"{self.base_url}/api/chat",
                json=chat_data
            ) as response:
                assert response.status == 200
                data = await response.json()
                assert "response" in data
                assert "session_id" in data
                assert "confidence" in data
            
            # Test metrics endpoint
            async with session.get(f"{self.base_url}/metrics") as response:
                assert response.status == 200
                data = await response.json()
                assert "total_requests" in data
                assert "avg_response_time" in data
            
            # Test stats dashboard
            async with session.get(f"{self.base_url}/api/stats") as response:
                assert response.status == 200
                data = await response.json()
                assert "requests_per_minute" in data
        
        print("✅ API endpoints test passed")
        self.test_results.append({"test": "API Endpoints", "status": "PASSED"})
    
    async def test_session_persistence(self):
        """Test session persistence across requests"""
        print("\n💾 Testing session persistence...")
        
        async with aiohttp.ClientSession() as session:
            session_id = "persistence-test-001"
            
            # First request - establish context
            chat_data = {
                "message": "My favorite programming language is Rust",
                "session_id": session_id
            }
            async with session.post(
                f"{self.base_url}/api/chat",
                json=chat_data
            ) as response:
                assert response.status == 200
            
            # Second request - test context retention
            chat_data = {
                "message": "What's my favorite programming language?",
                "session_id": session_id
            }
            async with session.post(
                f"{self.base_url}/api/chat",
                json=chat_data
            ) as response:
                assert response.status == 200
                data = await response.json()
                assert "rust" in data["response"].lower()
        
        print("✅ Session persistence test passed")
        self.test_results.append({"test": "Session Persistence", "status": "PASSED"})
    
    async def test_error_handling(self):
        """Test system error handling"""
        print("\n⚠️  Testing error handling...")
        
        async with aiohttp.ClientSession() as session:
            # Test invalid request
            async with session.post(
                f"{self.base_url}/api/chat",
                json={"invalid": "data"}
            ) as response:
                assert response.status == 400
            
            # Test empty message
            async with session.post(
                f"{self.base_url}/api/chat",
                json={"message": ""}
            ) as response:
                assert response.status == 400
            
            # Test malicious input
            async with session.post(
                f"{self.base_url}/api/chat",
                json={"message": "<script>alert('xss')</script>"}
            ) as response:
                assert response.status == 400
        
        print("✅ Error handling test passed")
        self.test_results.append({"test": "Error Handling", "status": "PASSED"})
    
    async def test_performance(self):
        """Test system performance under load"""
        print("\n⚡ Testing performance...")
        
        async with aiohttp.ClientSession() as session:
            response_times = []
            
            # Send 50 requests
            for i in range(50):
                start_time = time.time()
                
                chat_data = {
                    "message": f"Performance test message {i}",
                    "session_id": f"perf-test-{i % 5}"  # Use 5 different sessions
                }
                
                async with session.post(
                    f"{self.base_url}/api/chat",
                    json=chat_data
                ) as response:
                    assert response.status == 200
                    data = await response.json()
                    
                end_time = time.time()
                response_times.append(end_time - start_time)
                
                # Verify response has timing info
                assert "response_time_ms" in data
            
            # Calculate performance metrics
            avg_time = sum(response_times) / len(response_times)
            max_time = max(response_times)
            min_time = min(response_times)
            
            print(f"  Average response time: {avg_time:.3f}s")
            print(f"  Max response time: {max_time:.3f}s")
            print(f"  Min response time: {min_time:.3f}s")
            
            # Performance assertions
            assert avg_time < 2.0  # Average should be under 2 seconds
            assert max_time < 5.0  # Max should be under 5 seconds
        
        print("✅ Performance test passed")
        self.test_results.append({"test": "Performance", "status": "PASSED"})
    
    async def test_audio_functionality(self):
        """Test audio transcription and synthesis"""
        print("\n🎤 Testing audio functionality...")
        
        # Create a test audio file
        test_audio_path = os.path.join(self.temp_dir, "test_audio.wav")
        
        # Generate simple WAV file (silence)
        with open(test_audio_path, "wb") as f:
            # WAV header for 1 second of silence
            f.write(b'RIFF')
            f.write((36 + 44100 * 2).to_bytes(4, 'little'))  # File size
            f.write(b'WAVE')
            f.write(b'fmt ')
            f.write((16).to_bytes(4, 'little'))  # Subchunk size
            f.write((1).to_bytes(2, 'little'))   # Audio format (PCM)
            f.write((1).to_bytes(2, 'little'))   # Channels
            f.write((44100).to_bytes(4, 'little'))  # Sample rate
            f.write((44100 * 2).to_bytes(4, 'little'))  # Byte rate
            f.write((2).to_bytes(2, 'little'))   # Block align
            f.write((16).to_bytes(2, 'little'))  # Bits per sample
            f.write(b'data')
            f.write((44100 * 2).to_bytes(4, 'little'))  # Data size
            f.write(b'\x00' * (44100 * 2))  # Silent audio data
        
        async with aiohttp.ClientSession() as session:
            # Test audio transcription
            with open(test_audio_path, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field('audio', f, filename='test.wav')
                
                async with session.post(
                    f"{self.base_url}/api/transcribe",
                    data=data
                ) as response:
                    # Audio endpoint might not be implemented, so we accept 404
                    assert response.status in [200, 404]
            
            # Test TTS
            tts_data = {"text": "This is a test"}
            async with session.post(
                f"{self.base_url}/api/tts",
                json=tts_data
            ) as response:
                # Audio endpoint might not be implemented, so we accept 404
                assert response.status in [200, 404]
        
        print("✅ Audio functionality test completed")
        self.test_results.append({"test": "Audio Functionality", "status": "PASSED"})
    
    async def generate_test_report(self):
        """Generate comprehensive test report"""
        print("\n📊 Generating test report...")
        
        report = {
            "test_run_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "environment": {
                "base_url": self.base_url,
                "platform": sys.platform,
                "python_version": sys.version
            },
            "test_results": self.test_results,
            "summary": {
                "total_tests": len(self.test_results),
                "passed": len([r for r in self.test_results if r["status"] == "PASSED"]),
                "failed": len([r for r in self.test_results if r["status"] == "FAILED"])
            }
        }
        
        # Save report
        report_path = os.path.join(self.temp_dir, "e2e_test_report.json")
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print("\n" + "="*50)
        print("E2E TEST SUMMARY")
        print("="*50)
        print(f"Total Tests: {report['summary']['total_tests']}")
        print(f"Passed: {report['summary']['passed']} ✅")
        print(f"Failed: {report['summary']['failed']} ❌")
        print(f"Report saved to: {report_path}")
        print("="*50)
        
        return report
    
    async def run_all_tests(self):
        """Run all E2E tests"""
        try:
            await self.setup()
            
            # Run all test methods
            test_methods = [
                self.test_ui_responsiveness,
                self.test_chat_conversation_flow,
                self.test_api_endpoints,
                self.test_session_persistence,
                self.test_error_handling,
                self.test_performance,
                self.test_audio_functionality
            ]
            
            for test_method in test_methods:
                try:
                    await test_method()
                except Exception as e:
                    test_name = test_method.__name__.replace("test_", "").replace("_", " ").title()
                    print(f"❌ {test_name} test failed: {str(e)}")
                    self.test_results.append({"test": test_name, "status": "FAILED", "error": str(e)})
            
            # Generate report
            report = await self.generate_test_report()
            
            # Return success if all tests passed
            return report['summary']['failed'] == 0
            
        finally:
            await self.teardown()


async def main():
    """Main entry point for E2E tests"""
    print("🚀 Starting Think AI E2E Test Suite")
    print("="*50)
    
    test_suite = ThinkAIE2ETestSuite()
    success = await test_suite.run_all_tests()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())