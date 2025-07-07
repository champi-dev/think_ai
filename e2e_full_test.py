#!/usr/bin/env python3
"""
Comprehensive E2E Test Suite for Think AI
Tests all major components and functionality
"""

import subprocess
import requests
import json
import time
import sys
from datetime import datetime
import statistics

class ThinkAIE2ETester:
    def __init__(self):
        self.base_url = "http://localhost:8080"
        self.results = {
            "passed": 0,
            "failed": 0,
            "tests": [],
            "performance_metrics": []
        }
        self.server_process = None
        
    def start_server(self):
        """Start the Think AI server"""
        print("🚀 Starting Think AI server...")
        # Kill any existing process on port 8080
        subprocess.run(["lsof", "-ti:8080"], capture_output=True)
        subprocess.run(["pkill", "-f", "think-ai server"], capture_output=True)
        time.sleep(2)
        
        # Start server in background
        self.server_process = subprocess.Popen(
            ["./target/release/think-ai", "server"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        for i in range(30):
            try:
                response = requests.get(f"{self.base_url}/health", timeout=1)
                if response.status_code == 200:
                    print("✅ Server started successfully")
                    return True
            except:
                time.sleep(1)
        
        print("❌ Failed to start server")
        return False
    
    def stop_server(self):
        """Stop the Think AI server"""
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
        subprocess.run(["pkill", "-f", "think-ai server"], capture_output=True)
        print("🛑 Server stopped")
    
    def test_health_endpoint(self):
        """Test the health check endpoint"""
        test_name = "Health Check Endpoint"
        try:
            response = requests.get(f"{self.base_url}/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            self.pass_test(test_name, "Health endpoint working correctly")
        except Exception as e:
            self.fail_test(test_name, str(e))
    
    def test_chat_endpoint(self):
        """Test the chat API endpoint"""
        test_name = "Chat API Endpoint"
        queries = [
            "what is the sun",
            "explain quantum computing",
            "what is love",
            "how does programming work",
            "tell me about the universe"
        ]
        
        try:
            response_times = []
            
            for query in queries:
                start_time = time.time()
                response = requests.post(
                    f"{self.base_url}/chat",
                    json={"message": query},
                    headers={"Content-Type": "application/json"}
                )
                response_time = (time.time() - start_time) * 1000  # ms
                response_times.append(response_time)
                
                assert response.status_code == 200
                data = response.json()
                assert "response" in data
                assert len(data["response"]) > 0
                
                # Check response quality
                self.check_response_quality(query, data["response"])
            
            avg_response_time = statistics.mean(response_times)
            self.performance_metrics["chat_api_avg_ms"] = avg_response_time
            
            self.pass_test(test_name, f"All queries successful. Avg response: {avg_response_time:.2f}ms")
        except Exception as e:
            self.fail_test(test_name, str(e))
    
    def test_knowledge_api(self):
        """Test the knowledge retrieval API"""
        test_name = "Knowledge API Endpoint"
        try:
            response = requests.get(f"{self.base_url}/api/knowledge/stats")
            assert response.status_code == 200
            data = response.json()
            assert "total_nodes" in data
            assert data["total_nodes"] > 0
            self.pass_test(test_name, f"Knowledge base has {data['total_nodes']} nodes")
        except Exception as e:
            self.fail_test(test_name, str(e))
    
    def test_performance_metrics(self):
        """Test O(1) performance claims"""
        test_name = "O(1) Performance Test"
        try:
            # Test with increasing number of queries
            query_counts = [1, 10, 50, 100]
            response_times = []
            
            for count in query_counts:
                total_time = 0
                for i in range(count):
                    start = time.time()
                    response = requests.post(
                        f"{self.base_url}/chat",
                        json={"message": f"test query {i}"},
                        headers={"Content-Type": "application/json"}
                    )
                    total_time += (time.time() - start)
                
                avg_time = (total_time / count) * 1000  # ms
                response_times.append(avg_time)
            
            # Check if response time remains constant (O(1))
            # Allow 20% variance
            variance = max(response_times) / min(response_times)
            is_constant_time = variance < 1.2
            
            self.performance_metrics["response_time_variance"] = variance
            self.performance_metrics["response_times_by_load"] = dict(zip(query_counts, response_times))
            
            if is_constant_time:
                self.pass_test(test_name, f"O(1) performance verified. Variance: {variance:.2f}")
            else:
                self.fail_test(test_name, f"Performance not O(1). Variance: {variance:.2f}")
        except Exception as e:
            self.fail_test(test_name, str(e))
    
    def test_static_files(self):
        """Test static file serving"""
        test_name = "Static File Serving"
        try:
            files = [
                "/static/chat.html",
                "/static/simple_webapp.html"
            ]
            
            for file in files:
                response = requests.get(f"{self.base_url}{file}")
                assert response.status_code == 200
                assert len(response.content) > 0
            
            self.pass_test(test_name, "All static files served correctly")
        except Exception as e:
            self.fail_test(test_name, str(e))
    
    def test_response_quality(self):
        """Test response quality and template detection"""
        test_name = "Response Quality Check"
        
        template_patterns = [
            "Your question about",
            "Regarding your inquiry about",
            "Throughout history",
            "continues to evolve with new discoveries",
            "Practically, this allows",
            "Important features are"
        ]
        
        try:
            test_queries = {
                "what is the sun": "star",
                "what is programming": "code",
                "what is the universe": "space",
                "explain AI": "artificial intelligence"
            }
            
            template_found = False
            quality_issues = []
            
            for query, expected_keyword in test_queries.items():
                response = requests.post(
                    f"{self.base_url}/chat",
                    json={"message": query},
                    headers={"Content-Type": "application/json"}
                )
                
                content = response.json()["response"]
                
                # Check for templates
                for pattern in template_patterns:
                    if pattern in content:
                        template_found = True
                        quality_issues.append(f"Template '{pattern}' found in response to '{query}'")
                
                # Check for expected content
                if expected_keyword.lower() not in content.lower():
                    quality_issues.append(f"Expected keyword '{expected_keyword}' not found for query '{query}'")
            
            if not template_found and len(quality_issues) == 0:
                self.pass_test(test_name, "No template patterns detected, good response quality")
            else:
                self.fail_test(test_name, f"Quality issues: {'; '.join(quality_issues)}")
        except Exception as e:
            self.fail_test(test_name, str(e))
    
    def test_error_handling(self):
        """Test error handling"""
        test_name = "Error Handling"
        try:
            # Test invalid JSON
            response = requests.post(
                f"{self.base_url}/chat",
                data="invalid json",
                headers={"Content-Type": "application/json"}
            )
            assert response.status_code in [400, 500]
            
            # Test missing message
            response = requests.post(
                f"{self.base_url}/chat",
                json={},
                headers={"Content-Type": "application/json"}
            )
            assert response.status_code in [400, 500]
            
            self.pass_test(test_name, "Error handling working correctly")
        except Exception as e:
            self.fail_test(test_name, str(e))
    
    def test_concurrent_requests(self):
        """Test handling of concurrent requests"""
        test_name = "Concurrent Request Handling"
        try:
            import concurrent.futures
            
            def make_request(i):
                return requests.post(
                    f"{self.base_url}/chat",
                    json={"message": f"concurrent test {i}"},
                    headers={"Content-Type": "application/json"}
                )
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                start_time = time.time()
                futures = [executor.submit(make_request, i) for i in range(20)]
                results = [f.result() for f in concurrent.futures.as_completed(futures)]
                total_time = time.time() - start_time
            
            # Check all requests succeeded
            success_count = sum(1 for r in results if r.status_code == 200)
            
            if success_count == 20:
                self.pass_test(test_name, f"All 20 concurrent requests succeeded in {total_time:.2f}s")
            else:
                self.fail_test(test_name, f"Only {success_count}/20 requests succeeded")
        except Exception as e:
            self.fail_test(test_name, str(e))
    
    def check_response_quality(self, query, response):
        """Helper to check response quality"""
        # Add to performance metrics
        if "performance_metrics" not in self.__dict__:
            self.performance_metrics = {}
        
        response_length = len(response)
        if "response_lengths" not in self.performance_metrics:
            self.performance_metrics["response_lengths"] = []
        self.performance_metrics["response_lengths"].append(response_length)
    
    def pass_test(self, name, message):
        """Record a passing test"""
        self.results["passed"] += 1
        self.results["tests"].append({
            "name": name,
            "status": "PASSED",
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        print(f"✅ {name}: {message}")
    
    def fail_test(self, name, message):
        """Record a failing test"""
        self.results["failed"] += 1
        self.results["tests"].append({
            "name": name,
            "status": "FAILED", 
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        print(f"❌ {name}: {message}")
    
    def generate_report(self):
        """Generate test report"""
        print("\n" + "="*60)
        print("Think AI E2E Test Report")
        print("="*60)
        print(f"Total Tests: {self.results['passed'] + self.results['failed']}")
        print(f"Passed: {self.results['passed']}")
        print(f"Failed: {self.results['failed']}")
        print(f"Success Rate: {(self.results['passed'] / (self.results['passed'] + self.results['failed']) * 100):.1f}%")
        
        if hasattr(self, 'performance_metrics'):
            print("\nPerformance Metrics:")
            print("-"*30)
            if "chat_api_avg_ms" in self.performance_metrics:
                print(f"Average Chat Response Time: {self.performance_metrics['chat_api_avg_ms']:.2f}ms")
            if "response_time_variance" in self.performance_metrics:
                print(f"Response Time Variance: {self.performance_metrics['response_time_variance']:.2f}")
            if "response_lengths" in self.performance_metrics:
                avg_length = statistics.mean(self.performance_metrics["response_lengths"])
                print(f"Average Response Length: {avg_length:.0f} characters")
        
        # Save detailed report
        with open("e2e_test_report.json", "w") as f:
            json.dump({
                "summary": self.results,
                "performance": getattr(self, 'performance_metrics', {}),
                "timestamp": datetime.now().isoformat()
            }, f, indent=2)
        
        print(f"\nDetailed report saved to: e2e_test_report.json")
    
    def run_all_tests(self):
        """Run all E2E tests"""
        print("🧪 Starting Think AI E2E Test Suite")
        print("="*60)
        
        if not self.start_server():
            print("❌ Failed to start server, aborting tests")
            return
        
        time.sleep(2)  # Give server time to fully initialize
        
        try:
            # Run all tests
            self.test_health_endpoint()
            self.test_chat_endpoint()
            self.test_knowledge_api()
            self.test_static_files()
            self.test_response_quality()
            self.test_error_handling()
            self.test_performance_metrics()
            self.test_concurrent_requests()
            
        finally:
            self.stop_server()
            self.generate_report()

if __name__ == "__main__":
    tester = ThinkAIE2ETester()
    tester.run_all_tests()