#!/usr/bin/env python3
"""
Complete test suite for deployed Think AI libraries
Tests all Python and JavaScript components
"""

import json
import subprocess
import sys
import os
import time
import asyncio
import datetime
from pathlib import Path

class DeploymentTester:
    def __init__(self):
        self.results = {
            "timestamp": datetime.datetime.now().isoformat(),
            "platform": sys.platform,
            "python_version": sys.version,
            "tests": {},
            "summary": {}
        }
        self.test_dir = Path(f"deployment_test_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}")
        self.test_dir.mkdir(exist_ok=True)
    
    def run_command(self, cmd, timeout=30):
        """Run a shell command and capture output"""
        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=timeout
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout[:1000],
                "stderr": result.stderr[:1000],
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Command timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def test_python_packages(self):
        """Test Python package installations"""
        print("\n🐍 Testing Python Packages...")
        print("=" * 50)
        
        # Create virtual environment for testing
        venv_path = self.test_dir / "test_venv"
        print(f"Creating virtual environment: {venv_path}")
        
        result = self.run_command(f"python -m venv {venv_path}")
        if not result["success"]:
            self.results["tests"]["python_venv"] = result
            return
        
        # Activate venv and install packages
        if sys.platform == "win32":
            pip_cmd = f"{venv_path}\\Scripts\\pip"
            python_cmd = f"{venv_path}\\Scripts\\python"
        else:
            pip_cmd = f"{venv_path}/bin/pip"
            python_cmd = f"{venv_path}/bin/python"
        
        # Install packages from built distributions
        packages = [
            ("think-ai-consciousness", "dist/think_ai_consciousness-2.1.0-py3-none-any.whl"),
            ("think-ai-cli", "think-ai-cli/python/dist/think_ai_cli-0.1.0-py3-none-any.whl"),
            ("o1-python", "o1-python/dist/o1_vector_search-1.0.0-py3-none-any.whl")
        ]
        
        for pkg_name, pkg_path in packages:
            print(f"\nInstalling {pkg_name}...")
            if os.path.exists(pkg_path):
                result = self.run_command(f"{pip_cmd} install {pkg_path}")
                self.results["tests"][f"install_{pkg_name}"] = result
            else:
                self.results["tests"][f"install_{pkg_name}"] = {
                    "success": False,
                    "error": f"Package file not found: {pkg_path}"
                }
        
        # Test imports and functionality
        test_script = self.test_dir / "test_imports.py"
        test_script.write_text('''
import sys
import json

results = {}

# Test imports
try:
    import think_ai
    results["import_think_ai"] = {"success": True, "version": getattr(think_ai, "__version__", "unknown")}
except Exception as e:
    results["import_think_ai"] = {"success": False, "error": str(e)}

try:
    import think_ai_cli
    results["import_think_ai_cli"] = {"success": True}
except Exception as e:
    results["import_think_ai_cli"] = {"success": False, "error": str(e)}

try:
    import o1_vector_search
    results["import_o1_vector_search"] = {"success": True}
except Exception as e:
    results["import_o1_vector_search"] = {"success": False, "error": str(e)}

# Test core functionality
try:
    from think_ai import ThinkAI
    ai = ThinkAI()
    response = ai.chat("Test message")
    results["think_ai_chat"] = {"success": True, "response_length": len(response)}
except Exception as e:
    results["think_ai_chat"] = {"success": False, "error": str(e)}

# Test vector search
try:
    from o1_vector_search import O1VectorSearch
    search = O1VectorSearch(dimensions=128)
    search.add("test1", [0.1] * 128, {"content": "Test 1"})
    results["o1_vector_search"] = {"success": True}
except Exception as e:
    results["o1_vector_search"] = {"success": False, "error": str(e)}

print(json.dumps(results))
''')
        
        print("\nTesting Python imports and functionality...")
        result = self.run_command(f"{python_cmd} {test_script}", timeout=60)
        
        if result["success"] and result["stdout"]:
            try:
                import_results = json.loads(result["stdout"])
                self.results["tests"]["python_functionality"] = import_results
            except:
                self.results["tests"]["python_functionality"] = result
        else:
            self.results["tests"]["python_functionality"] = result
    
    def test_javascript_packages(self):
        """Test JavaScript package installations"""
        print("\n🟨 Testing JavaScript Packages...")
        print("=" * 50)
        
        # Create test directory for JS
        js_test_dir = self.test_dir / "js_test"
        js_test_dir.mkdir(exist_ok=True)
        
        # Initialize npm project
        package_json = {
            "name": "think-ai-test",
            "version": "1.0.0",
            "description": "Test Think AI JS packages",
            "main": "index.js",
            "scripts": {
                "test": "node test.js"
            }
        }
        
        (js_test_dir / "package.json").write_text(json.dumps(package_json, indent=2))
        
        # Install packages
        packages = [
            ("think-ai-js", "../../npm/think-ai-js-2.0.1.tgz"),
            ("@think-ai/cli", "../../think-ai-cli/nodejs/think-ai-cli-0.2.0.tgz"),
            ("o1-js", "../../o1-js/o1-js-1.0.0.tgz")
        ]
        
        os.chdir(js_test_dir)
        
        for pkg_name, pkg_path in packages:
            print(f"\nInstalling {pkg_name}...")
            if os.path.exists(pkg_path):
                result = self.run_command(f"npm install {pkg_path}")
                self.results["tests"][f"npm_install_{pkg_name}"] = result
            else:
                # Try from npm registry
                result = self.run_command(f"npm install {pkg_name}")
                self.results["tests"][f"npm_install_{pkg_name}"] = result
        
        # Create test script
        test_script = '''
const results = {};

// Test imports
try {
    const { ThinkAI } = require('think-ai-js');
    results.import_think_ai_js = { success: true };
    
    // Test client creation
    const client = new ThinkAI({ apiUrl: 'http://localhost:8000' });
    results.client_creation = { success: true };
} catch (e) {
    results.import_think_ai_js = { success: false, error: e.message };
}

try {
    const o1js = require('o1-js');
    results.import_o1_js = { success: true };
} catch (e) {
    results.import_o1_js = { success: false, error: e.message };
}

console.log(JSON.stringify(results));
'''
        
        (js_test_dir / "test.js").write_text(test_script)
        
        print("\nTesting JavaScript imports and functionality...")
        result = self.run_command("node test.js")
        
        if result["success"] and result["stdout"]:
            try:
                js_results = json.loads(result["stdout"])
                self.results["tests"]["javascript_functionality"] = js_results
            except:
                self.results["tests"]["javascript_functionality"] = result
        else:
            self.results["tests"]["javascript_functionality"] = result
        
        os.chdir("../..")
    
    async def test_full_system(self):
        """Test the complete integrated system"""
        print("\n🚀 Testing Full System Integration...")
        print("=" * 50)
        
        # Start API server
        print("Starting API server...")
        server_process = subprocess.Popen(
            [sys.executable, "-m", "think_ai.api.server"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        await asyncio.sleep(5)
        
        try:
            # Test API endpoints
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                # Health check
                try:
                    async with session.get("http://localhost:8000/health") as resp:
                        self.results["tests"]["api_health"] = {
                            "success": resp.status == 200,
                            "status": resp.status
                        }
                except Exception as e:
                    self.results["tests"]["api_health"] = {
                        "success": False,
                        "error": str(e)
                    }
                
                # Chat endpoint
                try:
                    async with session.post(
                        "http://localhost:8000/chat",
                        json={"message": "Hello, Think AI!"}
                    ) as resp:
                        self.results["tests"]["api_chat"] = {
                            "success": resp.status == 200,
                            "status": resp.status
                        }
                except Exception as e:
                    self.results["tests"]["api_chat"] = {
                        "success": False,
                        "error": str(e)
                    }
        
        finally:
            # Stop server
            server_process.terminate()
            server_process.wait()
    
    def generate_report(self):
        """Generate comprehensive test report"""
        # Calculate summary
        total_tests = len(self.results["tests"])
        passed_tests = sum(
            1 for test in self.results["tests"].values()
            if test.get("success") or test.get("status") == "success"
        )
        
        self.results["summary"] = {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": total_tests - passed_tests,
            "success_rate": f"{(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "0%"
        }
        
        # Save JSON report
        report_path = self.test_dir / "deployment_test_report.json"
        report_path.write_text(json.dumps(self.results, indent=2))
        
        # Generate HTML report
        html_report = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Think AI Deployment Test Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 5px; }}
        .summary {{ background: #ecf0f1; padding: 15px; margin: 20px 0; border-radius: 5px; }}
        .test-result {{ margin: 10px 0; padding: 10px; border-radius: 3px; }}
        .success {{ background: #2ecc71; color: white; }}
        .failed {{ background: #e74c3c; color: white; }}
        .details {{ background: #f8f9fa; padding: 10px; margin-top: 5px; border-radius: 3px; }}
        pre {{ background: #2c3e50; color: #2ecc71; padding: 10px; overflow-x: auto; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Think AI Deployment Test Report</h1>
        <p>Generated: {self.results["timestamp"]}</p>
        <p>Platform: {self.results["platform"]} | Python: {self.results["python_version"].split()[0]}</p>
    </div>
    
    <div class="summary">
        <h2>Summary</h2>
        <p>Total Tests: {self.results["summary"]["total_tests"]}</p>
        <p>Passed: {self.results["summary"]["passed"]}</p>
        <p>Failed: {self.results["summary"]["failed"]}</p>
        <p>Success Rate: {self.results["summary"]["success_rate"]}</p>
    </div>
    
    <h2>Test Results</h2>
'''
        
        for test_name, result in self.results["tests"].items():
            status = "success" if result.get("success") or result.get("status") == "success" else "failed"
            html_report += f'''
    <div class="test-result {status}">
        <h3>{test_name.replace("_", " ").title()}</h3>
        <div class="details">
            <pre>{json.dumps(result, indent=2)}</pre>
        </div>
    </div>
'''
        
        html_report += '''
</body>
</html>
'''
        
        html_path = self.test_dir / "deployment_test_report.html"
        html_path.write_text(html_report)
        
        print(f"\n📊 Test Report Generated:")
        print(f"   JSON: {report_path}")
        print(f"   HTML: {html_path}")
        
        return self.results["summary"]
    
    async def run_all_tests(self):
        """Run all deployment tests"""
        print("🧪 Think AI Deployment Testing Suite")
        print("===================================")
        
        # Test Python packages
        self.test_python_packages()
        
        # Test JavaScript packages
        self.test_javascript_packages()
        
        # Test full system
        await self.test_full_system()
        
        # Generate report
        summary = self.generate_report()
        
        print("\n" + "=" * 50)
        print("✅ Testing Complete!")
        print(f"   Total Tests: {summary['total_tests']}")
        print(f"   Passed: {summary['passed']}")
        print(f"   Failed: {summary['failed']}")
        print(f"   Success Rate: {summary['success_rate']}")
        print("=" * 50)

if __name__ == "__main__":
    tester = DeploymentTester()
    asyncio.run(tester.run_all_tests())