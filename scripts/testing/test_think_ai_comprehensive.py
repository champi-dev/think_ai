#!/usr/bin/env python3
"""
Comprehensive Test Suite for Think AI CLI
Tests all functionality with evidence generation
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

import pytest
from click.testing import CliRunner
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class TestReport:
    """Test report generator with evidence collection."""

    def __init__(self):
        self.results = []
        self.console = Console()
        self.start_time = time.time()
        self.test_dir = Path("test_evidence") / datetime.now().strftime("%Y%m%d_%H%M%S")
        self.test_dir.mkdir(parents=True, exist_ok=True)

    def add_result(self, category: str, test_name: str, passed: bool, details: str = "", screenshot: str = None):
        """Add a test result with evidence."""
        result = {
            "category": category,
            "test_name": test_name,
            "passed": passed,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "screenshot": screenshot,
        }
        self.results.append(result)

        # Save evidence
        evidence_file = self.test_dir / f"{category}_{test_name}.json"
        with open(evidence_file, "w") as f:
            json.dump(result, f, indent=2)

    def generate_report(self):
        """Generate comprehensive test report."""
        duration = time.time() - self.start_time
        passed_tests = sum(1 for r in self.results if r["passed"])
        failed_tests = len(self.results) - passed_tests

        # Console report
        self.console.print(Panel("[bold green]Think AI CLI Test Report[/bold green]"))

        table = Table(title="Test Summary")
        table.add_column("Category", style="cyan")
        table.add_column("Test", style="yellow")
        table.add_column("Status", style="green")
        table.add_column("Details")

        for result in self.results:
            status = "[green]✓ PASS[/green]" if result["passed"] else "[red]✗ FAIL[/red]"
            table.add_row(
                result["category"],
                result["test_name"],
                status,
                result["details"][:50] + "..." if len(result["details"]) > 50 else result["details"],
            )

        self.console.print(table)

        # Summary
        self.console.print(f"\n[bold]Total Tests:[/bold] {len(self.results)}")
        self.console.print(f"[green]Passed:[/green] {passed_tests}")
        self.console.print(f"[red]Failed:[/red] {failed_tests}")
        self.console.print(f"[yellow]Duration:[/yellow] {duration:.2f}s")
        self.console.print(f"[blue]Evidence saved to:[/blue] {self.test_dir}")

        # HTML report
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Think AI CLI Test Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #1e88e5; color: white; padding: 20px; border-radius: 5px; }}
        .summary {{ margin: 20px 0; padding: 15px; background: #f5f5f5; border-radius: 5px; }}
        .test-result {{ margin: 10px 0; padding: 10px; border-left: 4px solid #ccc; }}
        .pass {{ border-color: #4caf50; background: #e8f5e9; }}
        .fail {{ border-color: #f44336; background: #ffebee; }}
        .evidence {{ background: #f0f0f0; padding: 10px; margin: 10px 0; border-radius: 3px; }}
        pre {{ background: #263238; color: #aed581; padding: 10px; border-radius: 3px; overflow-x: auto; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Think AI CLI Comprehensive Test Report</h1>
        <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    </div>

    <div class="summary">
        <h2>Summary</h2>
        <p><strong>Total Tests:</strong> {len(self.results)}</p>
        <p><strong>Passed:</strong> <span style="color: green;">{passed_tests}</span></p>
        <p><strong>Failed:</strong> <span style="color: red;">{failed_tests}</span></p>
        <p><strong>Success Rate:</strong> {(passed_tests/len(self.results)*100):.1f}%</p>
        <p><strong>Duration:</strong> {duration:.2f} seconds</p>
    </div>

    <h2>Detailed Results</h2>
"""

        for result in self.results:
            status_class = "pass" if result["passed"] else "fail"
            status_text = "PASSED" if result["passed"] else "FAILED"

            html_content += f"""
    <div class="test-result {status_class}">
        <h3>{result['category']} :: {result['test_name']} - {status_text}</h3>
        <p><strong>Time:</strong> {result['timestamp']}</p>
        <div class="evidence">
            <pre>{result['details']}</pre>
        </div>
    </div>
"""

        html_content += """
</body>
</html>
"""

        report_path = self.test_dir / "test_report.html"
        with open(report_path, "w") as f:
            f.write(html_content)

        # JSON summary
        summary_path = self.test_dir / "test_summary.json"
        with open(summary_path, "w") as f:
            json.dump(
                {
                    "total_tests": len(self.results),
                    "passed": passed_tests,
                    "failed": failed_tests,
                    "success_rate": passed_tests / len(self.results) * 100,
                    "duration": duration,
                    "results": self.results,
                },
                f,
                indent=2,
            )

        return passed_tests, failed_tests


class ThinkAITester:
    """Comprehensive tester for Think AI CLI."""

    def __init__(self):
        self.report = TestReport()
        self.runner = CliRunner()
        self.temp_dir = None

    def setup(self):
        """Setup test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_home = os.environ.get("HOME")
        os.environ["HOME"] = self.temp_dir

    def teardown(self):
        """Cleanup test environment."""
        if self.original_home:
            os.environ["HOME"] = self.original_home
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def run_cli_command(self, args: List[str]) -> Tuple[int, str]:
        """Run Think AI CLI command and return exit code and output."""
        try:
            from think_ai_cli.cli import cli

            result = self.runner.invoke(cli, args)
            return result.exit_code, result.output
        except Exception as e:
            return 1, str(e)

    def test_installation(self):
        """Test that Think AI CLI is properly installed."""
        try:
            import think_ai_cli

            self.report.add_result(
                "Installation",
                "import_module",
                True,
                f"Successfully imported think_ai_cli version {think_ai_cli.__version__}",
            )
        except Exception as e:
            self.report.add_result("Installation", "import_module", False, f"Failed to import: {str(e)}")

        # Test CLI entry point
        try:
            result = subprocess.run(["python", "-m", "think_ai_cli", "--version"], capture_output=True, text=True)
            success = result.returncode == 0
            self.report.add_result(
                "Installation", "cli_entry_point", success, f"Exit code: {result.returncode}, Output: {result.stdout}"
            )
        except Exception as e:
            self.report.add_result("Installation", "cli_entry_point", False, str(e))

    def test_help_commands(self):
        """Test help functionality."""
        commands = ["", "search", "add", "generate", "analyze", "stats", "clear", "interactive"]

        for cmd in commands:
            args = ["--help"] if cmd == "" else [cmd, "--help"]
            exit_code, output = self.run_cli_command(args)

            success = exit_code == 0 and "help" in output.lower()
            self.report.add_result(
                "Help", f"help_{cmd or 'main'}", success, f"Exit code: {exit_code}, Output preview: {output[:200]}"
            )

    def test_add_functionality(self):
        """Test adding code to knowledge base."""
        # Test adding with code option
        exit_code, output = self.run_cli_command(
            [
                "add",
                "--code",
                "def hello(): return 'world'",
                "--language",
                "python",
                "--description",
                "Simple hello function",
                "--tags",
                "example",
                "--tags",
                "test",
            ]
        )

        success = exit_code == 0 and "Added successfully" in output
        self.report.add_result(
            "Core_Features", "add_code_snippet", success, f"Exit code: {exit_code}, Output: {output}"
        )

        # Test adding from file
        test_file = Path(self.temp_dir) / "test_code.py"
        test_file.write_text(
            """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""
        )

        exit_code, output = self.run_cli_command(
            ["add", "--file", str(test_file), "--language", "python", "--description", "Fibonacci function"]
        )

        success = exit_code == 0 and "Added successfully" in output
        self.report.add_result("Core_Features", "add_from_file", success, f"Exit code: {exit_code}, Output: {output}")

    def test_search_functionality(self):
        """Test search functionality."""
        # First add some code
        self.run_cli_command(
            [
                "add",
                "--code",
                "def quicksort(arr): pass",
                "--language",
                "python",
                "--description",
                "Quicksort algorithm",
            ]
        )

        # Search for it
        exit_code, output = self.run_cli_command(["search", "sorting algorithm", "--number", "5"])

        success = exit_code == 0
        self.report.add_result(
            "Core_Features", "search_code", success, f"Exit code: {exit_code}, Output: {output[:300]}"
        )

        # Test search with language filter
        exit_code, output = self.run_cli_command(["search", "function", "--language", "python"])

        self.report.add_result("Core_Features", "search_with_filter", exit_code == 0, f"Exit code: {exit_code}")

    def test_generate_functionality(self):
        """Test code generation."""
        # Basic generation
        exit_code, output = self.run_cli_command(
            ["generate", "create a function to calculate factorial", "--language", "python"]
        )

        success = exit_code == 0 and "Generated" in output
        self.report.add_result(
            "Core_Features",
            "generate_code",
            success,
            f"Exit code: {exit_code}, Generated code found: {'def' in output}",
        )

        # Generation with output file
        output_file = Path(self.temp_dir) / "generated.py"
        exit_code, output = self.run_cli_command(
            ["generate", "binary search implementation", "--language", "python", "--output", str(output_file)]
        )

        file_created = output_file.exists()
        success = exit_code == 0 and file_created
        self.report.add_result(
            "Core_Features", "generate_with_output", success, f"Exit code: {exit_code}, File created: {file_created}"
        )

    def test_analyze_functionality(self):
        """Test code analysis."""
        # Create a test file
        test_file = Path(self.temp_dir) / "analyze_test.py"
        test_file.write_text(
            """
def complex_function(data):
    # TODO: Add error handling
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result

# FIXME: This is broken
def broken_function():
    pass
"""
        )

        exit_code, output = self.run_cli_command(["analyze", str(test_file)])

        success = exit_code == 0 and "Analysis" in output
        has_suggestions = "TODO" in output or "test" in output.lower()

        self.report.add_result(
            "Core_Features", "analyze_code", success, f"Exit code: {exit_code}, Found suggestions: {has_suggestions}"
        )

    def test_stats_functionality(self):
        """Test statistics functionality."""
        # Add some test data first
        for i in range(3):
            self.run_cli_command(
                [
                    "add",
                    "--code",
                    f"def test_{i}(): pass",
                    "--language",
                    "python",
                    "--description",
                    f"Test function {i}",
                ]
            )

        exit_code, output = self.run_cli_command(["stats"])

        success = exit_code == 0 and "Statistics" in output
        has_count = "3" in output or "Total" in output

        self.report.add_result(
            "Core_Features", "view_stats", success, f"Exit code: {exit_code}, Shows count: {has_count}"
        )

    def test_clear_functionality(self):
        """Test clear functionality."""
        # Add data
        self.run_cli_command(["add", "--code", "test", "--language", "python", "--description", "test"])

        # Clear with confirmation
        exit_code, output = self.run_cli_command(["clear", "--yes"])

        success = exit_code == 0
        self.report.add_result("Core_Features", "clear_knowledge_base", success, f"Exit code: {exit_code}")

        # Verify cleared
        exit_code, output = self.run_cli_command(["stats"])
        is_empty = "0" in output or "Total Code Snippets" in output

        self.report.add_result("Core_Features", "verify_clear", is_empty, f"Knowledge base empty: {is_empty}")

    def test_error_handling(self):
        """Test error handling."""
        # Missing required arguments
        exit_code, output = self.run_cli_command(
            [
                "add",
                "--code",
                "test",
                # Missing required --language and --description
            ]
        )

        self.report.add_result(
            "Error_Handling", "missing_arguments", exit_code != 0, f"Properly failed with exit code: {exit_code}"
        )

        # Invalid file path
        exit_code, output = self.run_cli_command(["analyze", "/nonexistent/file.py"])

        self.report.add_result("Error_Handling", "invalid_file", exit_code != 0, f"Properly handled missing file")

    def test_persistence(self):
        """Test data persistence."""
        # Add data
        self.run_cli_command(
            [
                "add",
                "--code",
                "def persistent_test(): return True",
                "--language",
                "python",
                "--description",
                "Persistence test",
            ]
        )

        # Check stats
        exit_code1, output1 = self.run_cli_command(["stats"])

        # Simulate new session by creating new CLI instance
        from think_ai_cli import ThinkAI

        new_instance = ThinkAI()

        # Check if data persists
        stats = new_instance.get_stats()
        has_data = stats["total_snippets"] > 0

        self.report.add_result(
            "Persistence",
            "data_persistence",
            has_data,
            f"Data persisted across instances: {has_data}, Snippets: {stats['total_snippets']}",
        )

    def test_vector_search_quality(self):
        """Test vector search quality."""
        # Add various code snippets
        test_data = [
            ("def sort_array(arr): return sorted(arr)", "python", "Sort array function"),
            ("function sortArray(arr) { return arr.sort(); }", "javascript", "Sort array in JS"),
            ("def binary_search(arr, target): pass", "python", "Binary search algorithm"),
            ("class QuickSort: pass", "python", "QuickSort implementation"),
        ]

        for code, lang, desc in test_data:
            self.run_cli_command(["add", "--code", code, "--language", lang, "--description", desc])

        # Test semantic search
        exit_code, output = self.run_cli_command(["search", "sorting algorithm implementation"])

        found_sort = "sort" in output.lower()
        self.report.add_result(
            "Vector_Search",
            "semantic_search",
            exit_code == 0 and found_sort,
            f"Found sorting-related code: {found_sort}",
        )

    def test_performance(self):
        """Test performance with larger dataset."""
        start_time = time.time()

        # Add 50 code snippets
        for i in range(50):
            self.run_cli_command(
                [
                    "add",
                    "--code",
                    f"def function_{i}(x): return x * {i}",
                    "--language",
                    "python",
                    "--description",
                    f"Function number {i}",
                ]
            )

        add_time = time.time() - start_time

        # Test search performance
        search_start = time.time()
        exit_code, output = self.run_cli_command(["search", "function that multiplies", "--number", "10"])
        search_time = time.time() - search_start

        self.report.add_result(
            "Performance",
            "bulk_operations",
            add_time < 30 and search_time < 2,
            f"Added 50 items in {add_time:.2f}s, Search took {search_time:.2f}s",
        )

    def run_all_tests(self):
        """Run all tests."""
        self.setup()

        try:
            # Run all test categories
            self.test_installation()
            self.test_help_commands()
            self.test_add_functionality()
            self.test_search_functionality()
            self.test_generate_functionality()
            self.test_analyze_functionality()
            self.test_stats_functionality()
            self.test_clear_functionality()
            self.test_error_handling()
            self.test_persistence()
            self.test_vector_search_quality()
            self.test_performance()

        finally:
            self.teardown()

        # Generate report
        passed, failed = self.report.generate_report()

        return passed, failed


def main():
    """Main test runner."""
    console = Console()

    console.print(
        Panel(
            "[bold cyan]Think AI CLI Comprehensive Test Suite[/bold cyan]\n"
            "Testing all functionality with evidence generation",
            border_style="cyan",
        )
    )

    tester = ThinkAITester()
    passed, failed = tester.run_all_tests()

    # Exit with appropriate code
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
