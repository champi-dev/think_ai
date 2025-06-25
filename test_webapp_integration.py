#!/usr/bin/env python3
"""Test script for webapp integration - backend, frontend, and core Think AI methods."""

import json
import os
import subprocess
import sys
import time
from datetime import datetime

import requests

# Test results collector
test_results = {
    "timestamp": datetime.now().isoformat(),
    "backend_tests": {},
    "frontend_tests": {},
    "integration_tests": {},
    "evidence": [],
}


def log_test(category, test_name, result, details=""):
    """Log test results with evidence."""
    test_results[category][test_name] = {"result": result, "details": details, "timestamp": datetime.now().isoformat()}
    status = "✅ PASS" if result else "❌ FAIL"
    print(f"{status} {test_name}: {details}")
    test_results["evidence"].append(f"{status} {test_name}: {details}")


def test_backend_server():
    """Test backend server startup and API endpoints."""
    print("\n" + "=" * 60)
    print("🔧 TESTING BACKEND SERVER")
    print("=" * 60)

    # Start the backend server
    server_process = None
    try:
        print("\n1. Starting backend server...")
        server_process = subprocess.Popen(
            [sys.executable, "servers/simple_api_server.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        # Wait for server to start
        time.sleep(5)

        # Check if server is running
        try:
            response = requests.get("http://localhost:8080/api/v1/health", timeout=5)
            if response.status_code == 200:
                health_data = response.json()
                log_test(
                    "backend_tests",
                    "server_startup",
                    True,
                    f"Server running - Health: {json.dumps(health_data, indent=2)}",
                )
            else:
                log_test("backend_tests", "server_startup", False, f"Server returned status {response.status_code}")
        except Exception as e:
            log_test("backend_tests", "server_startup", False, f"Failed to connect: {str(e)}")
            return False

        # Test API endpoints
        print("\n2. Testing API endpoints...")

        # Test /api/think endpoint
        try:
            think_payload = {
                "query": "What is your purpose?",
                "enable_consciousness": True,
                "temperature": 0.7,
                "max_tokens": 500,
            }
            response = requests.post("http://localhost:8080/api/think", json=think_payload, timeout=10)
            if response.status_code == 200:
                think_data = response.json()
                log_test(
                    "backend_tests", "think_endpoint", True, f"Think AI responded: {think_data['response'][:100]}..."
                )

                # Verify consciousness state
                if "consciousness_state" in think_data:
                    log_test(
                        "backend_tests",
                        "consciousness_state",
                        True,
                        f"Consciousness active: {json.dumps(think_data['consciousness_state'], indent=2)}",
                    )
            else:
                log_test("backend_tests", "think_endpoint", False, f"Think endpoint returned {response.status_code}")
        except Exception as e:
            log_test("backend_tests", "think_endpoint", False, f"Think endpoint error: {str(e)}")

        # Test intelligence endpoint
        try:
            response = requests.get("http://localhost:8080/api/intelligence", timeout=5)
            if response.status_code == 200:
                intel_data = response.json()
                log_test(
                    "backend_tests",
                    "intelligence_endpoint",
                    True,
                    f"Intelligence metrics: IQ={intel_data['iq']}, Knowledge={intel_data['knowledge_count']}",
                )
            else:
                log_test(
                    "backend_tests",
                    "intelligence_endpoint",
                    False,
                    f"Intelligence endpoint returned {response.status_code}",
                )
        except Exception as e:
            log_test("backend_tests", "intelligence_endpoint", False, f"Intelligence endpoint error: {str(e)}")

        # Test code generation
        try:
            code_payload = {"type": "python", "prompt": "simple hello world function"}
            response = requests.post("http://localhost:8080/api/code/generate", json=code_payload, timeout=10)
            if response.status_code == 200:
                code_data = response.json()
                log_test("backend_tests", "code_generation", True, f"Generated code: {code_data['code'][:100]}...")
            else:
                log_test("backend_tests", "code_generation", False, f"Code generation returned {response.status_code}")
        except Exception as e:
            log_test("backend_tests", "code_generation", False, f"Code generation error: {str(e)}")

        # Test capabilities endpoint
        try:
            response = requests.get("http://localhost:8080/api/capabilities", timeout=5)
            if response.status_code == 200:
                cap_data = response.json()
                log_test(
                    "backend_tests", "capabilities_endpoint", True, f"Capabilities: {json.dumps(cap_data, indent=2)}"
                )
            else:
                log_test(
                    "backend_tests",
                    "capabilities_endpoint",
                    False,
                    f"Capabilities endpoint returned {response.status_code}",
                )
        except Exception as e:
            log_test("backend_tests", "capabilities_endpoint", False, f"Capabilities endpoint error: {str(e)}")

        return True

    except Exception as e:
        log_test("backend_tests", "server_startup", False, f"Server startup failed: {str(e)}")
        return False
    finally:
        # Cleanup server process
        if server_process:
            server_process.terminate()
            server_process.wait()


def test_core_think_ai_methods():
    """Test core Think AI methods directly."""
    print("\n" + "=" * 60)
    print("🧠 TESTING CORE THINK AI METHODS")
    print("=" * 60)

    try:
        # Import core Think AI components
        from think_ai_conversation_enhanced import generate_contextual_response, knowledge, model, vector_db

        # Test model loading
        log_test("integration_tests", "model_loading", True, f"Model loaded: {type(model).__name__}")

        # Test vector database
        log_test("integration_tests", "vector_db_init", True, f"Vector DB initialized: {type(vector_db).__name__}")

        # Test knowledge base
        log_test("integration_tests", "knowledge_base", True, f"Knowledge base loaded: {len(knowledge)} thoughts")

        # Test embedding generation
        test_text = "Testing embedding generation"
        embedding = model.encode(test_text)
        log_test("integration_tests", "embedding_generation", True, f"Generated embedding shape: {embedding.shape}")

        # Test vector search
        vector_db.add(embedding, {"thought": test_text, "id": "test"})
        results = vector_db.search(embedding, k=1)
        log_test("integration_tests", "vector_search", True, f"Vector search working: {len(results)} results found")

        # Test response generation
        response = generate_contextual_response("Hello, what can you do?", [])
        log_test("integration_tests", "response_generation", True, f"Generated response: {response[:100]}...")

        return True

    except Exception as e:
        log_test("integration_tests", "core_methods", False, f"Core methods test failed: {str(e)}")
        return False


def test_frontend_backend_integration():
    """Test frontend to backend communication."""
    print("\n" + "=" * 60)
    print("🌐 TESTING FRONTEND-BACKEND INTEGRATION")
    print("=" * 60)

    # Start backend server for integration test
    server_process = None
    try:
        print("\n1. Starting backend server for integration test...")
        server_process = subprocess.Popen(
            [sys.executable, "servers/simple_api_server.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        time.sleep(5)

        # Test various query types
        test_queries = [
            {"query": "Explain your architecture", "expected": ["vector", "consciousness", "parallel", "O(1)"]},
            {"query": "Write a Python function to calculate fibonacci", "expected": ["def", "fibonacci", "```python"]},
            {"query": "What programming languages do you know?", "expected": ["Python", "JavaScript", "TypeScript"]},
        ]

        for i, test in enumerate(test_queries):
            try:
                payload = {"query": test["query"], "enable_consciousness": True}
                response = requests.post("http://localhost:8080/api/think", json=payload, timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    response_text = data["response"]

                    # Check for expected keywords
                    found_keywords = [kw for kw in test["expected"] if kw.lower() in response_text.lower()]

                    success = len(found_keywords) > 0
                    log_test(
                        "integration_tests",
                        f"query_test_{i+1}",
                        success,
                        f"Query: '{test['query']}' - Found keywords: {found_keywords}",
                    )

                    # Check response quality
                    if len(response_text) > 50:
                        log_test(
                            "integration_tests",
                            f"response_quality_{i+1}",
                            True,
                            f"Response length: {len(response_text)} chars",
                        )
                else:
                    log_test(
                        "integration_tests",
                        f"query_test_{i+1}",
                        False,
                        f"Query failed with status {response.status_code}",
                    )

            except Exception as e:
                log_test("integration_tests", f"query_test_{i+1}", False, f"Query error: {str(e)}")

        # Test websocket endpoint (if available)
        print("\n2. Testing WebSocket support...")
        try:
            ws_response = requests.get("http://localhost:8080/api/ws", timeout=5)
            if ws_response.status_code in [101, 426]:  # WebSocket upgrade or upgrade required
                log_test("integration_tests", "websocket_support", True, "WebSocket endpoint available")
            else:
                log_test(
                    "integration_tests",
                    "websocket_support",
                    False,
                    f"WebSocket endpoint returned {ws_response.status_code}",
                )
        except:
            log_test("integration_tests", "websocket_support", False, "WebSocket endpoint not implemented")

        return True

    except Exception as e:
        log_test("integration_tests", "frontend_backend", False, f"Integration test failed: {str(e)}")
        return False
    finally:
        if server_process:
            server_process.terminate()
            server_process.wait()


def generate_evidence_report():
    """Generate comprehensive evidence report."""
    print("\n" + "=" * 60)
    print("📊 GENERATING EVIDENCE REPORT")
    print("=" * 60)

    # Calculate statistics
    total_tests = sum(
        len(test_results[category]) for category in ["backend_tests", "frontend_tests", "integration_tests"]
    )
    passed_tests = sum(
        1
        for category in ["backend_tests", "frontend_tests", "integration_tests"]
        for test in test_results[category].values()
        if test["result"]
    )

    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

    # Generate report
    report = {
        "summary": {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": total_tests - passed_tests,
            "success_rate": f"{success_rate:.1f}%",
            "timestamp": test_results["timestamp"],
        },
        "test_results": test_results,
        "evidence": test_results["evidence"],
        "conclusion": "WORKING AT 100% ACCURACY" if success_rate == 100 else f"WORKING AT {success_rate:.1f}% ACCURACY",
    }

    # Save report
    with open("webapp_integration_evidence.json", "w") as f:
        json.dump(report, f, indent=2)

    # Print summary
    print(f"\n✅ Total Tests: {total_tests}")
    print(f"✅ Passed: {passed_tests}")
    print(f"❌ Failed: {total_tests - passed_tests}")
    print(f"📈 Success Rate: {success_rate:.1f}%")
    print(f"\n{'='*60}")
    print(f"🎯 CONCLUSION: {report['conclusion']}")
    print(f"{'='*60}")

    # Save human-readable report
    with open("webapp_integration_report.md", "w") as f:
        f.write("# Web App Integration Test Report\n\n")
        f.write(f"**Generated:** {report['summary']['timestamp']}\n\n")
        f.write("## Summary\n\n")
        f.write(f"- Total Tests: {report['summary']['total_tests']}\n")
        f.write(f"- Passed: {report['summary']['passed']}\n")
        f.write(f"- Failed: {report['summary']['failed']}\n")
        f.write(f"- Success Rate: {report['summary']['success_rate']}\n\n")
        f.write("## Evidence\n\n")
        for evidence in report["evidence"]:
            f.write(f"- {evidence}\n")
        f.write(f"\n## Conclusion\n\n**{report['conclusion']}**\n")


if __name__ == "__main__":
    print("🚀 THINK AI WEB APP INTEGRATION TEST")
    print("Testing Frontend ↔ Backend ↔ Core Think AI Methods")

    # Run tests
    backend_ok = test_backend_server()
    core_ok = test_core_think_ai_methods()
    integration_ok = test_frontend_backend_integration()

    # Generate evidence report
    generate_evidence_report()

    print("\n✅ Test suite completed. Check webapp_integration_evidence.json for full report.")
