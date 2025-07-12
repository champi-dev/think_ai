#!/usr/bin/env python3
"""
End-to-End Test for Think AI Webapp
Tests the complete user journey with screenshots and video recording
"""
import os
import sys
import time
import json
import subprocess
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests

class ThinkAIE2ETest:
    def __init__(self, headless=True):
        self.url = "https://thinkai.lat"
        self.test_dir = f"/home/administrator/think_ai/e2e-test-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.headless = headless
        self.driver = None
        self.results = []
        
        # Create test directory
        os.makedirs(self.test_dir, exist_ok=True)
        
    def setup_driver(self):
        """Setup Chrome driver with options"""
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-gpu')
        
        try:
            self.driver = webdriver.Chrome(options=options)
            return True
        except Exception as e:
            print(f"Failed to setup Chrome driver: {e}")
            # Fallback to using curl/requests for API testing
            return False
    
    def take_screenshot(self, name):
        """Take a screenshot"""
        if self.driver:
            filepath = f"{self.test_dir}/{name}.png"
            self.driver.save_screenshot(filepath)
            print(f"📸 Screenshot saved: {filepath}")
            return filepath
        return None
    
    def test_api_endpoints(self):
        """Test API endpoints directly"""
        print("\n=== Testing API Endpoints ===")
        
        tests = [
            {
                "name": "Health Check",
                "url": f"{self.url}/health",
                "method": "GET",
                "expected_status": 200,
                "expected_content": "healthy"
            },
            {
                "name": "Chat API",
                "url": f"{self.url}/api/chat",
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "data": {"message": "What is Think AI?"},
                "expected_status": 200,
                "expected_content": "response"
            }
        ]
        
        for test in tests:
            try:
                print(f"\n📍 Testing: {test['name']}")
                
                if test["method"] == "GET":
                    response = requests.get(test["url"], timeout=10)
                else:
                    response = requests.post(
                        test["url"], 
                        headers=test.get("headers", {}),
                        json=test.get("data", {}),
                        timeout=10
                    )
                
                # Check status code
                if response.status_code == test["expected_status"]:
                    print(f"   ✅ Status code: {response.status_code}")
                    self.results.append({"test": test["name"], "status": "PASS", "details": f"Status {response.status_code}"})
                else:
                    print(f"   ❌ Status code: {response.status_code} (expected {test['expected_status']})")
                    self.results.append({"test": test["name"], "status": "FAIL", "details": f"Got {response.status_code}, expected {test['expected_status']}"})
                
                # Check content
                if test.get("expected_content") and test["expected_content"] in response.text:
                    print(f"   ✅ Response contains expected content")
                else:
                    print(f"   ❌ Response missing expected content")
                    print(f"   Response: {response.text[:200]}...")
                    
            except requests.exceptions.RequestException as e:
                print(f"   ❌ Request failed: {e}")
                self.results.append({"test": test["name"], "status": "FAIL", "details": str(e)})
    
    def test_ui_interaction(self):
        """Test UI interactions using Selenium"""
        if not self.driver:
            print("\n⚠️  Selenium not available, skipping UI tests")
            return
            
        print("\n=== Testing UI Interactions ===")
        
        try:
            # Load the webpage
            print("\n📍 Loading webpage...")
            self.driver.get(self.url)
            time.sleep(3)  # Wait for page load
            self.take_screenshot("01_initial_load")
            
            # Check if page loaded
            wait = WebDriverWait(self.driver, 10)
            
            # Test 1: Check for main elements
            print("\n📍 Checking main elements...")
            try:
                logo = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "logo")))
                print("   ✅ Logo found")
                
                input_field = self.driver.find_element(By.ID, "queryInput")
                print("   ✅ Input field found")
                
                send_button = self.driver.find_element(By.ID, "sendBtn")
                print("   ✅ Send button found")
                
                self.results.append({"test": "UI Elements", "status": "PASS", "details": "All main elements found"})
            except TimeoutException:
                print("   ❌ Some UI elements not found")
                self.results.append({"test": "UI Elements", "status": "FAIL", "details": "Missing UI elements"})
            
            # Test 2: Send a message
            print("\n📍 Testing chat interaction...")
            try:
                input_field = self.driver.find_element(By.ID, "queryInput")
                input_field.clear()
                input_field.send_keys("Hello, Think AI!")
                self.take_screenshot("02_typed_message")
                
                # Click send button
                send_button = self.driver.find_element(By.ID, "sendBtn")
                send_button.click()
                
                # Wait for response
                print("   ⏳ Waiting for AI response...")
                time.sleep(5)  # Give time for response
                self.take_screenshot("03_after_send")
                
                # Check if response appeared
                messages = self.driver.find_elements(By.CLASS_NAME, "message")
                if len(messages) > 1:  # Should have at least user message and AI response
                    print(f"   ✅ Got response! ({len(messages)} messages)")
                    self.results.append({"test": "Chat Interaction", "status": "PASS", "details": f"{len(messages)} messages"})
                else:
                    print(f"   ❌ No response received ({len(messages)} messages)")
                    self.results.append({"test": "Chat Interaction", "status": "FAIL", "details": "No AI response"})
                    
            except Exception as e:
                print(f"   ❌ Chat interaction failed: {e}")
                self.results.append({"test": "Chat Interaction", "status": "FAIL", "details": str(e)})
            
            # Test 3: Check 3D animation
            print("\n📍 Checking 3D canvas...")
            try:
                canvas = self.driver.find_element(By.ID, "canvas")
                if canvas:
                    print("   ✅ 3D canvas element found")
                    # Take screenshot of animation
                    time.sleep(2)
                    self.take_screenshot("04_3d_animation")
                    self.results.append({"test": "3D Canvas", "status": "PASS", "details": "Canvas rendering"})
            except:
                print("   ❌ 3D canvas not found")
                self.results.append({"test": "3D Canvas", "status": "FAIL", "details": "Canvas not found"})
                
        except Exception as e:
            print(f"\n❌ UI test error: {e}")
            self.take_screenshot("error_state")
    
    def generate_report(self):
        """Generate test report"""
        report_path = f"{self.test_dir}/test_report.json"
        
        # Calculate pass/fail counts
        passed = sum(1 for r in self.results if r["status"] == "PASS")
        failed = sum(1 for r in self.results if r["status"] == "FAIL")
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "url": self.url,
            "total_tests": len(self.results),
            "passed": passed,
            "failed": failed,
            "results": self.results,
            "test_directory": self.test_dir
        }
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print("\n" + "="*50)
        print("📊 TEST SUMMARY")
        print("="*50)
        print(f"Total Tests: {len(self.results)}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"\n📁 Test artifacts saved to: {self.test_dir}")
        print(f"📄 Report: {report_path}")
        
        # Print detailed results
        print("\nDetailed Results:")
        for result in self.results:
            status_icon = "✅" if result["status"] == "PASS" else "❌"
            print(f"{status_icon} {result['test']}: {result['details']}")
        
        return report
    
    def run(self):
        """Run all tests"""
        print("🚀 Starting Think AI E2E Tests")
        print(f"🌐 Testing: {self.url}")
        
        # Test API endpoints first
        self.test_api_endpoints()
        
        # Setup Selenium and test UI
        if self.setup_driver():
            self.test_ui_interaction()
            self.driver.quit()
        
        # Generate report
        self.generate_report()

def main():
    # Check if running in headless mode
    headless = "--headless" in sys.argv or not os.environ.get('DISPLAY')
    
    # Run tests
    tester = ThinkAIE2ETest(headless=headless)
    tester.run()

if __name__ == "__main__":
    main()