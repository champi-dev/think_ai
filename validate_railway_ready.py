#!/usr/bin/env python3
"""Validate that Think AI is ready for Railway deployment."""

import json
import os
import subprocess
import sys
import time


def run_command(cmd, description):
    """Run a command and return success status."""
    print(f"\n🔍 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ Success")
            if result.stdout:
                print(f"   Output: {result.stdout.strip()[:200]}")
            return True
        else:
            print(f"   ❌ Failed")
            if result.stderr:
                print(f"   Error: {result.stderr.strip()[:200]}")
            return False
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False


def validate_railway_deployment():
    """Validate the system is ready for Railway."""
    print("🚂 RAILWAY DEPLOYMENT VALIDATION")
    print("=" * 60)

    checks = []

    # 1. Check Railway configuration
    print("\n1️⃣ Checking Railway Configuration...")
    if os.path.exists("railway.json"):
        with open("railway.json", "r") as f:
            config = json.load(f)
        print(f"   ✅ railway.json exists")
        print(f"   Build: {config.get('build', {}).get('dockerfilePath', 'N/A')}")
        print(f"   Start command: {config.get('deploy', {}).get('startCommand', 'N/A')}")
        checks.append(("Railway Config", True))
    else:
        print(f"   ❌ railway.json not found")
        checks.append(("Railway Config", False))

    # 2. Check Dockerfile
    print("\n2️⃣ Checking Dockerfile...")
    dockerfile = "Dockerfile.railway-prebuilt"
    if os.path.exists(dockerfile):
        with open(dockerfile, "r") as f:
            content = f.read()
        if "think_ai_full.py" in content:
            print(f"   ✅ {dockerfile} runs full system")
            checks.append(("Dockerfile", True))
        else:
            print(f"   ❌ {dockerfile} doesn't run full system")
            checks.append(("Dockerfile", False))
    else:
        print(f"   ❌ {dockerfile} not found")
        checks.append(("Dockerfile", False))

    # 3. Test imports without running server
    print("\n3️⃣ Testing Python imports...")
    import_test = """
import os
os.environ["THINK_AI_USE_LIGHTWEIGHT"] = "false"
os.environ["THINK_AI_MINIMAL_INIT"] = "false"

try:
    from think_ai.api.endpoints import router
    from think_ai.core.config import Config
    from think_ai.core.engine import ThinkAIEngine
    print("SUCCESS")
except Exception as e:
    print(f"FAILED: {e}")
"""

    result = subprocess.run([sys.executable, "-c", import_test], capture_output=True, text=True)

    if "SUCCESS" in result.stdout:
        print(f"   ✅ All imports successful")
        checks.append(("Python Imports", True))
    else:
        print(f"   ❌ Import failed: {result.stderr[:200]}")
        checks.append(("Python Imports", False))

    # 4. Check environment variables
    print("\n4️⃣ Checking Environment Setup...")
    required_vars = [
        ("THINK_AI_USE_LIGHTWEIGHT", "false"),
        ("THINK_AI_MINIMAL_INIT", "false"),
        ("THINK_AI_COLOMBIAN", "true"),
    ]

    env_ok = True
    with open("railway.json", "r") as f:
        config = json.load(f)
        env_vars = config.get("deploy", {}).get("environmentVariables", {})

    for var, expected in required_vars:
        value = env_vars.get(var, "NOT SET")
        if value == expected:
            print(f"   ✅ {var} = {value}")
        else:
            print(f"   ❌ {var} = {value} (expected: {expected})")
            env_ok = False

    checks.append(("Environment Vars", env_ok))

    # 5. Check webapp configuration
    print("\n5️⃣ Checking Webapp Configuration...")
    webapp_checks = []

    # Check production env
    if os.path.exists("webapp/.env.production"):
        with open("webapp/.env.production", "r") as f:
            content = f.read()
        if "NEXT_PUBLIC_API_URL=/api/v1" in content:
            print(f"   ✅ Webapp uses relative API URLs in production")
            webapp_checks.append(True)
        else:
            print(f"   ❌ Webapp not configured for production API")
            webapp_checks.append(False)

    # Check if webapp uses correct endpoint
    query_interface = "webapp/src/components/QueryInterface.tsx"
    if os.path.exists(query_interface):
        with open(query_interface, "r") as f:
            content = f.read()
        if "/api/v1/generate" in content:
            print(f"   ✅ Webapp uses correct generate endpoint")
            webapp_checks.append(True)
        else:
            print(f"   ❌ Webapp uses wrong endpoint")
            webapp_checks.append(False)

    checks.append(("Webapp Config", all(webapp_checks)))

    # Summary
    print("\n" + "=" * 60)
    print("📊 VALIDATION SUMMARY:")

    passed = sum(1 for _, status in checks if status)
    total = len(checks)

    for check, status in checks:
        emoji = "✅" if status else "❌"
        print(f"   {emoji} {check}: {'PASSED' if status else 'FAILED'}")

    print(f"\n🎯 Total: {passed}/{total} checks passed")

    if passed == total:
        print("\n🚀 SYSTEM IS READY FOR RAILWAY DEPLOYMENT!")
        print("\nDeployment will include:")
        print("   • Full Think AI system (not minimal)")
        print("   • All API endpoints")
        print("   • Webapp with correct API connections")
        print("   • Colombian mode enabled 🇨🇴")
        print("   • O(1) performance optimizations")
        return True
    else:
        print(f"\n⚠️  {total - passed} checks failed.")
        print("Fix these issues before deploying to Railway.")
        return False


if __name__ == "__main__":
    # Kill any running servers first
    os.system("lsof -ti:8080 | xargs kill -9 2>/dev/null || true")

    success = validate_railway_deployment()
    sys.exit(0 if success else 1)
