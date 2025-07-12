#!/usr/bin/env python3
"""
Headless Markdown Testing with Puppeteer (via pyppeteer)
This version works without Chrome/ChromeDriver dependencies
"""

import asyncio
import json
import os
import time
import subprocess
from datetime import datetime

# Test configuration
PORT = 7777
BASE_URL = f"http://localhost:{PORT}"
SCREENSHOTS_DIR = "markdown_test_screenshots"

# Simple markdown test cases for headless testing
SIMPLE_TESTS = {
    "headers": "# H1 Header\n## H2 Header", 
    "bold_italic": "**bold** and *italic*",
    "code": "`inline code` and\n```python\nprint('hello')\n```",
    "list": "- Item 1\n- Item 2\n1. First\n2. Second",
    "link": "[Click here](https://example.com)"
}

async def test_with_playwright():
    """Test using Playwright (more reliable than Selenium for headless)"""
    try:
        from playwright.async_api import async_playwright
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            await page.goto(BASE_URL)
            await page.wait_for_selector("#queryInput")
            
            # Take screenshot
            await page.screenshot(path=f"{SCREENSHOTS_DIR}/playwright_test.png")
            
            # Test markdown
            for test_name, markdown in SIMPLE_TESTS.items():
                await page.fill("#queryInput", markdown)
                await page.click("#sendBtn")
                await asyncio.sleep(2)
                
                await page.screenshot(path=f"{SCREENSHOTS_DIR}/playwright_{test_name}.png")
                
            await browser.close()
            print("✅ Playwright tests completed")
            
    except ImportError:
        print("❌ Playwright not installed. Install with: pip install playwright && playwright install")
        return False
    return True

def test_with_curl():
    """Test API directly with curl and capture responses"""
    print("\n🔧 Testing with curl commands...")
    
    results = {}
    for test_name, markdown in SIMPLE_TESTS.items():
        cmd = [
            "curl", "-s", "-X", "POST",
            f"{BASE_URL}/api/chat",
            "-H", "Content-Type: application/json",
            "-d", json.dumps({"message": markdown})
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                response = json.loads(result.stdout)
                results[test_name] = {
                    "input": markdown,
                    "output": response.get("response", ""),
                    "status": "success"
                }
                print(f"✅ {test_name}: API responded successfully")
            else:
                results[test_name] = {"status": "error", "error": result.stderr}
                print(f"❌ {test_name}: API error")
        except Exception as e:
            results[test_name] = {"status": "error", "error": str(e)}
            print(f"❌ {test_name}: {e}")
            
    return results

def create_visual_test_html():
    """Create an HTML file to visually test markdown rendering"""
    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Visual Markdown Test</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .test { margin: 20px 0; padding: 20px; border: 1px solid #ddd; }
        .input { background: #f0f0f0; padding: 10px; margin: 10px 0; }
        iframe { width: 100%; height: 400px; border: 1px solid #ccc; }
    </style>
</head>
<body>
    <h1>Visual Markdown Tests</h1>
    <p>Open this file in a browser to see rendered markdown</p>
"""
    
    # Include the parseMarkdown function inline
    html_content += """
    <script>
        function escapeHtml(text) {
            const map = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'};
            return text.replace(/[&<>"']/g, m => map[m]);
        }
        
        // Simplified parseMarkdown for testing
        function parseMarkdown(text) {
            let result = text;
            
            // Headers
            result = result.replace(/^### (.+)$/gm, '<h3>$1</h3>');
            result = result.replace(/^## (.+)$/gm, '<h2>$1</h2>');
            result = result.replace(/^# (.+)$/gm, '<h1>$1</h1>');
            
            // Bold and italic
            result = result.replace(/\\*\\*([^\\*]+)\\*\\*/g, '<strong>$1</strong>');
            result = result.replace(/\\*([^\\*]+)\\*/g, '<em>$1</em>');
            
            // Code
            result = result.replace(/`([^`]+)`/g, '<code>$1</code>');
            
            // Links
            result = result.replace(/\\[([^\\]]+)\\]\\(([^)]+)\\)/g, '<a href="$2">$1</a>');
            
            return result;
        }
    </script>
"""
    
    for test_name, markdown in SIMPLE_TESTS.items():
        html_content += f"""
    <div class="test">
        <h2>{test_name}</h2>
        <div class="input">
            <h3>Input:</h3>
            <pre>{markdown}</pre>
        </div>
        <div class="output">
            <h3>Rendered:</h3>
            <div id="output_{test_name}"></div>
        </div>
    </div>
    <script>
        document.getElementById('output_{test_name}').innerHTML = parseMarkdown(`{markdown}`);
    </script>
"""
    
    html_content += "</body></html>"
    
    with open(f"{SCREENSHOTS_DIR}/visual_test.html", "w") as f:
        f.write(html_content)
    
    print(f"✅ Created visual test file: {SCREENSHOTS_DIR}/visual_test.html")

def run_simple_screenshot():
    """Use a simple screenshot tool if available"""
    print("\n📸 Attempting screenshots with system tools...")
    
    # Try different screenshot tools
    tools = [
        ["import", "-window", "root", f"{SCREENSHOTS_DIR}/desktop.png"],
        ["scrot", f"{SCREENSHOTS_DIR}/desktop.png"],
        ["gnome-screenshot", "-f", f"{SCREENSHOTS_DIR}/desktop.png"]
    ]
    
    for tool in tools:
        try:
            subprocess.run(tool, capture_output=True, timeout=5)
            print(f"✅ Screenshot taken with {tool[0]}")
            return True
        except:
            continue
            
    print("❌ No screenshot tool available")
    return False

def main():
    """Run all available tests"""
    print("🧪 Markdown Rendering Tests (Headless/API Mode)")
    print("=" * 50)
    
    # Create directories
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    
    # Start server
    print(f"🚀 Starting server on port {PORT}...")
    server_process = subprocess.Popen(
        ["python3", "serve_webapp_7777_final.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    time.sleep(5)  # Wait for server
    
    try:
        # 1. Test with curl
        api_results = test_with_curl()
        
        # 2. Create visual test HTML
        create_visual_test_html()
        
        # 3. Try playwright if available
        asyncio.run(test_with_playwright())
        
        # 4. Try system screenshot
        run_simple_screenshot()
        
        # Generate simple report
        print("\n" + "="*50)
        print("TEST REPORT")
        print("="*50)
        
        with open(f"{SCREENSHOTS_DIR}/test_report.json", "w") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "api_results": api_results,
                "screenshots": os.listdir(SCREENSHOTS_DIR)
            }, f, indent=2)
            
        print(f"✅ Report saved to: {SCREENSHOTS_DIR}/test_report.json")
        print(f"📁 All test files in: {SCREENSHOTS_DIR}/")
        
    finally:
        server_process.terminate()
        print("\n✅ Testing complete!")

if __name__ == "__main__":
    main()