#!/usr/bin/env python3
"""Automated QA Environment Check - Non-interactive version for CI/CD."""

import subprocess
import sys
import time
import os
from pathlib import Path


def check_qa_environment():
    """Run automated QA checks without manual intervention."""
    print("🧪 THINK AI AUTOMATED QA CHECK")
    print("=" * 50)

    # Run test suite
    print("\n📊 Running test suite...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"], capture_output=True, text=True, timeout=30
        )

        if result.returncode == 0:
            print("✅ All tests passed!")
            test_passed = True
        else:
            print("❌ Some tests failed")
            print(result.stdout[-500:])  # Last 500 chars of output
            test_passed = False
    except subprocess.TimeoutExpired:
        print("⚠️  Test suite timed out after 30 seconds")
        test_passed = False
    except Exception as e:
        print(f"❌ Test suite error: {e}")
        test_passed = False

    # Quick API health check (non-blocking)
    print("\n🔍 Checking API readiness...")
    api_ready = False
    try:
        # Try to import and check if API can be loaded
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import think_ai_minimal

        print("✅ API module loads successfully")
        api_ready = True
    except Exception as e:
        print(f"⚠️  API module load warning: {e}")

    # Check critical files exist
    print("\n📁 Checking critical files...")
    critical_files = [
        "think_ai_minimal.py",
        "think_ai/core/engine.py",
        "think_ai/models/language/language_model.py",
        "railway.json",
        "requirements.txt",
    ]

    files_ok = True
    for file in critical_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} missing!")
            files_ok = False

    # Summary
    print("\n" + "=" * 50)
    all_checks_passed = test_passed and api_ready and files_ok

    if all_checks_passed:
        print("✅ QA CHECKS PASSED - Ready to commit!")
        return 0
    else:
        print("❌ QA CHECKS FAILED - Please fix issues before committing")
        return 1


if __name__ == "__main__":
    sys.exit(check_qa_environment())
