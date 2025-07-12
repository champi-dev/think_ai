#!/usr/bin/env python3
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def test_frontend():
    # Setup Chrome in headless mode
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        print("Testing https://thinkai.lat...")
        driver.get("https://thinkai.lat")
        
        # Wait for page to load
        time.sleep(3)
        
        # Find input field and send button
        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "queryInput"))
        )
        send_button = driver.find_element(By.ID, "sendBtn")
        
        # Type a message
        input_field.send_keys("Hello, test message")
        driver.save_screenshot("/tmp/before_send.png")
        print("✓ Screenshot saved: /tmp/before_send.png")
        
        # Click send
        send_button.click()
        
        # Wait for response
        print("Waiting for response...")
        time.sleep(5)
        
        # Check if thinking message appears
        try:
            thinking = driver.find_element(By.CLASS_NAME, "loading-message")
            print("✓ Found 'Thinking...' message")
        except:
            print("✗ No 'Thinking...' message found")
        
        # Wait more for response
        time.sleep(10)
        
        # Take screenshot after response
        driver.save_screenshot("/tmp/after_send.png")
        print("✓ Screenshot saved: /tmp/after_send.png")
        
        # Check for AI response
        try:
            ai_messages = driver.find_elements(By.CSS_SELECTOR, ".message.ai")
            if ai_messages:
                print(f"✓ Found {len(ai_messages)} AI response(s)")
                for i, msg in enumerate(ai_messages):
                    content = msg.find_element(By.CLASS_NAME, "message-content").text
                    print(f"  Response {i+1}: {content[:100]}...")
            else:
                print("✗ No AI responses found")
        except Exception as e:
            print(f"✗ Error checking responses: {e}")
        
        # Check console for errors
        logs = driver.get_log('browser')
        errors = [log for log in logs if log['level'] == 'SEVERE']
        if errors:
            print(f"✗ Found {len(errors)} browser errors:")
            for error in errors:
                print(f"  - {error['message']}")
        else:
            print("✓ No browser errors")
            
    finally:
        driver.quit()

if __name__ == "__main__":
    test_frontend()