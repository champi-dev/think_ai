#!/usr/bin/env python3
"""
Manual markdown testing with screenshot capability
Serves the HTML files and provides commands to take screenshots
"""

import http.server
import socketserver
import threading
import time
import os
import subprocess
from datetime import datetime


def start_server(port=8090):
    """Start HTTP server in a thread"""
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)

    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    return httpd


def take_screenshot(url, filename):
    """Take a screenshot using a headless browser"""
    try:
        # Try using chromium/chrome in headless mode
        cmd = [
            "chromium-browser",
            "--headless",
            "--disable-gpu",
            "--screenshot=" + filename,
            "--window-size=1280,800",
            "--force-device-scale-factor=2",
            url,
        ]

        # Try different browser commands
        browsers = [
            "chromium-browser",
            "chromium",
            "google-chrome",
            "google-chrome-stable",
        ]

        for browser in browsers:
            cmd[0] = browser
            try:
                subprocess.run(cmd, check=True, capture_output=True)
                print(f"✓ Screenshot saved: {filename}")
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue

        print("✗ Could not find a suitable browser for screenshots")
        print("  Please install chromium: sudo apt-get install chromium-browser")
        return False

    except Exception as e:
        print(f"✗ Screenshot failed: {str(e)}")
        return False


def main():
    print("Think AI Markdown Manual Testing")
    print("=" * 60)

    # Create screenshots directory
    os.makedirs("manual_screenshots", exist_ok=True)

    # Start server
    print("\nStarting HTTP server on port 8090...")
    httpd = start_server(8090)
    print("✓ Server started")

    print("\nYou can now test the markdown rendering by visiting:")
    print("  - Custom Parser: http://localhost:8090/minimal_3d.html")
    print("  - Marked.js:     http://localhost:8090/minimal_3d_markdown.html")

    print("\nTest markdown examples to try:")
    print("-" * 60)

    test_examples = [
        "**Bold** and *italic* and ***bold italic***",
        "# Header 1\\n## Header 2\\n### Header 3",
        "- List item 1\\n- List item 2\\n  - Nested item",
        "1. First\\n2. Second\\n3. Third",
        "`inline code` and\\n```javascript\\nfunction test() {\\n  return 42;\\n}\\n```",
        "[Link to OpenAI](https://openai.com)",
        "> This is a blockquote\\n> with multiple lines",
        "| Col 1 | Col 2 |\\n|-------|-------|\\n| A     | B     |",
    ]

    for i, example in enumerate(test_examples, 1):
        print(f"\n{i}. {example.replace('\\n', '\\n   ')}")

    print("\n" + "-" * 60)
    print("\nCommands:")
    print("  s1 - Take screenshot of custom parser")
    print("  s2 - Take screenshot of marked.js version")
    print("  sb - Take screenshots of both")
    print("  q  - Quit")

    try:
        while True:
            cmd = input("\nCommand: ").strip().lower()

            if cmd == "q":
                break
            elif cmd == "s1":
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                take_screenshot(
                    "http://localhost:8090/minimal_3d.html",
                    f"manual_screenshots/custom_parser_{timestamp}.png",
                )
            elif cmd == "s2":
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                take_screenshot(
                    "http://localhost:8090/minimal_3d_markdown.html",
                    f"manual_screenshots/marked_js_{timestamp}.png",
                )
            elif cmd == "sb":
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                take_screenshot(
                    "http://localhost:8090/minimal_3d.html",
                    f"manual_screenshots/custom_parser_{timestamp}.png",
                )
                take_screenshot(
                    "http://localhost:8090/minimal_3d_markdown.html",
                    f"manual_screenshots/marked_js_{timestamp}.png",
                )
            else:
                print("Invalid command. Use s1, s2, sb, or q")

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")

    finally:
        print("\nShutting down server...")
        httpd.shutdown()
        print("✓ Server stopped")

        # List screenshots
        screenshots = os.listdir("manual_screenshots")
        if screenshots:
            print(f"\nScreenshots saved ({len(screenshots)} files):")
            for f in sorted(screenshots):
                print(f"  - {f}")


if __name__ == "__main__":
    main()
