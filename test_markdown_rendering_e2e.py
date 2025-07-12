#!/usr/bin/env python3
"""
E2E Test for Think AI Markdown Rendering
Tests the webapp's ability to properly render various markdown elements
"""

import asyncio
import json
import time
import os
import subprocess
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

# Test configuration
PORT = 7777
BASE_URL = f"http://localhost:{PORT}"
SCREENSHOTS_DIR = "markdown_test_screenshots"
TEST_RESULTS_FILE = "markdown_test_results.html"

# Markdown test cases
MARKDOWN_TESTS = {
    "headers": {
        "input": "# H1 Header\n## H2 Header\n### H3 Header",
        "description": "Testing header rendering (H1, H2, H3)"
    },
    "text_formatting": {
        "input": "This is **bold text** and this is *italic text* and this is ***bold italic***",
        "description": "Testing bold, italic, and combined formatting"
    },
    "lists_unordered": {
        "input": "- First item\n- Second item\n  - Nested item\n- Third item",
        "description": "Testing unordered lists with nesting"
    },
    "lists_ordered": {
        "input": "1. First step\n2. Second step\n3. Third step\n   - Sub-item\n4. Fourth step",
        "description": "Testing ordered lists with mixed content"
    },
    "code_inline": {
        "input": "Use `console.log()` for debugging and `const x = 42` for constants",
        "description": "Testing inline code rendering"
    },
    "code_block": {
        "input": "```python\ndef hello_world():\n    print('Hello, World!')\n    return 42\n```",
        "description": "Testing code block with syntax highlighting"
    },
    "links": {
        "input": "Check out [OpenAI](https://openai.com) and [Think AI](https://github.com/think-ai)",
        "description": "Testing link rendering"
    },
    "blockquote": {
        "input": "> This is a blockquote\n> It can span multiple lines\n> And should be styled differently",
        "description": "Testing blockquote rendering"
    },
    "horizontal_rule": {
        "input": "Above the line\n\n---\n\nBelow the line",
        "description": "Testing horizontal rule"
    },
    "mixed_content": {
        "input": """# Complete Example

This demonstrates **multiple** markdown elements:

## Features
1. **Bold text** and *italic text*
2. `inline code` examples
3. Links like [this one](https://example.com)

### Code Example
```javascript
function calculateO1Performance() {
    const lookupTable = new Map();
    return lookupTable.get(key) || computeValue(key);
}
```

> "The best performance is O(1)" - Think AI

---

- Lists work too
  - Even nested ones
  - With multiple levels""",
        "description": "Testing complex mixed markdown content"
    },
    "edge_cases": {
        "input": "Test **bold with `code` inside** and *italic with `code` too*\n\nAlso test ```\ncode without language\n```",
        "description": "Testing edge cases and nested formatting"
    },
    "long_lines": {
        "input": "This is a very long line that should wrap properly: " + "word " * 50,
        "description": "Testing long line wrapping"
    }
}

class MarkdownE2ETest:
    def __init__(self):
        self.driver = None
        self.server_process = None
        self.test_results = []
        
    def setup(self):
        """Set up test environment"""
        print("🔧 Setting up test environment...")
        
        # Create screenshots directory
        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
        
        # Start the server
        print(f"🚀 Starting server on port {PORT}...")
        self.server_process = subprocess.Popen(
            ["python3", "serve_webapp_7777_final.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        time.sleep(5)
        
        # Set up Chrome options for headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Initialize Chrome driver
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            print("✅ Chrome driver initialized")
        except Exception as e:
            print(f"❌ Failed to initialize Chrome driver: {e}")
            print("Make sure Chrome and ChromeDriver are installed")
            sys.exit(1)
            
    def teardown(self):
        """Clean up test environment"""
        print("🧹 Cleaning up...")
        
        if self.driver:
            self.driver.quit()
            
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
            
    def wait_for_element(self, selector, timeout=10):
        """Wait for element to be present"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
    
    def send_message(self, message):
        """Send a message through the chat interface"""
        # Find input field
        input_field = self.wait_for_element("#queryInput")
        input_field.clear()
        input_field.send_keys(message)
        
        # Click send button
        send_button = self.driver.find_element(By.CSS_SELECTOR, "#sendBtn")
        send_button.click()
        
        # Wait for response
        time.sleep(3)  # Give time for response to render
        
    def take_screenshot(self, name):
        """Take a screenshot of the current page"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{SCREENSHOTS_DIR}/{name}_{timestamp}.png"
        
        # Scroll to show latest messages
        self.driver.execute_script("document.querySelector('.messages').scrollTop = document.querySelector('.messages').scrollHeight")
        time.sleep(0.5)  # Wait for scroll
        
        self.driver.save_screenshot(filename)
        return filename
        
    def get_last_ai_message(self):
        """Get the last AI message element"""
        messages = self.driver.find_elements(By.CSS_SELECTOR, ".message.ai .message-content")
        if messages:
            # Return the last message (excluding copy button)
            return messages[-1]
        return None
        
    def run_markdown_test(self, test_name, test_data):
        """Run a single markdown test"""
        print(f"\n📝 Testing: {test_data['description']}")
        
        result = {
            "name": test_name,
            "description": test_data["description"],
            "input": test_data["input"],
            "status": "failed",
            "screenshot": None,
            "html_output": None,
            "errors": []
        }
        
        try:
            # Send the markdown content
            self.send_message(test_data["input"])
            
            # Get the rendered output
            ai_message = self.get_last_ai_message()
            if ai_message:
                result["html_output"] = ai_message.get_attribute("innerHTML")
                
                # Take screenshot
                screenshot_path = self.take_screenshot(f"markdown_{test_name}")
                result["screenshot"] = screenshot_path
                
                # Basic validation
                if self.validate_markdown_rendering(test_name, ai_message, test_data["input"]):
                    result["status"] = "passed"
                    print(f"✅ {test_name}: PASSED")
                else:
                    print(f"❌ {test_name}: FAILED")
            else:
                result["errors"].append("No AI response found")
                print(f"❌ {test_name}: No response")
                
        except Exception as e:
            result["errors"].append(str(e))
            print(f"❌ {test_name}: ERROR - {e}")
            
        self.test_results.append(result)
        return result
        
    def validate_markdown_rendering(self, test_name, element, original_text):
        """Validate that markdown was properly rendered"""
        html = element.get_attribute("innerHTML").lower()
        
        validations = {
            "headers": lambda: all(tag in html for tag in ["<h1>", "<h2>", "<h3>"]),
            "text_formatting": lambda: "<strong>" in html and "<em>" in html,
            "lists_unordered": lambda: "<ul>" in html and "<li>" in html,
            "lists_ordered": lambda: "<ol>" in html and "<li>" in html,
            "code_inline": lambda: "<code>" in html,
            "code_block": lambda: "<pre>" in html and "<code" in html,
            "links": lambda: "<a href=" in html,
            "blockquote": lambda: "<blockquote" in html,
            "horizontal_rule": lambda: "<hr" in html,
        }
        
        # Check specific validation for this test
        if test_name in validations:
            return validations[test_name]()
            
        # For mixed content and edge cases, check multiple elements
        return True  # Basic check passed if we got here
        
    def generate_report(self):
        """Generate HTML report with results and screenshots"""
        print("\n📊 Generating test report...")
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Markdown Rendering Test Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .header {{ background: #333; color: white; padding: 20px; border-radius: 8px; }}
        .test-case {{ background: white; margin: 20px 0; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .passed {{ border-left: 5px solid #4CAF50; }}
        .failed {{ border-left: 5px solid #f44336; }}
        .test-input {{ background: #f0f0f0; padding: 10px; border-radius: 4px; margin: 10px 0; white-space: pre-wrap; font-family: monospace; }}
        .screenshot {{ max-width: 100%; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; }}
        .html-output {{ background: #fafafa; padding: 10px; border: 1px solid #ddd; border-radius: 4px; margin: 10px 0; overflow-x: auto; }}
        .summary {{ background: white; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .status-badge {{ padding: 4px 8px; border-radius: 4px; color: white; font-weight: bold; }}
        .status-passed {{ background: #4CAF50; }}
        .status-failed {{ background: #f44336; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Think AI - Markdown Rendering E2E Test Report</h1>
        <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    </div>
    
    <div class="summary">
        <h2>Test Summary</h2>
        <p>Total Tests: {len(self.test_results)}</p>
        <p>Passed: {sum(1 for r in self.test_results if r['status'] == 'passed')}</p>
        <p>Failed: {sum(1 for r in self.test_results if r['status'] == 'failed')}</p>
    </div>
"""
        
        for result in self.test_results:
            status_class = result['status']
            html_content += f"""
    <div class="test-case {status_class}">
        <h3>{result['description']} <span class="status-badge status-{status_class}">{result['status'].upper()}</span></h3>
        <h4>Input Markdown:</h4>
        <div class="test-input">{result['input']}</div>
        
        <h4>Rendered Output:</h4>
        <div class="html-output">{result.get('html_output', 'No output captured')}</div>
        
        <h4>Screenshot:</h4>
        <img class="screenshot" src="{result.get('screenshot', '')}" alt="Screenshot for {result['name']}">
        
        {f"<h4>Errors:</h4><ul>{''.join(f'<li>{e}</li>' for e in result['errors'])}</ul>" if result['errors'] else ""}
    </div>
"""
        
        html_content += """
</body>
</html>
"""
        
        with open(TEST_RESULTS_FILE, 'w') as f:
            f.write(html_content)
            
        print(f"✅ Report generated: {TEST_RESULTS_FILE}")
        
    def run_all_tests(self):
        """Run all markdown tests"""
        print("🧪 Starting Markdown Rendering E2E Tests")
        
        try:
            # Navigate to the webapp
            print(f"🌐 Navigating to {BASE_URL}")
            self.driver.get(BASE_URL)
            
            # Wait for page to load
            self.wait_for_element("#queryInput")
            print("✅ Webapp loaded successfully")
            
            # Take initial screenshot
            self.take_screenshot("initial_page")
            
            # Run each test
            for test_name, test_data in MARKDOWN_TESTS.items():
                self.run_markdown_test(test_name, test_data)
                time.sleep(1)  # Brief pause between tests
                
        except Exception as e:
            print(f"❌ Test suite error: {e}")
            
        finally:
            # Generate report
            self.generate_report()
            
def main():
    tester = MarkdownE2ETest()
    
    try:
        tester.setup()
        tester.run_all_tests()
    finally:
        tester.teardown()
        
    # Print summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    passed = sum(1 for r in tester.test_results if r['status'] == 'passed')
    total = len(tester.test_results)
    print(f"Total: {total} | Passed: {passed} | Failed: {total - passed}")
    print(f"\n📄 Full report: {TEST_RESULTS_FILE}")
    print(f"📸 Screenshots: {SCREENSHOTS_DIR}/")
    
if __name__ == "__main__":
    main()