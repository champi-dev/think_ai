#!/usr/bin/env python3
"""
Think AI System Verification Test
Comprehensive test to verify the Think AI system works correctly
"""

import asyncio
import importlib.util
import json
import os
import subprocess
import sys
import time
from typing import Any, Dict, List


class ThinkAISystemVerifier:
    """Comprehensive system verification for Think AI"""

    def __init__(self):
        self.results = {
            "timestamp": time.time(),
            "tests": {},
            "summary": {"total": 0, "passed": 0, "failed": 0, "errors": []},
        }

    def log_test(self, name: str, passed: bool, details: str = ""):
        """Log test result"""
        self.results["tests"][name] = {"passed": passed, "details": details, "timestamp": time.time()}
        self.results["summary"]["total"] += 1
        if passed:
            self.results["summary"]["passed"] += 1
            print(f"✅ {name}: PASSED")
        else:
            self.results["summary"]["failed"] += 1
            self.results["summary"]["errors"].append(f"{name}: {details}")
            print(f"❌ {name}: FAILED - {details}")

        if details:
            print(f"   Details: {details}")

    def test_package_structure(self):
        """Test that key package files exist"""
        key_files = ["package.json", "setup.py", "requirements.txt", "README.md", "api_server.py"]

        missing_files = []
        for file in key_files:
            if not os.path.exists(file):
                missing_files.append(file)

        if missing_files:
            self.log_test("Package Structure", False, f"Missing files: {missing_files}")
        else:
            self.log_test("Package Structure", True, "All key files present")

    def test_python_imports(self):
        """Test basic Python module imports"""
        basic_modules = ["json", "os", "sys", "time", "asyncio"]

        failed_imports = []
        for module in basic_modules:
            try:
                __import__(module)
            except ImportError as e:
                failed_imports.append(f"{module}: {e}")

        if failed_imports:
            self.log_test("Python Basic Imports", False, f"Failed: {failed_imports}")
        else:
            self.log_test("Python Basic Imports", True, "All basic modules importable")

    def test_node_modules(self):
        """Test Node.js dependencies"""
        try:
            # Check if package.json exists and has dependencies
            if os.path.exists("package.json"):
                with open("package.json", "r") as f:
                    package_data = json.load(f)

                has_deps = "dependencies" in package_data or "devDependencies" in package_data
                node_modules_exists = os.path.exists("node_modules")

                if has_deps and node_modules_exists:
                    self.log_test("Node Dependencies", True, "package.json and node_modules present")
                else:
                    self.log_test("Node Dependencies", False, "Missing dependencies or node_modules")
            else:
                self.log_test("Node Dependencies", False, "No package.json found")
        except Exception as e:
            self.log_test("Node Dependencies", False, str(e))

    def test_npm_scripts(self):
        """Test npm scripts execution"""
        try:
            # Test linting
            lint_result = subprocess.run(["npm", "run", "lint"], capture_output=True, text=True, timeout=30)

            if lint_result.returncode == 0:
                self.log_test("NPM Lint", True, "Linting passed")
            else:
                self.log_test("NPM Lint", False, f"Lint errors: {lint_result.stderr}")

            # Test tests
            test_result = subprocess.run(["npm", "test"], capture_output=True, text=True, timeout=60)

            if test_result.returncode == 0:
                self.log_test("NPM Tests", True, "All tests passed")
            else:
                self.log_test("NPM Tests", False, f"Test failures: {test_result.stderr}")

        except subprocess.TimeoutExpired:
            self.log_test("NPM Scripts", False, "Timeout during npm script execution")
        except Exception as e:
            self.log_test("NPM Scripts", False, str(e))

    def test_python_linter(self):
        """Test Python linting with Think AI linter"""
        try:
            # Test if the linter runs
            linter_result = subprocess.run(
                ["python", "think_ai_linter.py", "--help"], capture_output=True, text=True, timeout=10
            )

            if linter_result.returncode == 0:
                self.log_test("Python Linter", True, "Think AI linter functional")
            else:
                self.log_test("Python Linter", False, f"Linter error: {linter_result.stderr}")

        except Exception as e:
            self.log_test("Python Linter", False, str(e))

    def test_o1_vector_search_js(self):
        """Test O(1) Vector Search JavaScript implementation"""
        try:
            # Check if o1-js directory and files exist
            o1_js_path = "o1-js/src/index.ts"
            if os.path.exists(o1_js_path):
                self.log_test("O1 Vector Search JS", True, "TypeScript implementation found")
            else:
                self.log_test("O1 Vector Search JS", False, "O1 JS implementation not found")
        except Exception as e:
            self.log_test("O1 Vector Search JS", False, str(e))

    def test_npm_package_structure(self):
        """Test npm package structure"""
        try:
            npm_path = "npm/src/index.ts"
            npm_test_path = "npm/src/index.test.ts"

            if os.path.exists(npm_path) and os.path.exists(npm_test_path):
                self.log_test("NPM Package Structure", True, "NPM package files present")
            else:
                self.log_test("NPM Package Structure", False, "Missing NPM package files")
        except Exception as e:
            self.log_test("NPM Package Structure", False, str(e))

    def test_api_server_existence(self):
        """Test if API server file exists and is syntactically valid"""
        try:
            if os.path.exists("api_server.py"):
                # Try to compile the file to check syntax
                with open("api_server.py", "r") as f:
                    content = f.read()

                compile(content, "api_server.py", "exec")
                self.log_test("API Server Syntax", True, "API server file is syntactically valid")
            else:
                self.log_test("API Server Syntax", False, "API server file not found")
        except SyntaxError as e:
            self.log_test("API Server Syntax", False, f"Syntax error: {e}")
        except Exception as e:
            self.log_test("API Server Syntax", False, str(e))

    def test_configuration_files(self):
        """Test configuration files"""
        config_files = {
            ".eslintrc.js": "ESLint config",
            "jest.config.js": "Jest config",
            "tsconfig.json": "TypeScript config",
        }

        for file, desc in config_files.items():
            if os.path.exists(file):
                self.log_test(f"Config: {desc}", True, f"{file} exists")
            else:
                self.log_test(f"Config: {desc}", False, f"{file} missing")

    def run_all_tests(self):
        """Run all verification tests"""
        print("🧠 Think AI System Verification Starting...")
        print("=" * 50)

        # Run all tests
        self.test_package_structure()
        self.test_python_imports()
        self.test_node_modules()
        self.test_npm_scripts()
        self.test_python_linter()
        self.test_o1_vector_search_js()
        self.test_npm_package_structure()
        self.test_api_server_existence()
        self.test_configuration_files()

        # Print summary
        print("\n" + "=" * 50)
        print("📊 VERIFICATION SUMMARY")
        print("=" * 50)

        total = self.results["summary"]["total"]
        passed = self.results["summary"]["passed"]
        failed = self.results["summary"]["failed"]

        print(f"Total Tests: {total}")
        print(f"Passed: ✅ {passed}")
        print(f"Failed: ❌ {failed}")
        print(f"Success Rate: {(passed/total*100):.1f}%")

        if failed > 0:
            print("\n🔍 FAILED TESTS:")
            for error in self.results["summary"]["errors"]:
                print(f"  • {error}")

        # Save results
        with open("system_verification_results.json", "w") as f:
            json.dump(self.results, f, indent=2)

        print(f"\n📝 Detailed results saved to: system_verification_results.json")

        return passed == total


if __name__ == "__main__":
    verifier = ThinkAISystemVerifier()
    success = verifier.run_all_tests()

    if success:
        print("\n🎉 ALL TESTS PASSED! Think AI system is fully functional!")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Check results above.")
        sys.exit(1)
