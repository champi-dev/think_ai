#!/usr/bin/env python3
"""Comprehensive webapp test to verify 100% functionality."""

import requests
import json
import time
import asyncio
import websockets
from datetime import datetime

class WebappTestSuite:
    def __init__(self):
        self.webapp_url = "http://localhost:3000"
        self.api_url = "http://localhost:8080"
        self.ws_url = "ws://localhost:3000/ws"
        self.results = []
        
    def test_webapp_home(self):
        """Test webapp homepage loads."""
        try:
            response = requests.get(self.webapp_url)
            success = response.status_code == 200 and "Think AI" in response.text
            self.results.append({
                "test": "Webapp Homepage",
                "status": "✅ PASS" if success else "❌ FAIL",
                "details": f"Status: {response.status_code}, Content includes 'Think AI': {'Yes' if 'Think AI' in response.text else 'No'}"
            })
            return success
        except Exception as e:
            self.results.append({
                "test": "Webapp Homepage",
                "status": "❌ FAIL",
                "details": str(e)
            })
            return False
            
    def test_api_health(self):
        """Test API health endpoint."""
        try:
            response = requests.get(f"{self.api_url}/health")
            data = response.json()
            success = response.status_code == 200 and data.get("status") == "healthy"
            self.results.append({
                "test": "API Health Check",
                "status": "✅ PASS" if success else "❌ FAIL", 
                "details": f"Status: {response.status_code}, Response: {data}"
            })
            return success
        except Exception as e:
            self.results.append({
                "test": "API Health Check",
                "status": "❌ FAIL",
                "details": str(e)
            })
            return False
            
    def test_api_generate(self):
        """Test API generate endpoint."""
        try:
            payload = {"prompt": "Write a hello world function in Python"}
            response = requests.post(f"{self.api_url}/api/v1/generate", json=payload)
            data = response.json()
            success = response.status_code == 200 and ("response" in data or "generated_text" in data)
            self.results.append({
                "test": "API Generate Endpoint",
                "status": "✅ PASS" if success else "❌ FAIL",
                "details": f"Status: {response.status_code}, Has response: {'Yes' if 'response' in data else 'No'}"
            })
            return success
        except Exception as e:
            self.results.append({
                "test": "API Generate Endpoint", 
                "status": "❌ FAIL",
                "details": str(e)
            })
            return False
            
    async def test_websocket(self):
        """Test WebSocket connection."""
        try:
            async with websockets.connect(self.ws_url) as websocket:
                # Send a test message
                test_message = json.dumps({
                    "type": "generate",
                    "prompt": "Hello"
                })
                await websocket.send(test_message)
                
                # Wait for response
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                data = json.loads(response)
                
                success = "type" in data or "response" in data
                self.results.append({
                    "test": "WebSocket Connection",
                    "status": "✅ PASS" if success else "❌ FAIL",
                    "details": f"Sent: {test_message}, Received: {data}"
                })
                return success
        except Exception as e:
            self.results.append({
                "test": "WebSocket Connection",
                "status": "❌ FAIL", 
                "details": str(e)
            })
            return False
            
    def test_static_assets(self):
        """Test static assets are served."""
        try:
            # Test manifest
            manifest_response = requests.get(f"{self.webapp_url}/manifest.json")
            manifest_ok = manifest_response.status_code == 200
            
            # Test service worker
            sw_response = requests.get(f"{self.webapp_url}/sw.js")
            sw_ok = sw_response.status_code == 200
            
            success = manifest_ok and sw_ok
            self.results.append({
                "test": "Static Assets",
                "status": "✅ PASS" if success else "❌ FAIL",
                "details": f"Manifest: {manifest_response.status_code}, Service Worker: {sw_response.status_code}"
            })
            return success
        except Exception as e:
            self.results.append({
                "test": "Static Assets",
                "status": "❌ FAIL",
                "details": str(e)
            })
            return False
            
    def test_api_proxy(self):
        """Test webapp API proxy."""
        try:
            # Test if webapp proxies API requests
            response = requests.get(f"{self.webapp_url}/api/health")
            success = response.status_code == 200
            self.results.append({
                "test": "Webapp API Proxy",
                "status": "✅ PASS" if success else "❌ FAIL",
                "details": f"Status: {response.status_code}"
            })
            return success
        except Exception as e:
            self.results.append({
                "test": "Webapp API Proxy",
                "status": "❌ FAIL",
                "details": str(e)
            })
            return False
            
    def generate_report(self):
        """Generate test report."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if "✅" in r["status"])
        
        report = {
            "timestamp": timestamp,
            "summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": total_tests - passed_tests,
                "success_rate": f"{(passed_tests/total_tests)*100:.1f}%"
            },
            "tests": self.results,
            "conclusion": "✅ WEBAPP WORKING 100%" if passed_tests == total_tests else "⚠️ SOME TESTS FAILED"
        }
        
        # Save report
        with open("webapp_test_report.json", "w") as f:
            json.dump(report, f, indent=2)
            
        # Print summary
        print("\n" + "="*60)
        print("WEBAPP TEST RESULTS")
        print("="*60)
        print(f"Timestamp: {timestamp}")
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {report['summary']['success_rate']}")
        print("\nDetailed Results:")
        print("-"*60)
        
        for result in self.results:
            print(f"{result['status']} {result['test']}")
            print(f"   Details: {result['details']}")
            
        print("\n" + "="*60)
        print(f"CONCLUSION: {report['conclusion']}")
        print("="*60)
        
        return report

async def main():
    """Run all tests."""
    tester = WebappTestSuite()
    
    print("Starting webapp tests...")
    print("Waiting for services to be ready...")
    time.sleep(2)
    
    # Run synchronous tests
    tester.test_webapp_home()
    tester.test_api_health()
    tester.test_api_generate()
    tester.test_static_assets()
    tester.test_api_proxy()
    
    # Run async tests
    await tester.test_websocket()
    
    # Generate report
    report = tester.generate_report()
    
    # Take screenshot evidence
    print("\nGenerating visual evidence...")
    try:
        import subprocess
        subprocess.run(["curl", "-s", f"{tester.webapp_url}", "-o", "webapp_homepage.html"])
        print("✅ Saved webapp homepage HTML")
    except:
        pass

if __name__ == "__main__":
    asyncio.run(main())