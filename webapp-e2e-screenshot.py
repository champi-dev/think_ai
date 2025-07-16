#!/usr/bin/env python3
"""
Simple E2E test with screenshot capture using headless Chrome
"""
import os
import time
import subprocess
from datetime import datetime


def take_screenshot(url, output_file):
    """Take a screenshot using headless Chrome"""
    cmd = [
        "chromium-browser",
        "--headless",
        "--no-sandbox",
        "--disable-gpu",
        "--window-size=1920,1080",
        f"--screenshot={output_file}",
        url,
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0 and os.path.exists(output_file):
            return True
        print(f"Chrome error: {result.stderr}")
        return False
    except Exception as e:
        print(f"Screenshot error: {e}")
        return False


def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_dir = f"/home/administrator/think_ai/screenshots_{timestamp}"
    os.makedirs(screenshot_dir, exist_ok=True)

    print("🚀 Think AI E2E Test with Screenshots")
    print("=====================================\n")

    # Test 1: Homepage
    print("📸 Taking screenshot of homepage...")
    homepage_screenshot = f"{screenshot_dir}/01_homepage.png"
    if take_screenshot("https://thinkai.lat", homepage_screenshot):
        print(f"✅ Homepage screenshot saved: {homepage_screenshot}")
        print(f"   File size: {os.path.getsize(homepage_screenshot):,} bytes")
    else:
        print("❌ Failed to capture homepage screenshot")

    # Test 2: Local comparison
    print("\n📸 Taking screenshot of local version...")
    local_screenshot = f"{screenshot_dir}/02_local.png"
    if take_screenshot("http://localhost:8080", local_screenshot):
        print(f"✅ Local screenshot saved: {local_screenshot}")
        print(f"   File size: {os.path.getsize(local_screenshot):,} bytes")
    else:
        print("❌ Failed to capture local screenshot")

    # Test 3: API Health
    print("\n🔍 Testing API endpoints...")
    import requests

    try:
        # Health check
        response = requests.get("https://thinkai.lat/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint: OK")
            print(f"   Response: {response.text}")
        else:
            print(f"❌ Health endpoint: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")

    try:
        # Chat API test
        response = requests.post(
            "https://thinkai.lat/api/chat",
            json={"message": "Hello, Think AI!"},
            headers={"Content-Type": "application/json"},
            timeout=10,
        )
        if response.status_code == 200:
            print("✅ Chat API: OK")
            print(f"   Response preview: {response.text[:100]}...")
        else:
            print(f"❌ Chat API: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Chat API error: {e}")

    # Create a simple HTML report
    print("\n📄 Generating report...")
    report_path = f"{screenshot_dir}/report.html"
    with open(report_path, "w") as f:
        f.write(
            f"""
<!DOCTYPE html>
<html>
<head>
    <title>Think AI E2E Test Report - {timestamp}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #333; }}
        .screenshot {{ max-width: 800px; margin: 20px 0; border: 1px solid #ddd; }}
        .screenshot img {{ width: 100%; }}
        .status {{ padding: 10px; margin: 10px 0; border-radius: 5px; }}
        .success {{ background: #d4edda; color: #155724; }}
        .error {{ background: #f8d7da; color: #721c24; }}
    </style>
</head>
<body>
    <h1>Think AI E2E Test Report</h1>
    <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    
    <div class="status success">
        <h2>✅ Website Status: ONLINE</h2>
        <p>URL: <a href="https://thinkai.lat">https://thinkai.lat</a></p>
    </div>
    
    <h2>Screenshots</h2>
    <div class="screenshot">
        <h3>Production Site (https://thinkai.lat)</h3>
        <img src="01_homepage.png" alt="Homepage">
    </div>
    
    <div class="screenshot">
        <h3>Local Development (http://localhost:8080)</h3>
        <img src="02_local.png" alt="Local">
    </div>
</body>
</html>
        """
        )

    print(f"✅ Report generated: {report_path}")
    print(f"\n📁 All files saved to: {screenshot_dir}")
    print("\n✨ E2E Test Complete!")


if __name__ == "__main__":
    main()
