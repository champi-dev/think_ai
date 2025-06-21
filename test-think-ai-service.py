#!/usr/bin/env python3
"""
Test Think AI Service Running on http://0.0.0.0:8080
Comprehensive testing of all endpoints and functionality
"""

import json
import time
from datetime import datetime

import requests

# Base URL for Think AI service
BASE_URL = "http://localhost:8080"


class ThinkAITester:
    def __init__(self):
        self.results = []
        self.start_time = time.time()

    def test_endpoint(self, name, method, path, data=None, headers=None):
        """Test a single endpoint"""
        url = f"{BASE_URL}{path}"
        print(f"\n🔍 Testing: {name}")
        print(f"   {method} {url}")

        try:
            if method == "GET":
                response = requests.get(url, headers=headers, timeout=10)
            elif method == "POST":
                response = requests.post(url, json=data, headers=headers, timeout=30)
            else:
                response = requests.request(method, url, json=data, headers=headers, timeout=10)

            # Record result
            result = {
                "name": name,
                "endpoint": f"{method} {path}",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "success": 200 <= response.status_code < 300,
            }

            # Print response
            print(f"   Status: {response.status_code}")
            print(f"   Time: {response.elapsed.total_seconds():.3f}s")

            if response.status_code == 200:
                try:
                    data = response.json()
                    result["response"] = data
                    print(f"   Response: {json.dumps(data, indent=2)[:200]}...")
                except:
                    result["response"] = response.text[:200]
                    print(f"   Response: {response.text[:200]}...")

                print(f"   ✅ SUCCESS")
            else:
                print(f"   ❌ FAILED: {response.text[:200]}")
                result["error"] = response.text[:200]

            self.results.append(result)
            return response

        except requests.exceptions.ConnectionError:
            print(f"   ❌ Connection refused - is the service running?")
            self.results.append(
                {
                    "name": name,
                    "endpoint": f"{method} {path}",
                    "status_code": 0,
                    "success": False,
                    "error": "Connection refused",
                }
            )
            return None
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            self.results.append(
                {"name": name, "endpoint": f"{method} {path}", "status_code": 0, "success": False, "error": str(e)}
            )
            return None

    def run_tests(self):
        """Run all tests"""
        print("🚀 Think AI Service Test Suite")
        print("=" * 50)
        print(f"Testing: {BASE_URL}")
        print(f"Started: {datetime.now()}")
        print("=" * 50)

        # 1. Health check
        self.test_endpoint("Health Check", "GET", "/health")
        self.test_endpoint("Root Endpoint", "GET", "/")

        # 2. API Info
        self.test_endpoint("API Info", "GET", "/api")
        self.test_endpoint("API Version", "GET", "/api/v1")

        # 3. Vector Search
        self.test_endpoint("Vector Search", "POST", "/api/v1/search", data={"query": "What is consciousness?", "k": 3})

        # 4. Generate Response
        self.test_endpoint(
            "Generate Response",
            "POST",
            "/api/v1/generate",
            data={"prompt": "Explain O(1) complexity", "max_tokens": 100},
        )

        # 5. Chat Endpoint
        self.test_endpoint(
            "Chat", "POST", "/api/v1/chat", data={"message": "Hello Think AI! How fast is your vector search?"}
        )

        # 6. Embeddings
        self.test_endpoint(
            "Generate Embeddings", "POST", "/api/v1/embeddings", data={"text": "Think AI is a conscious system"}
        )

        # 7. Stats/Metrics
        self.test_endpoint("Statistics", "GET", "/api/v1/stats")
        self.test_endpoint("Metrics", "GET", "/metrics")

        # 8. WebSocket test info
        print("\n🔌 WebSocket Endpoint:")
        print(f"   ws://localhost:8080/ws")
        print("   (Use webapp/test-websocket.js to test)")

        # Generate report
        self.generate_report()

    def generate_report(self):
        """Generate test report"""
        duration = time.time() - self.start_time
        successful = sum(1 for r in self.results if r["success"])
        total = len(self.results)

        print("\n" + "=" * 50)
        print("📊 TEST REPORT")
        print("=" * 50)
        print(f"Total Tests: {total}")
        print(f"Successful: {successful}")
        print(f"Failed: {total - successful}")
        print(f"Success Rate: {successful/total*100:.1f}%")
        print(f"Total Time: {duration:.2f}s")

        # Average response time for successful requests
        response_times = [r["response_time"] for r in self.results if r.get("response_time")]
        if response_times:
            avg_time = sum(response_times) / len(response_times)
            print(f"Avg Response Time: {avg_time:.3f}s")

        # Show failures
        failures = [r for r in self.results if not r["success"]]
        if failures:
            print("\n❌ Failed Tests:")
            for f in failures:
                print(f"  - {f['name']}: {f.get('error', 'Unknown error')}")

        # Save detailed report
        report = {
            "timestamp": datetime.now().isoformat(),
            "base_url": BASE_URL,
            "summary": {
                "total_tests": total,
                "successful": successful,
                "failed": total - successful,
                "success_rate": f"{successful/total*100:.1f}%",
                "duration": duration,
            },
            "results": self.results,
        }

        with open("think-ai-test-results.json", "w") as f:
            json.dump(report, f, indent=2)

        print(f"\nDetailed report saved to: think-ai-test-results.json")

        # Show sample responses
        print("\n📝 Sample Successful Responses:")
        for r in self.results[:3]:
            if r["success"] and "response" in r:
                print(f"\n{r['name']}:")
                if isinstance(r["response"], dict):
                    print(json.dumps(r["response"], indent=2)[:300] + "...")
                else:
                    print(r["response"][:300] + "...")


def test_with_curl():
    """Alternative testing with curl commands"""
    print("\n🔧 Quick curl tests:")
    print("=" * 50)

    curl_commands = [
        ("Health Check", "curl http://localhost:8080/health"),
        ("API Info", "curl http://localhost:8080/api"),
        (
            "Chat Test",
            'curl -X POST http://localhost:8080/api/v1/chat -H "Content-Type: application/json" -d \'{"message":"Hello"}\'',
        ),
    ]

    for name, cmd in curl_commands:
        print(f"\n{name}:")
        print(f"$ {cmd}")


def main():
    tester = ThinkAITester()

    # First check if service is running
    print("🔍 Checking if Think AI service is running...")

    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        print("✅ Service is running!")
    except:
        print("❌ Service not reachable. Please ensure Think AI is running on port 8080")
        print("\nTo start Think AI:")
        print("  python think_ai_full.py")
        print("  # or")
        print("  ./railway_server.py")
        return

    # Run full test suite
    tester.run_tests()

    # Show curl examples
    test_with_curl()


if __name__ == "__main__":
    main()
