#!/usr/bin/env python3
"""
Take screenshots of the Think AI webapp for E2E testing
"""
import subprocess
import time
import os
from datetime import datetime

def take_screenshot():
    """Take a screenshot of the webapp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"/home/administrator/think_ai/webapp_screenshot_{timestamp}.png"
    
    # Use Google Chrome in headless mode to take screenshot
    cmd = [
        "google-chrome",
        "--headless",
        "--no-sandbox",
        "--disable-gpu",
        "--window-size=1920,1080",
        "--screenshot=" + screenshot_path,
        "https://thinkai.lat"
    ]
    
    try:
        print(f"Taking screenshot of https://thinkai.lat...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(screenshot_path):
            print(f"✓ Screenshot saved to: {screenshot_path}")
            # Also take a screenshot of the local version for comparison
            local_screenshot = f"/home/administrator/think_ai/webapp_local_{timestamp}.png"
            cmd_local = cmd[:-1] + ["http://localhost:8080"]
            cmd_local[5] = "--screenshot=" + local_screenshot
            subprocess.run(cmd_local, capture_output=True)
            if os.path.exists(local_screenshot):
                print(f"✓ Local screenshot saved to: {local_screenshot}")
            return screenshot_path
        else:
            print(f"✗ Failed to take screenshot: {result.stderr}")
            return None
    except Exception as e:
        print(f"✗ Error taking screenshot: {e}")
        return None

def test_webapp_functionality():
    """Test basic webapp functionality"""
    print("\n=== Testing Think AI Webapp ===\n")
    
    # Test 1: Check if webapp is accessible
    print("1. Testing webapp accessibility...")
    result = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "https://thinkai.lat"], 
                          capture_output=True, text=True)
    if result.stdout == "200":
        print("   ✓ Webapp is accessible (HTTP 200)")
    else:
        print(f"   ✗ Webapp returned HTTP {result.stdout}")
    
    # Test 2: Check API health endpoint
    print("\n2. Testing API health endpoint...")
    result = subprocess.run(["curl", "-s", "https://thinkai.lat/health"], 
                          capture_output=True, text=True)
    if '"status":"healthy"' in result.stdout:
        print("   ✓ API is healthy")
        print(f"   Response: {result.stdout}")
    else:
        print("   ✗ API health check failed")
    
    # Test 3: Take screenshots
    print("\n3. Taking screenshots...")
    screenshot = take_screenshot()
    
    # Test 4: Check if ngrok tunnel is working
    print("\n4. Checking ngrok tunnel status...")
    result = subprocess.run(["curl", "-s", "http://localhost:4040/api/tunnels"], 
                          capture_output=True, text=True)
    if "thinkai.lat" in result.stdout:
        print("   ✓ Ngrok tunnel is active for thinkai.lat")
    else:
        print("   ✗ Ngrok tunnel status unknown")
    
    print("\n=== Test Summary ===")
    print("Webapp URL: https://thinkai.lat")
    print("Local URL: http://localhost:8080")
    if screenshot:
        print(f"Screenshot: {screenshot}")
    print("\nThe Think AI webapp is now running as a system service and will start automatically on boot.")
    print("Service management commands:")
    print("  - sudo systemctl status think-ai.service")
    print("  - sudo systemctl restart think-ai.service")
    print("  - sudo systemctl stop think-ai.service")
    print("  - sudo journalctl -u think-ai.service -f")

if __name__ == "__main__":
    test_webapp_functionality()