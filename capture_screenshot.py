#!/usr/bin/env python3
import time
import subprocess
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

def capture_markdown_test():
    # Setup Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1280,1024")
    
    # Create webdriver
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Navigate to chat interface
        print("Opening chat interface...")
        driver.get("http://localhost:3456/static/chat.html")
        
        # Wait for page to load
        wait = WebDriverWait(driver, 10)
        message_input = wait.until(EC.presence_of_element_located((By.ID, "messageInput")))
        
        # Send test message with markdown
        test_message = """Here are some Python examples:

# Simple Calculator
A basic calculator with **arithmetic operations**.

```python
def simple_calculator():
    print("Simple Calculator")
    num1 = float(input("Enter first number: "))
    operator = input("Enter operator (+, -, *, /): ")
    num2 = float(input("Enter second number: "))
    
    if operator == '+':
        result = num1 + num2
    elif operator == '-':
        result = num1 - num2
    else:
        result = "Invalid"
    
    print(f"Result: {result}")
```

## Features:
- Easy to use interface
- Support for *basic operations*
- Error handling for division by zero

1. Enter first number
2. Choose operator
3. Enter second number"""
        
        print("Sending test message...")
        message_input.send_keys(test_message)
        
        # Click send button
        send_button = driver.find_element(By.ID, "sendButton")
        send_button.click()
        
        # Wait for response
        print("Waiting for response...")
        time.sleep(5)
        
        # Take screenshot
        screenshot_path = "/home/administrator/think_ai/markdown_test_screenshot.png"
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to: {screenshot_path}")
        
        # Also capture the page source for debugging
        with open("/home/administrator/think_ai/markdown_test_page.html", "w") as f:
            f.write(driver.page_source)
        print("Page source saved for debugging")
        
        return screenshot_path
        
    except Exception as e:
        print(f"Error during screenshot capture: {e}")
        # Try to save error screenshot
        try:
            driver.save_screenshot("/home/administrator/think_ai/error_screenshot.png")
        except:
            pass
        raise
    finally:
        driver.quit()

if __name__ == "__main__":
    # Check if server is running
    try:
        import requests
        response = requests.get("http://localhost:3456/health", timeout=5)
        if response.status_code != 200:
            print("Server not healthy!")
            exit(1)
    except:
        print("Server not running on port 3456!")
        exit(1)
    
    # Capture screenshot
    capture_markdown_test()