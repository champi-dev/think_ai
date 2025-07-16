#!/usr/bin/env python3
"""
E2E test for Think AI markdown rendering
Tests both custom parser and marked.js implementations
"""

import asyncio
import os
import sys
import time
import json
from datetime import datetime
import subprocess
from pathlib import Path

# Use Playwright for browser automation
try:
    from playwright.async_api import async_playwright
except ImportError:
    print("Installing playwright...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
    subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
    from playwright.async_api import async_playwright

# Test data - various markdown elements
TEST_MESSAGES = [
    # Basic formatting
    "**Bold text** and *italic text* and ***bold italic***",
    # Headers
    "# Header 1\n## Header 2\n### Header 3",
    # Lists
    "Unordered list:\n- Item 1\n- Item 2\n  - Nested item\n- Item 3",
    "Ordered list:\n1. First\n2. Second\n3. Third",
    # Code blocks
    "Inline code: `console.log('Hello')` and code block:\n```javascript\nfunction test() {\n  return 42;\n}\n```",
    # Links and quotes
    "[OpenAI](https://openai.com) and [GitHub](https://github.com)\n\n> This is a blockquote\n> with multiple lines",
    # Tables (for marked.js version)
    "| Column 1 | Column 2 |\n|----------|----------|\n| Cell 1   | Cell 2   |\n| Cell 3   | Cell 4   |",
    # Complex mixed content
    """## Complex Example

Here's a list with **formatting**:
1. First item with `code`
2. Second item with [link](https://example.com)
   - Nested with *italic*
   - Another nested

```python
def hello():
    print("World")
```

> Quote with **bold** and `code`""",
]


async def test_interface(page, interface_name, url):
    """Test a single interface"""
    print(f"\n{'='*60}")
    print(f"Testing {interface_name}")
    print(f"URL: {url}")
    print(f"{'='*60}")

    screenshots = []

    try:
        # Navigate to the page
        await page.goto(url, wait_until="networkidle")
        print(f"✓ Page loaded successfully")

        # Wait for interface to be ready
        await page.wait_for_selector("#queryInput", timeout=10000)
        await page.wait_for_selector(".messages", timeout=10000)
        print(f"✓ Interface elements found")

        # Take initial screenshot
        screenshot_path = f"screenshots/{interface_name}_0_initial.png"
        await page.screenshot(path=screenshot_path, full_page=True)
        screenshots.append(screenshot_path)
        print(f"✓ Initial screenshot saved: {screenshot_path}")

        # Test each markdown element
        for i, test_content in enumerate(TEST_MESSAGES, 1):
            print(f"\nTest {i}: {test_content[:50]}...")

            # Type the message
            await page.fill("#queryInput", test_content)

            # Send the message
            await page.click("#sendBtn")

            # Wait for response
            await page.wait_for_timeout(2000)  # Give time for rendering

            # Scroll to bottom to see latest message
            await page.evaluate(
                'document.querySelector(".messages").scrollTop = document.querySelector(".messages").scrollHeight'
            )

            # Take screenshot
            screenshot_path = f"screenshots/{interface_name}_{i}_{test_content[:20].replace(' ', '_').replace('/', '_')}.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            screenshots.append(screenshot_path)
            print(f"✓ Screenshot saved: {screenshot_path}")

            # Check for errors in console
            console_messages = []
            page.on("console", lambda msg: console_messages.append(msg))

        # Final full-page screenshot
        await page.wait_for_timeout(1000)
        final_screenshot = f"screenshots/{interface_name}_final_all_messages.png"
        await page.screenshot(path=final_screenshot, full_page=True)
        screenshots.append(final_screenshot)
        print(f"\n✓ Final screenshot with all messages: {final_screenshot}")

        return True, screenshots

    except Exception as e:
        error_screenshot = f"screenshots/{interface_name}_error.png"
        await page.screenshot(path=error_screenshot, full_page=True)
        print(f"✗ Error: {str(e)}")
        print(f"  Error screenshot: {error_screenshot}")
        return False, screenshots


async def start_test_server():
    """Start a simple HTTP server for testing"""
    process = await asyncio.create_subprocess_exec(
        sys.executable,
        "-m",
        "http.server",
        "8090",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    # Wait for server to start
    await asyncio.sleep(2)
    return process


async def main():
    """Main test runner"""
    print("Think AI Markdown Rendering E2E Test")
    print("=" * 60)

    # Create screenshots directory
    os.makedirs("screenshots", exist_ok=True)

    # Start test server
    print("Starting test HTTP server on port 8090...")
    server_process = await start_test_server()

    try:
        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(
                headless=False,  # Set to True for CI/CD
                args=["--no-sandbox", "--disable-setuid-sandbox"],
            )

            context = await browser.new_context(
                viewport={"width": 1280, "height": 800},
                device_scale_factor=2,  # High quality screenshots
            )

            # Test both interfaces
            interfaces = [
                ("Custom Parser", "http://localhost:8090/minimal_3d.html"),
                ("Marked.js", "http://localhost:8090/minimal_3d_markdown.html"),
            ]

            results = {}
            all_screenshots = []

            for name, url in interfaces:
                page = await context.new_page()
                success, screenshots = await test_interface(page, name, url)
                results[name] = success
                all_screenshots.extend(screenshots)
                await page.close()

            await browser.close()

            # Generate report
            print("\n" + "=" * 60)
            print("TEST RESULTS")
            print("=" * 60)

            for name, success in results.items():
                status = "✓ PASSED" if success else "✗ FAILED"
                print(f"{name}: {status}")

            # Save test report
            report = {
                "test_date": datetime.now().isoformat(),
                "results": results,
                "screenshots": all_screenshots,
                "test_messages": TEST_MESSAGES,
            }

            with open("markdown_test_report.json", "w") as f:
                json.dump(report, f, indent=2)

            print(f"\n✓ Test report saved: markdown_test_report.json")
            print(f"✓ Screenshots saved in: screenshots/")
            print(f"\nTotal screenshots: {len(all_screenshots)}")

            # Create HTML report
            create_html_report(report)

    finally:
        # Stop server
        server_process.terminate()
        await server_process.wait()


def create_html_report(report):
    """Create an HTML report with all screenshots"""
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Think AI Markdown Rendering Test Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1, h2 {{
            color: #333;
        }}
        .screenshot {{
            margin: 20px 0;
            border: 1px solid #ddd;
            border-radius: 5px;
            overflow: hidden;
        }}
        .screenshot img {{
            width: 100%;
            display: block;
        }}
        .screenshot-title {{
            background: #f0f0f0;
            padding: 10px;
            font-weight: bold;
        }}
        .status {{
            display: inline-block;
            padding: 5px 10px;
            border-radius: 5px;
            color: white;
            font-weight: bold;
        }}
        .status.passed {{
            background: #4CAF50;
        }}
        .status.failed {{
            background: #f44336;
        }}
        .test-message {{
            background: #f5f5f5;
            padding: 10px;
            margin: 10px 0;
            border-left: 3px solid #2196F3;
            font-family: monospace;
            white-space: pre-wrap;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Think AI Markdown Rendering Test Report</h1>
        <p>Test Date: {report['test_date']}</p>
        
        <h2>Test Results</h2>
"""

    for name, success in report["results"].items():
        status_class = "passed" if success else "failed"
        status_text = "PASSED" if success else "FAILED"
        html += (
            f'<p>{name}: <span class="status {status_class}">{status_text}</span></p>'
        )

    html += """
        <h2>Test Messages</h2>
"""

    for i, msg in enumerate(report["test_messages"], 1):
        html += f'<div class="test-message">Test {i}:\n{msg}</div>'

    html += """
        <h2>Screenshots</h2>
"""

    for screenshot in report["screenshots"]:
        html += f"""
        <div class="screenshot">
            <div class="screenshot-title">{screenshot}</div>
            <img src="{screenshot}" alt="{screenshot}">
        </div>
"""

    html += """
    </div>
</body>
</html>
"""

    with open("markdown_test_report.html", "w") as f:
        f.write(html)

    print(f"✓ HTML report saved: markdown_test_report.html")


if __name__ == "__main__":
    asyncio.run(main())
