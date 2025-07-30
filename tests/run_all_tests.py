#!/usr/bin/env python3
"""
Main test runner for Think AI
Runs all unit, integration, and e2e tests with proper configuration
"""

import asyncio
import subprocess
import sys
import os
import json
import time
from pathlib import Path
from typing import Dict, List, Any
from test_config import get_config


class TestRunner:
    def __init__(self):
        self.config = get_config()
        self.results = {
            "unit_tests": {},
            "integration_tests": {},
            "e2e_tests": {},
            "summary": {}
        }
        self.start_time = time.time()
    
    def run_rust_tests(self) -> Dict[str, Any]:
        """Run Rust unit and integration tests"""
        print("\n🦀 Running Rust tests...")
        
        test_results = {}
        
        # Run unit tests
        print("  Running unit tests...")
        result = subprocess.run(
            ["cargo", "test", "--lib", "--", "--nocapture"],
            cwd="/home/administrator/think_ai",
            capture_output=True,
            text=True
        )
        
        test_results["unit"] = {
            "success": result.returncode == 0,
            "output": result.stdout,
            "errors": result.stderr
        }
        
        # Run integration tests
        print("  Running integration tests...")
        result = subprocess.run(
            ["cargo", "test", "--test", "*", "--", "--nocapture"],
            cwd="/home/administrator/think_ai",
            capture_output=True,
            text=True
        )
        
        test_results["integration"] = {
            "success": result.returncode == 0,
            "output": result.stdout,
            "errors": result.stderr
        }
        
        return test_results
    
    async def run_python_unit_tests(self) -> Dict[str, Any]:
        """Run Python unit tests"""
        print("\n🐍 Running Python unit tests...")
        
        # Use pytest to run unit tests
        result = subprocess.run(
            ["python", "-m", "pytest", "tests/unit/", "-v", "--json-report", "--json-report-file=unit_test_results.json"],
            cwd="/home/administrator/think_ai",
            capture_output=True,
            text=True
        )
        
        # Load test results if available
        results_file = Path("/home/administrator/think_ai/unit_test_results.json")
        if results_file.exists():
            with open(results_file, 'r') as f:
                return json.load(f)
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "errors": result.stderr
        }
    
    async def run_integration_tests(self) -> Dict[str, Any]:
        """Run integration tests"""
        print("\n🔗 Running integration tests...")
        
        # Import and run integration tests
        sys.path.insert(0, str(Path(__file__).parent))
        from integration.test_api_integration import run_integration_tests
        
        results = await run_integration_tests()
        
        return {
            "success": all(r[1] == "PASSED" for r in results),
            "tests": results
        }
    
    async def run_e2e_tests(self) -> Dict[str, Any]:
        """Run E2E tests"""
        print("\n🎯 Running E2E tests...")
        
        # Import and run E2E tests
        from e2e.test_full_system_e2e import ThinkAIE2ETestSuite
        
        suite = ThinkAIE2ETestSuite()
        success = await suite.run_all_tests()
        
        return {
            "success": success,
            "results": suite.test_results
        }
    
    def run_frontend_tests(self) -> Dict[str, Any]:
        """Run frontend tests"""
        print("\n⚛️  Running frontend tests...")
        
        # Check if frontend directory exists
        frontend_dir = Path("/home/administrator/think_ai/frontend")
        if not frontend_dir.exists():
            return {"success": True, "skipped": True, "reason": "Frontend directory not found"}
        
        # Install dependencies if needed
        if not (frontend_dir / "node_modules").exists():
            print("  Installing frontend dependencies...")
            subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
        
        # Run tests
        result = subprocess.run(
            ["npm", "test", "--", "--watchAll=false"],
            cwd=frontend_dir,
            capture_output=True,
            text=True
        )
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "errors": result.stderr
        }
    
    def generate_report(self):
        """Generate comprehensive test report"""
        end_time = time.time()
        duration = end_time - self.start_time
        
        # Calculate summary
        total_success = all([
            self.results.get("unit_tests", {}).get("success", True),
            self.results.get("integration_tests", {}).get("success", True),
            self.results.get("e2e_tests", {}).get("success", True),
            self.results.get("frontend_tests", {}).get("success", True),
            self.results.get("rust_tests", {}).get("unit", {}).get("success", True),
            self.results.get("rust_tests", {}).get("integration", {}).get("success", True),
        ])
        
        self.results["summary"] = {
            "success": total_success,
            "duration_seconds": duration,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "config": {
                "api_url": self.config.api_base_url,
                "headless": self.config.is_headless,
                "mock_llm": self.config.should_mock_llm
            }
        }
        
        # Save report
        report_path = self.config.save_test_results(self.results)
        
        # Print summary
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        print(f"Overall Status: {'✅ PASSED' if total_success else '❌ FAILED'}")
        print(f"Duration: {duration:.2f} seconds")
        print(f"Report saved to: {report_path}")
        
        # Print individual results
        print("\nTest Categories:")
        categories = [
            ("Rust Unit Tests", self.results.get("rust_tests", {}).get("unit", {}).get("success")),
            ("Rust Integration Tests", self.results.get("rust_tests", {}).get("integration", {}).get("success")),
            ("Python Unit Tests", self.results.get("unit_tests", {}).get("success")),
            ("Integration Tests", self.results.get("integration_tests", {}).get("success")),
            ("E2E Tests", self.results.get("e2e_tests", {}).get("success")),
            ("Frontend Tests", self.results.get("frontend_tests", {}).get("success")),
        ]
        
        for name, success in categories:
            if success is None:
                status = "⏭️  SKIPPED"
            elif success:
                status = "✅ PASSED"
            else:
                status = "❌ FAILED"
            print(f"  {name}: {status}")
        
        print("="*60)
        
        return total_success
    
    async def run_all(self):
        """Run all tests"""
        print("🚀 Starting Think AI Test Suite")
        print(f"Configuration: {self.config.config_path}")
        
        # Run tests in order
        self.results["rust_tests"] = self.run_rust_tests()
        self.results["unit_tests"] = await self.run_python_unit_tests()
        self.results["frontend_tests"] = self.run_frontend_tests()
        self.results["integration_tests"] = await self.run_integration_tests()
        self.results["e2e_tests"] = await self.run_e2e_tests()
        
        # Generate report
        success = self.generate_report()
        
        return success


async def main():
    """Main entry point"""
    runner = TestRunner()
    success = await runner.run_all()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())