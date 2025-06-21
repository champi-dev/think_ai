#!/usr/bin/env python3
"""
Think AI FULL System Test Suite
Complete testing of ALL functionalities with comprehensive evidence
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import traceback
from datetime import datetime
from pathlib import Path


class FullSystemTester:
    """Complete system testing with full evidence."""

    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests": [],
            "summary": {"total": 0, "passed": 0, "failed": 0, "errors": []},
        }
        self.evidence_dir = Path("FULL_TEST_EVIDENCE") / datetime.now().strftime("%Y%m%d_%H%M%S")
        self.evidence_dir.mkdir(parents=True, exist_ok=True)

    def log_test(self, category, name, passed, details, evidence=None):
        """Log test result with evidence."""
        test_result = {
            "category": category,
            "name": name,
            "passed": passed,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "evidence": evidence or {},
        }
        self.results["tests"].append(test_result)
        self.results["summary"]["total"] += 1
        if passed:
            self.results["summary"]["passed"] += 1
        else:
            self.results["summary"]["failed"] += 1

        # Save evidence file
        evidence_file = self.evidence_dir / f"{category}_{name}.json"
        with open(evidence_file, "w") as f:
            json.dump(test_result, f, indent=2)

        # Print live status
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} | {category} :: {name}")
        if not passed:
            print(f"   └─ {details}")

    def run_command(self, cmd, cwd=None, env=None):
        """Run command and capture output."""
        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=60, cwd=cwd, env=env or os.environ.copy()
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "command": cmd,
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "stdout": "", "stderr": "Command timed out", "returncode": -1, "command": cmd}
        except Exception as e:
            return {"success": False, "stdout": "", "stderr": str(e), "returncode": -1, "command": cmd}

    def test_python_environment(self):
        """Test Python environment setup."""
        print("\n🔍 TESTING PYTHON ENVIRONMENT")
        print("=" * 50)

        # Check Python version
        result = self.run_command("python3 --version")
        self.log_test("Environment", "python_version", result["success"], result["stdout"].strip(), result)

        # Check pip
        result = self.run_command("python3 -m pip --version")
        self.log_test("Environment", "pip_available", result["success"], result["stdout"].strip(), result)

        # List installed packages
        result = self.run_command("python3 -m pip list")
        if result["success"]:
            packages_file = self.evidence_dir / "installed_packages.txt"
            packages_file.write_text(result["stdout"])

        self.log_test(
            "Environment",
            "packages_list",
            result["success"],
            f"Listed {len(result['stdout'].splitlines())} packages",
            {"packages_saved": str(packages_file) if result["success"] else None},
        )

    def test_think_ai_installation(self):
        """Test Think AI package installation."""
        print("\n🔍 TESTING THINK AI INSTALLATION")
        print("=" * 50)

        # Try importing think_ai
        test_code = """
import sys
try:
    import think_ai
    print(f"SUCCESS: think_ai version {getattr(think_ai, '__version__', 'unknown')}")
    sys.exit(0)
except ImportError as e:
    print(f"FAILED: {e}")
    sys.exit(1)
"""
        result = self.run_command(f'python3 -c "{test_code}"')
        self.log_test("Installation", "think_ai_import", result["success"], result["stdout"].strip(), result)

        # Check Think AI CLI installation
        cli_paths = ["think-ai-cli/python", "./think-ai-cli/python", Path.cwd() / "think-ai-cli" / "python"]

        cli_installed = False
        for path in cli_paths:
            if Path(path).exists():
                result = self.run_command("python3 -m pip install -e .", cwd=str(path))
                if result["success"]:
                    cli_installed = True
                    break

        self.log_test(
            "Installation",
            "think_ai_cli_install",
            cli_installed,
            "Think AI CLI installed successfully" if cli_installed else "Failed to install CLI",
            result if "result" in locals() else None,
        )

    def test_think_ai_cli_commands(self):
        """Test all Think AI CLI commands."""
        print("\n🔍 TESTING THINK AI CLI COMMANDS")
        print("=" * 50)

        # Create a temporary home for testing
        with tempfile.TemporaryDirectory() as temp_home:
            env = os.environ.copy()
            env["HOME"] = temp_home

            # Test help command
            result = self.run_command("python3 -m think_ai_cli --help")
            self.log_test(
                "CLI_Commands",
                "help_main",
                result["success"] and "Think AI" in result["stdout"],
                "Main help displayed",
                result,
            )

            # Test version
            result = self.run_command("python3 -m think_ai_cli --version")
            self.log_test("CLI_Commands", "version", result["success"], result["stdout"].strip(), result)

            # Test add command
            result = self.run_command(
                'python3 -m think_ai_cli add --code "def test(): pass" --language python --description "Test function"',
                env=env,
            )
            self.log_test(
                "CLI_Commands",
                "add_code",
                result["success"] and "Added successfully" in result["stdout"],
                "Code snippet added",
                result,
            )

            # Test search command
            result = self.run_command('python3 -m think_ai_cli search "test function"', env=env)
            self.log_test("CLI_Commands", "search", result["success"], "Search executed", result)

            # Test stats command
            result = self.run_command("python3 -m think_ai_cli stats", env=env)
            self.log_test(
                "CLI_Commands",
                "stats",
                result["success"] and "Statistics" in result["stdout"],
                "Statistics displayed",
                result,
            )

            # Test generate command
            result = self.run_command('python3 -m think_ai_cli generate "create a hello world function"', env=env)
            self.log_test(
                "CLI_Commands",
                "generate",
                result["success"] and "Generated" in result["stdout"],
                "Code generated",
                result,
            )

            # Test analyze command with a real file
            test_file = Path(temp_home) / "test_analyze.py"
            test_file.write_text(
                """
def calculate_sum(numbers):
    # TODO: Add error handling
    total = 0
    for num in numbers:
        total += num
    return total
"""
            )

            result = self.run_command(f"python3 -m think_ai_cli analyze {test_file}", env=env)
            self.log_test(
                "CLI_Commands", "analyze", result["success"] and "Analysis" in result["stdout"], "Code analyzed", result
            )

    def test_think_ai_core_functionality(self):
        """Test Think AI core Python API."""
        print("\n🔍 TESTING THINK AI CORE API")
        print("=" * 50)

        test_script = """
import sys
import json

try:
    # Import based on what's available
    try:
        from think_ai_cli import ThinkAI
    except ImportError:
        try:
            from think_ai_cli.core import ThinkAI
        except ImportError:
            from think_ai_cli.core_annoy import ThinkAI

    # Initialize
    ai = ThinkAI()
    results = {"tests": []}

    # Test 1: Add code
    try:
        idx = ai.add_code(
            "def hello_world():\\n    return 'Hello, World!'",
            "python",
            "Classic hello world function"
        )
        results["tests"].append({
            "name": "add_code",
            "passed": True,
            "index": idx
        })
    except Exception as e:
        results["tests"].append({
            "name": "add_code",
            "passed": False,
            "error": str(e)
        })

    # Test 2: Search
    try:
        search_results = ai.search("hello", k=3)
        results["tests"].append({
            "name": "search",
            "passed": len(search_results) > 0,
            "count": len(search_results)
        })
    except Exception as e:
        results["tests"].append({
            "name": "search",
            "passed": False,
            "error": str(e)
        })

    # Test 3: Generate code
    try:
        generated = ai.generate_code("create a function to add two numbers")
        results["tests"].append({
            "name": "generate",
            "passed": len(generated) > 0,
            "length": len(generated)
        })
    except Exception as e:
        results["tests"].append({
            "name": "generate",
            "passed": False,
            "error": str(e)
        })

    # Test 4: Analyze code
    try:
        analysis = ai.analyze_code("def test():\\n    pass")
        results["tests"].append({
            "name": "analyze",
            "passed": "lines" in analysis,
            "lines": analysis.get("lines", 0)
        })
    except Exception as e:
        results["tests"].append({
            "name": "analyze",
            "passed": False,
            "error": str(e)
        })

    # Test 5: Get stats
    try:
        stats = ai.get_stats()
        results["tests"].append({
            "name": "stats",
            "passed": "total_snippets" in stats,
            "snippets": stats.get("total_snippets", 0)
        })
    except Exception as e:
        results["tests"].append({
            "name": "stats",
            "passed": False,
            "error": str(e)
        })

    print(json.dumps(results))
    sys.exit(0)

except Exception as e:
    print(json.dumps({"error": str(e), "tests": []}))
    sys.exit(1)
"""

        # Save and run test script
        script_file = self.evidence_dir / "core_api_test.py"
        script_file.write_text(test_script)

        result = self.run_command(f"python3 {script_file}")

        if result["success"]:
            try:
                api_results = json.loads(result["stdout"])
                for test in api_results.get("tests", []):
                    self.log_test("Core_API", test["name"], test.get("passed", False), json.dumps(test), test)
            except json.JSONDecodeError:
                self.log_test("Core_API", "api_tests", False, f"Failed to parse results: {result['stdout']}", result)
        else:
            self.log_test("Core_API", "api_tests", False, result["stderr"] or "Failed to run API tests", result)

    def test_dependencies_and_imports(self):
        """Test all dependencies can be imported."""
        print("\n🔍 TESTING DEPENDENCIES")
        print("=" * 50)

        dependencies = [
            "torch",
            "numpy",
            "sentence_transformers",
            "faiss",
            "annoy",
            "click",
            "rich",
            "asyncio",
            "aiohttp",
            "pydantic",
            "uvicorn",
            "fastapi",
        ]

        for dep in dependencies:
            test_code = f"""
import sys
try:
    import {dep}
    print(f"SUCCESS: {dep} version {{getattr({dep}, '__version__', 'installed')}}")
    sys.exit(0)
except ImportError as e:
    print(f"FAILED: {{e}}")
    sys.exit(1)
"""
            result = self.run_command(f'python3 -c "{test_code}"')
            self.log_test("Dependencies", f"import_{dep}", result["success"], result["stdout"].strip(), result)

    def test_file_operations(self):
        """Test file operations and persistence."""
        print("\n🔍 TESTING FILE OPERATIONS")
        print("=" * 50)

        with tempfile.TemporaryDirectory() as temp_dir:
            # Test knowledge base persistence
            test_script = f"""
import os
os.environ['HOME'] = '{temp_dir}'

try:
    from think_ai_cli import ThinkAI
except ImportError:
    from think_ai_cli.core_annoy import ThinkAI

# Create instance and add data
ai1 = ThinkAI()
ai1.add_code("def persist_test(): pass", "python", "Persistence test")

# Create new instance and check if data persists
ai2 = ThinkAI()
stats = ai2.get_stats()
print(f"Snippets found: {{stats['total_snippets']}}")
"""

            result = self.run_command(f'python3 -c "{test_script}"')
            self.log_test(
                "File_Operations",
                "persistence",
                result["success"] and "Snippets found: 1" in result["stdout"],
                "Data persists across instances",
                result,
            )

            # Check knowledge base file creation
            kb_file = Path(temp_dir) / ".think-ai" / "knowledge.json"
            self.log_test(
                "File_Operations",
                "knowledge_base_file",
                kb_file.exists(),
                f"Knowledge base file created at {kb_file}",
                {"file_exists": kb_file.exists(), "path": str(kb_file)},
            )

    def test_error_handling(self):
        """Test error handling scenarios."""
        print("\n🔍 TESTING ERROR HANDLING")
        print("=" * 50)

        # Test missing required arguments
        result = self.run_command('python3 -m think_ai_cli add --code "test"')
        self.log_test(
            "Error_Handling",
            "missing_arguments",
            result["returncode"] != 0,
            "Properly handles missing required arguments",
            result,
        )

        # Test invalid file path
        result = self.run_command("python3 -m think_ai_cli analyze /nonexistent/file.py")
        self.log_test(
            "Error_Handling", "invalid_file", result["returncode"] != 0, "Properly handles invalid file paths", result
        )

        # Test empty search
        with tempfile.TemporaryDirectory() as temp_home:
            env = {"HOME": temp_home}
            result = self.run_command('python3 -m think_ai_cli search "nonexistent"', env=env)
            self.log_test(
                "Error_Handling", "empty_search", result["success"], "Handles empty search results gracefully", result
            )

    def test_performance(self):
        """Test performance benchmarks."""
        print("\n🔍 TESTING PERFORMANCE")
        print("=" * 50)

        perf_script = """
import time
import sys

try:
    from think_ai_cli import ThinkAI
except ImportError:
    from think_ai_cli.core_annoy import ThinkAI

ai = ThinkAI()

# Add 100 code snippets
start = time.time()
for i in range(100):
    ai.add_code(f"def func_{i}(): return {i}", "python", f"Function {i}")
add_time = time.time() - start

# Search performance
start = time.time()
results = ai.search("function that returns", k=10)
search_time = time.time() - start

print(f"Add 100 items: {add_time:.3f}s")
print(f"Search time: {search_time:.3f}s")
print(f"Search results: {len(results)}")
"""

        result = self.run_command(f'python3 -c "{perf_script}"')
        if result["success"]:
            lines = result["stdout"].strip().split("\n")
            add_time = float(lines[0].split(": ")[1].replace("s", ""))
            search_time = float(lines[1].split(": ")[1].replace("s", ""))

            self.log_test(
                "Performance",
                "bulk_add",
                add_time < 10,  # Should complete in under 10 seconds
                f"Added 100 items in {add_time:.3f}s",
                {"add_time": add_time},
            )

            self.log_test(
                "Performance",
                "search_speed",
                search_time < 1,  # Search should be under 1 second
                f"Search completed in {search_time:.3f}s",
                {"search_time": search_time},
            )
        else:
            self.log_test("Performance", "performance_test", False, "Performance test failed to run", result)

    def generate_final_report(self):
        """Generate comprehensive final report."""
        print("\n" + "=" * 60)
        print("📊 FINAL TEST REPORT")
        print("=" * 60)

        # Console summary
        total = self.results["summary"]["total"]
        passed = self.results["summary"]["passed"]
        failed = self.results["summary"]["failed"]
        success_rate = (passed / total * 100) if total > 0 else 0

        print(f"Total Tests: {total}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} ❌")
        print(f"Success Rate: {success_rate:.1f}%")
        print(f"\nEvidence saved to: {self.evidence_dir}")

        # Save full JSON report
        report_file = self.evidence_dir / "full_test_report.json"
        with open(report_file, "w") as f:
            json.dump(self.results, f, indent=2)

        # Generate HTML report
        html_report = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Think AI Full System Test Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; text-align: center; }}
        .summary {{ background: #e3f2fd; padding: 20px; border-radius: 5px; margin: 20px 0; }}
        .test-category {{ margin: 20px 0; }}
        .test-result {{ padding: 10px; margin: 5px 0; border-left: 4px solid #ddd; background: #fafafa; }}
        .pass {{ border-color: #4caf50; background: #e8f5e9; }}
        .fail {{ border-color: #f44336; background: #ffebee; }}
        .details {{ font-family: monospace; font-size: 12px; color: #666; margin-top: 5px; }}
        .evidence {{ background: #f0f0f0; padding: 10px; margin: 10px 0; border-radius: 3px; overflow-x: auto; }}
        pre {{ white-space: pre-wrap; word-wrap: break-word; }}
        .stats {{ display: flex; justify-content: space-around; text-align: center; }}
        .stat {{ padding: 20px; }}
        .stat-value {{ font-size: 2em; font-weight: bold; }}
        .pass-rate {{ color: {'#4caf50' if success_rate >= 80 else '#ff9800' if success_rate >= 60 else '#f44336'}; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Think AI Full System Test Report</h1>

        <div class="summary">
            <h2>Test Summary</h2>
            <div class="stats">
                <div class="stat">
                    <div class="stat-value">{total}</div>
                    <div>Total Tests</div>
                </div>
                <div class="stat">
                    <div class="stat-value" style="color: #4caf50;">{passed}</div>
                    <div>Passed</div>
                </div>
                <div class="stat">
                    <div class="stat-value" style="color: #f44336;">{failed}</div>
                    <div>Failed</div>
                </div>
                <div class="stat">
                    <div class="stat-value pass-rate">{success_rate:.1f}%</div>
                    <div>Success Rate</div>
                </div>
            </div>
            <p><strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <p><strong>Evidence Directory:</strong> {self.evidence_dir}</p>
        </div>

        <h2>Detailed Test Results</h2>
"""

        # Group tests by category
        categories = {}
        for test in self.results["tests"]:
            category = test["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append(test)

        for category, tests in categories.items():
            html_report += f"""
        <div class="test-category">
            <h3>{category}</h3>
"""
            for test in tests:
                status_class = "pass" if test["passed"] else "fail"
                status_icon = "✅" if test["passed"] else "❌"

                html_report += f"""
            <div class="test-result {status_class}">
                <strong>{status_icon} {test['name']}</strong>
                <div class="details">{test['details']}</div>
"""

                if test.get("evidence") and isinstance(test["evidence"], dict):
                    if test["evidence"].get("stdout"):
                        html_report += f"""
                <div class="evidence">
                    <strong>Output:</strong>
                    <pre>{test['evidence']['stdout'][:500]}{'...' if len(test['evidence'].get('stdout', '')) > 500 else ''}</pre>
                </div>
"""

                html_report += """
            </div>
"""

            html_report += """
        </div>
"""

        html_report += """
    </div>
</body>
</html>
"""

        # Save HTML report
        html_file = self.evidence_dir / "test_report.html"
        with open(html_file, "w") as f:
            f.write(html_report)

        print(f"\n📄 HTML Report: {html_file}")
        print(f"📄 JSON Report: {report_file}")

        # Return success status
        return success_rate >= 80  # Consider 80% as passing

    def run_all_tests(self):
        """Run all tests in sequence."""
        print("🚀 THINK AI FULL SYSTEM TEST SUITE")
        print("=" * 60)
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Evidence Directory: {self.evidence_dir}")
        print("=" * 60)

        try:
            self.test_python_environment()
            self.test_think_ai_installation()
            self.test_think_ai_cli_commands()
            self.test_think_ai_core_functionality()
            self.test_dependencies_and_imports()
            self.test_file_operations()
            self.test_error_handling()
            self.test_performance()
        except Exception as e:
            print(f"\n❌ CRITICAL ERROR: {e}")
            traceback.print_exc()
            self.results["summary"]["errors"].append(
                {"type": "critical", "error": str(e), "traceback": traceback.format_exc()}
            )

        # Generate final report
        success = self.generate_final_report()

        return success


def main():
    """Main entry point."""
    tester = FullSystemTester()
    success = tester.run_all_tests()

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
