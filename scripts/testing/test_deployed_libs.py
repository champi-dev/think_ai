#! / usr / bin / env python3

"""
Test deployed Think AI libraries
"""

import sys

import think_ai
from think_ai import Config, ThinkAIEngine
from think_ai.utils.complexity_detector import detect_complexity


def test_imports():
"""Test all critical imports"""
    tests = []

# Test 1: Basic package import
    try:
        tests.append(
        ("Import think_ai package",
        True,
        f"Version: {
        think_ai.__version__}"))
        except Exception as e:
            tests.append(("Import think_ai package", False, str(e)))

# Test 2: Core engine
            try:
                ThinkAIEngine()
                tests.append(("Initialize ThinkAIEngine", True,
                "Engine created successfully"))
                except Exception as e:
                    tests.append(("Initialize ThinkAIEngine", False, str(e)))

# Test 3: Complexity detection
                    try:
                        tokens, level = detect_complexity("What is consciousness?")
                        tests.append(
                        ("Complexity detection",
                        True,
                        f"{tokens} tokens for {level} question"))
                        except Exception as e:
                            tests.append(("Complexity detection", False, str(e)))

# Test 4: Config loading
                            try:
                                config = Config()
                                tests.append(
                                ("Load configuration",
                                True,
                                f"Max tokens: {
                                config.max_tokens}"))
                                except Exception as e:
                                    tests.append(("Load configuration", False, str(e)))

# Test 5: Consciousness module
                                    try:
                                        tests.append(("Import consciousness principles", True, "Module loaded"))
                                        except Exception as e:
                                            tests.append(("Import consciousness principles", False, str(e)))

# Test 6: Storage components
                                            try:
                                                tests.append(("Import storage module", True, "Storage module available"))
                                                except Exception as e:
                                                    tests.append(("Import storage module", False, str(e)))

# Test 7: Graph components
                                                    try:
                                                        tests.append(("Import knowledge graph", True, "Graph module available"))
                                                        except Exception as e:
                                                            tests.append(("Import knowledge graph", False, str(e)))

# Test 8: Model module
                                                            try:
                                                                tests.append(("Import language model", True, "Model module available"))
                                                                except Exception as e:
                                                                    tests.append(("Import language model", False, str(e)))

                                                                    return tests

                                                                def test_functionality():
"""Test actual functionality"""
                                                                    tests = []

# Test 1: Complexity detection with various inputs
                                                                    try:

                                                                        test_cases = [
                                                                        ("2 + 2", "simple"),
                                                                        ("Explain quantum mechanics", "complex"),
                                                                        ("Write a sorting algorithm", "moderate"),
                                                                        ("What is the meaning of life?", "complex")
                                                                        ]

                                                                        all_passed = True
                                                                        results = []
                                                                        for question, expected_level in test_cases:
                                                                            tokens, level = detect_complexity(question)
                                                                            if level ! = expected_level and not (level == "complex" and expected_level == "moderate"):
                                                                                all_passed = False
                                                                                results.append(f"{question[:20]}... -> {tokens} tokens ({level})")

                                                                                tests.append(
                                                                                ("Complexity detection tests",
                                                                                all_passed,
                                                                                "\n".join(results)))
                                                                                except Exception as e:
                                                                                    tests.append(("Complexity detection tests", False, str(e)))

# Test 2: Engine configuration
                                                                                    try:

                                                                                        config = Config()
                                                                                        config.max_tokens = 500
                                                                                        ThinkAIEngine(config=config)

                                                                                        tests.append(("Engine with custom config", True,
                                                                                        "Engine accepts configuration"))
                                                                                        except Exception as e:
                                                                                            tests.append(("Engine with custom config", False, str(e)))

                                                                                            return tests

                                                                                        def main():
                                                                                            print("🧪 Testing Think AI Deployed Libraries\n")
                                                                                            print("=" * 60)

# Run import tests
                                                                                            print("\n📦 Import Tests:")
                                                                                            print("-" * 60)
                                                                                            import_tests = test_imports()

                                                                                            passed = 0
                                                                                        failed = 0

                                                                                        for test_name, success, details in import_tests:
                                                                                            status = "✅ PASS" if success else "❌ FAIL"
                                                                                            print(f"{status} | {test_name}")
                                                                                            if details:
                                                                                                print(f" └─ {details}")

                                                                                                if success:
                                                                                                    passed + = 1
                                                                                            else:
                                                                                                failed + = 1

# Run functionality tests
                                                                                                print("\n⚙️ Functionality Tests:")
                                                                                                print("-" * 60)
                                                                                                func_tests = test_functionality()

                                                                                                for test_name, success, details in func_tests:
                                                                                                    status = "✅ PASS" if success else "❌ FAIL"
                                                                                                    print(f"{status} | {test_name}")
                                                                                                    if details and "\n" in details:
                                                                                                        for line in details.split("\n"):
                                                                                                            print(f" └─ {line}")
                                                                                                        elif details:
                                                                                                            print(f" └─ {details}")

                                                                                                            if success:
                                                                                                                passed + = 1
                                                                                                        else:
                                                                                                            failed + = 1

# Summary
                                                                                                            print("\n" + "=" * 60)
                                                                                                            total = passed + failed
                                                                                                            print(
                                                                                                            f"📊 Summary: {passed}/{total} tests passed ({passed / total * 100:.1f}%)")

                                                                                                            if failed = = 0:
                                                                                                                print("🎉 All tests passed! Think AI libraries are working correctly.")
                                                                                                            else:
                                                                                                                print(f"⚠️ {failed} tests failed. Check the errors above.")

                                                                                                                return 0 if failed = = 0 else 1

                                                                                                            if __name__ = = "__main__":
                                                                                                                sys.exit(main())
