#!/usr/bin/env python3
"""Pre-commit QA Environment - Manual testing interface for Think AI."""

import subprocess
import time
import webbrowser
import sys
import os
from pathlib import Path

def launch_qa_environment():
    """Launch full QA testing environment for manual verification."""
    print("🧪 THINK AI QA ENVIRONMENT")
    print("=" * 50)
    print("Starting all services for manual testing...\n")
    
    processes = []
    
    try:
        # 1. Start API server
        print("1️⃣  Starting API server on http://localhost:8080...")
        api_proc = subprocess.Popen(
            [sys.executable, "think_ai_minimal.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        processes.append(api_proc)
        time.sleep(3)
        
        # 2. Start webapp
        print("2️⃣  Starting webapp on http://localhost:3000...")
        webapp_proc = subprocess.Popen(
            ["npm", "start"],
            cwd="webapp",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        processes.append(webapp_proc)
        time.sleep(5)
        
        # 3. Start consciousness demo
        print("3️⃣  Starting consciousness demo on http://localhost:5000...")
        demo_proc = subprocess.Popen(
            [sys.executable, "servers/demo_server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        processes.append(demo_proc)
        time.sleep(2)
        
        # 4. Run test suite
        print("\n4️⃣  Running full test suite...")
        test_result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
            capture_output=True,
            text=True
        )
        
        print("\n📊 TEST RESULTS:")
        print("-" * 50)
        if test_result.returncode == 0:
            print("✅ All tests passed!")
        else:
            print("❌ Some tests failed:")
            print(test_result.stdout[-500:])  # Last 500 chars
        
        # 5. Display QA checklist
        print("\n📋 MANUAL QA CHECKLIST:")
        print("-" * 50)
        print("Please verify the following:")
        print("")
        print("[ ] 1. API Health: http://localhost:8080/health")
        print("[ ] 2. API Docs: http://localhost:8080/docs")
        print("[ ] 3. Chat Interface: http://localhost:3000")
        print("[ ] 4. Consciousness Demo: http://localhost:5000")
        print("[ ] 5. Test neural pathways creation")
        print("[ ] 6. Test O(1) vector search performance")
        print("[ ] 7. Test self-training functionality")
        print("[ ] 8. Test multilingual responses")
        print("[ ] 9. Test code generation")
        print("[ ] 10. Verify Docker services are healthy")
        print("")
        print("🔍 Quick Tests:")
        print("-" * 50)
        print("curl http://localhost:8080/api/chat -X POST -H 'Content-Type: application/json' -d '{\"message\": \"Hello\"}'")
        print("curl http://localhost:8080/api/train -X POST")
        print("curl http://localhost:8080/api/health")
        print("")
        
        # Open browser tabs
        print("🌐 Opening browser tabs...")
        webbrowser.open("http://localhost:8080/docs")
        time.sleep(1)
        webbrowser.open("http://localhost:3000")
        time.sleep(1)
        webbrowser.open("http://localhost:5000")
        
        print("\n⏳ QA environment is running. Press Enter when testing is complete...")
        input()
        
        # Ask for QA approval
        print("\n❓ Did all manual tests pass? (y/n): ", end="")
        approval = input().lower().strip()
        
        if approval != 'y':
            print("❌ QA failed. Please fix issues before committing.")
            return False
        
        print("✅ QA approved!")
        return True
        
    except Exception as e:
        print(f"❌ Error in QA environment: {e}")
        return False
        
    finally:
        # Cleanup
        print("\n🧹 Cleaning up QA environment...")
        for proc in processes:
            try:
                proc.terminate()
                proc.wait(timeout=5)
            except:
                proc.kill()
        print("✅ QA environment closed")

if __name__ == "__main__":
    success = launch_qa_environment()
    sys.exit(0 if success else 1)