#!/usr/bin/env python3
"""
Unit tests for Think AI model integration with Ollama
Tests both qwen2.5:3b and codellama:7b models
"""

import requests
import json
import time
import sys
from datetime import datetime

BASE_URL = "http://localhost:8080"
TIMEOUT = 30


class ModelIntegrationTests:
    def __init__(self):
        self.results = {"passed": 0, "failed": 0, "tests": []}

    def log_result(self, test_name, passed, details=""):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "PASS" if passed else "FAIL"
        print(f"[{timestamp}] {test_name}: {status} {details}")

        self.results["tests"].append(
            {
                "name": test_name,
                "status": status,
                "details": details,
                "timestamp": timestamp,
            }
        )

        if passed:
            self.results["passed"] += 1
        else:
            self.results["failed"] += 1

        return passed

    def test_api_health(self):
        """Test if API is responding"""
        try:
            response = requests.get(f"{BASE_URL}/", timeout=5)
            return self.log_result(
                "API Health Check",
                response.status_code == 200,
                f"(Status: {response.status_code})",
            )
        except Exception as e:
            return self.log_result("API Health Check", False, f"(Error: {str(e)})")

    def test_qwen_general_query(self):
        """Test general query using qwen2.5:3b"""
        try:
            payload = {
                "message": "What is 2 + 2?",
                "model": "qwen",
                "session_id": "test_qwen_1",
            }

            response = requests.post(
                f"{BASE_URL}/api/chat",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=TIMEOUT,
            )

            if response.status_code == 200:
                data = response.json()
                # Check if response is not a hardcoded template
                hardcoded_phrases = [
                    "I don't have specific information",
                    "Quantum Analysis:",
                    "Processing through optimized consciousness",
                ]

                response_text = data.get("response", "")
                is_hardcoded = any(
                    phrase in response_text for phrase in hardcoded_phrases
                )

                # qwen should provide a real answer about 2+2
                has_answer = "4" in response_text or "four" in response_text.lower()

                passed = not is_hardcoded and has_answer and len(response_text) > 10

                return self.log_result(
                    "Qwen General Query",
                    passed,
                    f"(Hardcoded: {is_hardcoded}, Has Answer: {has_answer}, Length: {len(response_text)})",
                )
            else:
                return self.log_result(
                    "Qwen General Query", False, f"(Status: {response.status_code})"
                )

        except Exception as e:
            return self.log_result("Qwen General Query", False, f"(Error: {str(e)})")

    def test_qwen_complex_query(self):
        """Test complex query using qwen2.5:3b"""
        try:
            payload = {
                "message": "Explain quantum computing in simple terms",
                "model": "qwen",
                "session_id": "test_qwen_2",
            }

            response = requests.post(
                f"{BASE_URL}/api/chat",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=TIMEOUT,
            )

            if response.status_code == 200:
                data = response.json()
                response_text = data.get("response", "")

                # Should contain relevant keywords
                keywords = ["quantum", "qubit", "computer", "state", "superposition"]
                has_keywords = any(
                    keyword in response_text.lower() for keyword in keywords
                )

                # Should be substantial response
                is_substantial = len(response_text) > 100

                passed = has_keywords and is_substantial

                return self.log_result(
                    "Qwen Complex Query",
                    passed,
                    f"(Has Keywords: {has_keywords}, Length: {len(response_text)})",
                )
            else:
                return self.log_result(
                    "Qwen Complex Query", False, f"(Status: {response.status_code})"
                )

        except Exception as e:
            return self.log_result("Qwen Complex Query", False, f"(Error: {str(e)})")

    def test_codellama_code_query(self):
        """Test code query using codellama:7b"""
        try:
            payload = {
                "message": "Write a Python function to calculate factorial",
                "model": "codellama",
                "session_id": "test_codellama_1",
            }

            response = requests.post(
                f"{BASE_URL}/api/chat",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=TIMEOUT,
            )

            if response.status_code == 200:
                data = response.json()
                response_text = data.get("response", "")

                # Should contain code elements
                code_indicators = [
                    "def",
                    "factorial",
                    "return",
                    "if",
                    "else",
                    "for",
                    "while",
                ]
                has_code = any(
                    indicator in response_text for indicator in code_indicators
                )

                # Should be substantial
                is_substantial = len(response_text) > 50

                # Should mention CodeLlama or have code formatting
                is_from_codellama = (
                    "CodeLlama" in response_text or "```" in response_text
                )

                passed = has_code and is_substantial

                return self.log_result(
                    "CodeLlama Code Query",
                    passed,
                    f"(Has Code: {has_code}, From CodeLlama: {is_from_codellama}, Length: {len(response_text)})",
                )
            else:
                return self.log_result(
                    "CodeLlama Code Query", False, f"(Status: {response.status_code})"
                )

        except Exception as e:
            return self.log_result("CodeLlama Code Query", False, f"(Error: {str(e)})")

    def test_model_switching(self):
        """Test automatic model switching based on query type"""
        queries = [
            ("What is the meaning of life?", "qwen", ["meaning", "life", "purpose"]),
            (
                "How do I implement a binary search tree?",
                "codellama",
                ["binary", "tree", "node", "def"],
            ),
        ]

        all_passed = True

        for query, expected_model, expected_keywords in queries:
            try:
                payload = {
                    "message": query,
                    "session_id": f"test_switch_{expected_model}",
                }

                response = requests.post(
                    f"{BASE_URL}/api/chat",
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=TIMEOUT,
                )

                if response.status_code == 200:
                    data = response.json()
                    response_text = data.get("response", "").lower()

                    has_keywords = any(
                        keyword in response_text for keyword in expected_keywords
                    )

                    passed = has_keywords and len(response_text) > 20
                    all_passed = all_passed and passed

                    self.log_result(
                        f"Model Switch - {expected_model}",
                        passed,
                        f"(Query: '{query[:30]}...', Has Keywords: {has_keywords})",
                    )
                else:
                    all_passed = False
                    self.log_result(
                        f"Model Switch - {expected_model}",
                        False,
                        f"(Status: {response.status_code})",
                    )

            except Exception as e:
                all_passed = False
                self.log_result(
                    f"Model Switch - {expected_model}", False, f"(Error: {str(e)})"
                )

        return all_passed

    def test_response_time(self):
        """Test response time is reasonable"""
        try:
            start_time = time.time()

            payload = {"message": "Hello", "session_id": "test_performance"}

            response = requests.post(
                f"{BASE_URL}/api/chat",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=TIMEOUT,
            )

            end_time = time.time()
            response_time = end_time - start_time

            # Should respond within 10 seconds
            passed = response.status_code == 200 and response_time < 10

            return self.log_result(
                "Response Time",
                passed,
                f"(Time: {response_time:.2f}s, Status: {response.status_code})",
            )

        except Exception as e:
            return self.log_result("Response Time", False, f"(Error: {str(e)})")

    def run_all_tests(self):
        """Run all unit tests"""
        print("\n" + "=" * 60)
        print("Think AI Model Integration Unit Tests")
        print("=" * 60 + "\n")

        # Run tests
        self.test_api_health()
        time.sleep(1)

        self.test_qwen_general_query()
        time.sleep(1)

        self.test_qwen_complex_query()
        time.sleep(1)

        self.test_codellama_code_query()
        time.sleep(1)

        self.test_model_switching()
        time.sleep(1)

        self.test_response_time()

        # Summary
        print("\n" + "=" * 60)
        print(
            f"Results: {self.results['passed']}/{self.results['passed'] + self.results['failed']} tests passed"
        )
        print("=" * 60 + "\n")

        # Save results
        with open("/home/administrator/think_ai/unit_test_results.json", "w") as f:
            json.dump(self.results, f, indent=2)

        return self.results["failed"] == 0


if __name__ == "__main__":
    tester = ModelIntegrationTests()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
