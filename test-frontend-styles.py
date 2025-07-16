#!/usr/bin/env python3
import sys
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def test_frontend_styles():
    # Setup Edge with headless options
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Edge(options=options)

    try:
        print("Testing https://thinkai.lat/...")
        driver.get("https://thinkai.lat/")

        # Wait for page load
        time.sleep(3)

        # Check if root element exists
        root = driver.find_element(By.ID, "root")
        print(f"✓ Root element found")

        # Check computed styles on body
        body = driver.find_element(By.TAG_NAME, "body")
        bg_color = driver.execute_script(
            "return window.getComputedStyle(arguments[0]).backgroundColor", body
        )
        font_family = driver.execute_script(
            "return window.getComputedStyle(arguments[0]).fontFamily", body
        )
        color = driver.execute_script(
            "return window.getComputedStyle(arguments[0]).color", body
        )

        print(f"\nComputed styles on body:")
        print(f"  Background color: {bg_color}")
        print(f"  Font family: {font_family}")
        print(f"  Text color: {color}")

        # Check if styles are applied (not default)
        if "Inter" in font_family or "sans-serif" in font_family:
            print("✓ Custom fonts are loaded")
        else:
            print("✗ Custom fonts NOT loaded")

        # Check for any React content
        root_html = root.get_attribute("innerHTML")
        if root_html and len(root_html) > 0:
            print(f"✓ React app rendered (content length: {len(root_html)})")
        else:
            print("✗ React app NOT rendered")

        # Check for console errors
        logs = driver.get_logs("browser")
        if logs:
            print("\nConsole logs:")
            for log in logs:
                print(f"  {log['level']}: {log['message']}")
        else:
            print("\n✓ No console errors")

        # Take screenshot
        driver.save_screenshot("/home/administrator/think_ai/frontend-test.png")
        print("\nScreenshot saved to frontend-test.png")

    finally:
        driver.quit()


if __name__ == "__main__":
    test_frontend_styles()
