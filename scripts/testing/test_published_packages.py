#!/usr/bin/env python3
"""Test script to verify published packages work correctly"""

import json
import subprocess
import sys
from datetime import datetime


def test_package_install_and_import():
    """Test that published packages can be installed and imported"""

    results = {"test_date": datetime.now().isoformat(), "python_version": sys.version, "tests": {}}

    print("🧪 Testing Published Think AI Packages")
    print("=" * 50)

    # Test 1: Import think-ai-consciousness
    print("\n1. Testing think-ai-consciousness import...")
    try:
        import think_ai

        results["tests"]["import_think_ai"] = {
            "status": "✅ SUCCESS",
            "version": getattr(think_ai, "__version__", "unknown"),
            "package": "think-ai-consciousness",
        }
        print("   ✅ Successfully imported think_ai")
    except Exception as e:
        results["tests"]["import_think_ai"] = {"status": "❌ FAILED", "error": str(e)}
        print(f"   ❌ Failed to import: {e}")

    # Test 2: Import think-ai-cli
    print("\n2. Testing think-ai-cli import...")
    try:
        import think_ai_cli

        results["tests"]["import_think_ai_cli"] = {"status": "✅ SUCCESS", "package": "think-ai-cli"}
        print("   ✅ Successfully imported think_ai_cli")
    except Exception as e:
        results["tests"]["import_think_ai_cli"] = {"status": "❌ FAILED", "error": str(e)}
        print(f"   ❌ Failed to import: {e}")

    # Test 3: Import o1-vector-search
    print("\n3. Testing o1-vector-search import...")
    try:
        import o1_vector_search

        results["tests"]["import_o1_vector_search"] = {
            "status": "✅ SUCCESS",
            "version": getattr(o1_vector_search, "__version__", "1.0.0"),
            "package": "o1-vector-search",
        }
        print("   ✅ Successfully imported o1_vector_search")
    except Exception as e:
        results["tests"]["import_o1_vector_search"] = {"status": "❌ FAILED", "error": str(e)}
        print(f"   ❌ Failed to import: {e}")

    # Test 4: Basic functionality test
    print("\n4. Testing basic Think AI functionality...")
    try:
        from think_ai import ThinkAI

        ai = ThinkAI()

        # Test chat functionality
        response = ai.chat("Say 'Hello, I am Think AI!'")

        results["tests"]["basic_functionality"] = {
            "status": "✅ SUCCESS",
            "test": "chat",
            "response_received": bool(response),
            "response_preview": str(response)[:100] if response else None,
        }
        print("   ✅ Think AI chat functionality works!")
        print(f"   Response: {response[:100]}...")
    except Exception as e:
        results["tests"]["basic_functionality"] = {"status": "❌ FAILED", "error": str(e)}
        print(f"   ❌ Functionality test failed: {e}")

    # Test 5: CLI availability
    print("\n5. Testing CLI command availability...")
    try:
        result = subprocess.run(["think-ai", "--version"], capture_output=True, text=True, timeout=5)

        if result.returncode == 0:
            results["tests"]["cli_availability"] = {"status": "✅ SUCCESS", "output": result.stdout.strip()}
            print("   ✅ CLI command 'think-ai' is available")
            print(f"   Version: {result.stdout.strip()}")
        else:
            results["tests"]["cli_availability"] = {"status": "❌ FAILED", "error": result.stderr}
            print("   ❌ CLI command failed")
    except Exception as e:
        results["tests"]["cli_availability"] = {"status": "❌ FAILED", "error": str(e)}
        print(f"   ❌ CLI test failed: {e}")

    # Test 6: PyPI availability check
    print("\n6. Verifying packages on PyPI...")
    packages = ["think-ai-consciousness", "think-ai-cli", "o1-vector-search"]

    for package in packages:
        try:
            result = subprocess.run(["pip", "show", package], capture_output=True, text=True)

            if result.returncode == 0:
                # Extract version from output
                version_line = [line for line in result.stdout.split("\n") if line.startswith("Version:")]
                version = version_line[0].split(": ")[1] if version_line else "unknown"

                results["tests"][f"pypi_{package}"] = {"status": "✅ SUCCESS", "version": version, "available": True}
                print(f"   ✅ {package} v{version} is available on PyPI")
            else:
                results["tests"][f"pypi_{package}"] = {"status": "❌ NOT FOUND", "available": False}
        except Exception as e:
            results["tests"][f"pypi_{package}"] = {"status": "❌ ERROR", "error": str(e)}

    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)

    total_tests = len(results["tests"])
    passed_tests = sum(1 for test in results["tests"].values() if "SUCCESS" in str(test.get("status", "")))

    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")

    # Save results
    with open("published_packages_test_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n💾 Detailed results saved to: published_packages_test_results.json")

    return results


if __name__ == "__main__":
    # First, ensure we have the latest packages
    print("📦 Installing/updating packages from PyPI...")
    packages_to_install = ["think-ai-consciousness==2.1.0", "think-ai-cli==0.2.0", "o1-vector-search==1.0.0"]

    for package in packages_to_install:
        print(f"Installing {package}...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", package])

    print("\n" + "=" * 50)

    # Run tests
    test_package_install_and_import()
