#!/usr/bin/env python3
"""Test markdown rendering issues on production site"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os

# Test cases for markdown rendering
test_messages = [
    # Test 1: Line breaks issue
    "This is line 1\nThis is line 2\nThis is line 3",
    # Test 2: Paragraphs with double newlines
    "Paragraph 1 here.\n\nParagraph 2 here.\n\nParagraph 3 here.",
    # Test 3: Mixed markdown elements
    """# Heading 1
This is a paragraph with **bold** and *italic* text.

## Heading 2
- List item 1
- List item 2
- List item 3

This is inline `code` and below is a code block:

```python
def hello():
    print("Hello, World!")
```

> This is a blockquote
> with multiple lines

Final paragraph with a [link](https://example.com).""",
    # Test 4: Edge cases
    "Single line",
    "Line with trailing newline\n",
    "\n\nStarting with newlines",
]


def setup_driver():
    """Setup Chrome driver with options"""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    # Comment out headless for debugging
    # chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    return driver


def test_site(url, site_name):
    """Test markdown rendering on a site"""
    print(f"\n{'='*60}")
    print(f"Testing {site_name}: {url}")
    print("=" * 60)

    driver = setup_driver()

    try:
        # Navigate to site
        print(f"1. Navigating to {url}...")
        driver.get(url)
        time.sleep(3)  # Wait for initial load

        # Take screenshot of initial state
        screenshot_path = f"/tmp/{site_name}_initial.png"
        driver.save_screenshot(screenshot_path)
        print(f"   ✓ Initial screenshot saved: {screenshot_path}")

        # Find chat input
        wait = WebDriverWait(driver, 10)
        chat_input = wait.until(EC.presence_of_element_located((By.ID, "chatInput")))
        send_button = driver.find_element(By.ID, "sendBtn")

        print("\n2. Testing markdown rendering...")

        for i, test_msg in enumerate(test_messages):
            print(f"\n   Test {i+1}: {test_msg[:30]}...")

            # Clear and send message
            chat_input.clear()
            chat_input.send_keys(test_msg)
            send_button.click()

            # Wait for response
            time.sleep(2)

            # Take screenshot
            screenshot_path = f"/tmp/{site_name}_test{i+1}.png"
            driver.save_screenshot(screenshot_path)
            print(f"   ✓ Screenshot saved: {screenshot_path}")

            # Get the last user message element
            user_messages = driver.find_elements(By.CSS_SELECTOR, ".message.user")
            if user_messages:
                last_user_msg = user_messages[-1]
                rendered_html = last_user_msg.get_attribute("innerHTML")
                print(f"   User message HTML: {rendered_html[:100]}...")

        # Check default bot message spacing
        print("\n3. Checking default bot message...")
        bot_messages = driver.find_elements(By.CSS_SELECTOR, ".message.ai")
        if bot_messages:
            first_bot_msg = bot_messages[0]
            bot_html = first_bot_msg.get_attribute("innerHTML")
            bot_text = first_bot_msg.text
            print(f"   Bot message HTML: {bot_html[:200]}...")
            print(f"   Bot message text: {bot_text[:100]}...")

            # Check for spacing issues
            if "  " in bot_text or bot_text.startswith(" ") or bot_text.endswith(" "):
                print("   ⚠️  WARNING: Spacing issues detected in bot message!")

        # Final screenshot
        time.sleep(1)
        final_screenshot = f"/tmp/{site_name}_final.png"
        driver.save_screenshot(final_screenshot)
        print(f"\n✓ Final screenshot: {final_screenshot}")

    except Exception as e:
        print(f"\n❌ Error testing {site_name}: {str(e)}")
        error_screenshot = f"/tmp/{site_name}_error.png"
        driver.save_screenshot(error_screenshot)
        print(f"   Error screenshot: {error_screenshot}")

    finally:
        driver.quit()


def main():
    """Main test runner"""
    print("Starting markdown rendering tests...")

    # Test production
    test_site("https://thinkai.lat", "production")

    # Test local if running
    print("\n" + "=" * 60)
    print(
        "Would you like to test local server too? (Make sure it's running on port 8888)"
    )
    response = input("Test local? (y/n): ").lower()
    if response == "y":
        test_site("http://localhost:8888", "local")

    print("\n" + "=" * 60)
    print("Test complete! Check screenshots in /tmp/")
    print("Screenshots generated:")
    os.system("ls -la /tmp/*.png | grep -E '(production|local)_'")


if __name__ == "__main__":
    main()
