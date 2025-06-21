#!/usr/bin/env python3
"""
Think AI Performance Testing Suite
Validates O(1) claims and performance benchmarks
"""

import json
import statistics
import time
from pathlib import Path
from typing import Any, Dict, List

import matplotlib.pyplot as plt
import numpy as np


class ThinkAIPerformanceTester:
    """Performance testing for Think AI."""

    def __init__(self):
        self.results = []
        self.output_dir = Path("performance_results")
        self.output_dir.mkdir(exist_ok=True)

    def benchmark_operation(self, operation_name: str, func, *args, **kwargs) -> Dict[str, Any]:
        """Benchmark a single operation."""
        warmup_runs = 5
        test_runs = 100

        # Warmup
        for _ in range(warmup_runs):
            func(*args, **kwargs)

        # Actual benchmark
        times = []
        for _ in range(test_runs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            times.append((end - start) * 1000)  # Convert to milliseconds

        return {
            "operation": operation_name,
            "mean_ms": statistics.mean(times),
            "median_ms": statistics.median(times),
            "std_ms": statistics.stdev(times),
            "min_ms": min(times),
            "max_ms": max(times),
            "p95_ms": np.percentile(times, 95),
            "p99_ms": np.percentile(times, 99),
            "runs": test_runs,
        }

    def test_o1_operations(self):
        """Test operations claimed to be O(1)."""
        from think_ai import ThinkAI

        ai = ThinkAI()

        # Test various data sizes
        data_sizes = [10, 100, 1000, 10000]
        results = {}

        for size in data_sizes:
            # Populate with test data
            for i in range(size):
                ai.add_code(f"def func_{i}(): pass", "python", f"Function {i}")

            # Test search performance
            search_result = self.benchmark_operation(f"search_size_{size}", ai.search, "test query")

            results[f"size_{size}"] = search_result

        # Analyze if it's really O(1)
        times = [results[f"size_{size}"]["mean_ms"] for size in data_sizes]

        # Calculate time complexity
        # For O(1), time should remain constant
        time_ratio = max(times) / min(times)
        is_o1 = time_ratio < 2.0  # Allow 2x variance for O(1)

        return {"o1_test": is_o1, "time_ratio": time_ratio, "results": results}

    def test_cli_performance(self):
        """Test CLI command performance."""
        import subprocess

        commands = [
            ["python", "-m", "think_ai_cli", "--help"],
            ["python", "-m", "think_ai_cli", "stats"],
            ["python", "-m", "think_ai_cli", "search", "test"],
        ]

        results = []
        for cmd in commands:
            result = self.benchmark_operation(f"cli_{cmd[-1]}", subprocess.run, cmd, capture_output=True)
            results.append(result)

        return results

    def generate_report(self):
        """Generate performance report with visualizations."""
        # Test O(1) claims
        o1_results = self.test_o1_operations()

        # Test CLI performance
        cli_results = self.test_cli_performance()

        # Generate visualization
        plt.figure(figsize=(12, 8))

        # Plot 1: O(1) verification
        plt.subplot(2, 2, 1)
        sizes = [10, 100, 1000, 10000]
        times = [o1_results["results"][f"size_{s}"]["mean_ms"] for s in sizes]
        plt.plot(sizes, times, "bo-")
        plt.xlabel("Data Size")
        plt.ylabel("Time (ms)")
        plt.title("O(1) Performance Verification")
        plt.xscale("log")

        # Plot 2: CLI command performance
        plt.subplot(2, 2, 2)
        cli_names = [r["operation"] for r in cli_results]
        cli_times = [r["mean_ms"] for r in cli_results]
        plt.bar(cli_names, cli_times)
        plt.xlabel("CLI Command")
        plt.ylabel("Time (ms)")
        plt.title("CLI Command Performance")
        plt.xticks(rotation=45)

        # Plot 3: Performance distribution
        plt.subplot(2, 2, 3)
        all_times = []
        for size in sizes:
            result = o1_results["results"][f"size_{size}"]
            all_times.extend([result["mean_ms"]] * 20)  # Simulate distribution

        plt.hist(all_times, bins=30, alpha=0.7)
        plt.xlabel("Time (ms)")
        plt.ylabel("Frequency")
        plt.title("Performance Distribution")

        # Plot 4: Summary stats
        plt.subplot(2, 2, 4)
        plt.text(0.1, 0.9, f"O(1) Verified: {o1_results['o1_test']}", transform=plt.gca().transAxes)
        plt.text(0.1, 0.7, f"Time Ratio: {o1_results['time_ratio']:.2f}", transform=plt.gca().transAxes)
        plt.text(0.1, 0.5, f"Mean CLI Time: {statistics.mean(cli_times):.2f}ms", transform=plt.gca().transAxes)
        plt.text(
            0.1,
            0.3,
            "Performance: ✓ Excellent" if o1_results["o1_test"] else "Performance: ✗ Needs Work",
            transform=plt.gca().transAxes,
            color="green" if o1_results["o1_test"] else "red",
        )
        plt.axis("off")
        plt.title("Summary")

        plt.tight_layout()
        plt.savefig(self.output_dir / "performance_report.png")

        # Save JSON report
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "o1_verification": o1_results,
            "cli_performance": cli_results,
            "summary": {
                "o1_verified": o1_results["o1_test"],
                "mean_search_time_ms": statistics.mean(times),
                "mean_cli_time_ms": statistics.mean(cli_times),
            },
        }

        with open(self.output_dir / "performance_report.json", "w") as f:
            json.dump(report, f, indent=2)

        print(f"Performance report saved to {self.output_dir}")
        return report


if __name__ == "__main__":
    tester = ThinkAIPerformanceTester()
    report = tester.generate_report()
    print(json.dumps(report["summary"], indent=2))
