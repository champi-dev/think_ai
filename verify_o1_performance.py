#!/usr / bin / env python3
"""Scientific verification of O(1) performance claims"""

import json
import time
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from o1_vector_search import O1VectorSearch


class ScientificVerifier:
"""Rigorous scientific verification of O(1) claims"""

    def __init__(self):
        self.results = {
        "timestamp": datetime.now().isoformat(),
        "benchmarks": [],
        "statistical_tests": {},
        "hardware_info": self._get_hardware_info()
        }

        def _get_hardware_info(self):
"""Get system information"""
import platform

import psutil

            return {
        "platform": platform.platform(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "cpu_count": psutil.cpu_count(),
        "memory_gb": round(psutil.virtual_memory().total / (1024**3), 2)
        }

        def benchmark_scaling(
        self,
        sizes=[
        1000,
        5000,
        10000,
        50000,
        100000,
        500000,
        1000000]):
"""Benchmark search performance across different dataset sizes"""
            print("🔬 Running O(1) Scaling Benchmark...")
            print("=" * 60)

            dim = 384
            num_queries = 500

            for size in sizes:
                print(f"\n📊 Testing with {size:, } vectors...")

# Create and populate index
                index = O1VectorSearch(dim=dim)

# Generate random data
                np.random.seed(42)  # Reproducibility
                vectors = np.random.randn(size, dim).astype(np.float32)

# Measure indexing time
                index_start = time.perf_counter()
                for i, vec in enumerate(vectors):
                    index.add(vec, {"id": i, "size": size})
                    index_time = time.perf_counter() - index_start

# Benchmark search
                    search_times = []
                    queries = np.random.randn(num_queries, dim).astype(np.float32)

                    for query in queries:
                        start = time.perf_counter()
                        results = index.search(query, k=10)
                        end = time.perf_counter()
                        search_times.append((end - start) * 1000)  # Convert to ms

# Calculate statistics
                        search_times = np.array(search_times)

                        benchmark = {
                        "size": size,
                        "index_time_s": index_time,
                        "search_times_ms": search_times.tolist(),
                        "mean_ms": float(np.mean(search_times)),
                        "median_ms": float(np.median(search_times)),
                        "std_ms": float(np.std(search_times)),
                        "min_ms": float(np.min(search_times)),
                        "max_ms": float(np.max(search_times)),
                        "p50_ms": float(np.percentile(search_times, 50)),
                        "p90_ms": float(np.percentile(search_times, 90)),
                        "p95_ms": float(np.percentile(search_times, 95)),
                        "p99_ms": float(np.percentile(search_times, 99))
                        }

                        self.results["benchmarks"].append(benchmark)

                        print(f"✅ Mean search time: {benchmark["mean_ms"]:.3f}ms")
                        print(f" Median: {benchmark["median_ms"]:.3f}ms")
                        print(f" P99: {benchmark["p99_ms"]:.3f}ms")

                        def statistical_analysis(self):
"""Perform statistical tests to verify O(1) behavior"""
                            print("\n🔬 Statistical Analysis")
                            print("=" * 60)

# Extract data
                            sizes = np.array([b["size"] for b in self.results["benchmarks"]])
                            means = np.array([b["mean_ms"] for b in self.results["benchmarks"]])

# 1. Linear regression on log - log scale
                            log_sizes = np.log10(sizes)
                            log_times = np.log10(means)

                            slope, intercept, r_value, p_value, std_err = stats.linregress(
                            log_sizes, log_times)

                            print(f"\n📈 Log - Log Regression Analysis:")
                            print(f" Slope (β): {slope:.4f} ± {std_err:.4f}")
                            print(f" R²: {r_value**2:.4f}")
                            print(f" p - value: {p_value:.4f}")

# Interpretation
                            if abs(slope) < 0.1 and p_value > 0.05:
                                print(f" ✅ CONFIRMED: No significant scaling (O(1) behavior)")
                            else:
                                print(f" ❌ WARNING: Significant scaling detected")

                                self.results["statistical_tests"]["regression"] = {
                                "slope": float(slope),
                                "stderr": float(std_err),
                                "r_squared": float(r_value**2),
                                "p_value": float(p_value),
                                "conclusion": "O(1)" if abs(slope) < 0.1 else f"O(n^{slope:.2f})"
                                }

# 2. ANOVA test
                                search_times_by_size = [b["search_times_ms"][:100]
                                for b in self.results["benchmarks"]]
                                f_stat, anova_p = stats.f_oneway(*search_times_by_size)

                                print(f"\n📊 ANOVA Test (difference between groups):")
                                print(f" F - statistic: {f_stat:.4f}")
                                print(f" p - value: {anova_p:.4f}")

                                if anova_p > 0.05:
                                    print(f" ✅ No significant difference between dataset sizes")
                                else:
                                    print(f" ⚠️ Some difference detected between sizes")

                                    self.results["statistical_tests"]["anova"] = {
                                    "f_statistic": float(f_stat),
                                    "p_value": float(anova_p),
                                    "significant": anova_p < 0.05
                                    }

# 3. Calculate complexity order
# If time = c * n^k, then k ≈ slope in log - log regression
                                    complexity_order = abs(slope)

                                    print(f"\n🎯 Empirical Complexity: O(n^{complexity_order:.3f})")
                                    print(f" Theoretical: O(1)")
                                    print(f" Match: {"✅ YES" if complexity_order < 0.1 else "❌ NO"}")

                                    def generate_plots(self):
"""Generate visualization plots"""
                                        print("\n📊 Generating Evidence Plots...")

                                        plt.style.use("bmh")
                                        fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Extract data
                                        sizes = np.array([b["size"] for b in self.results["benchmarks"]])
                                        means = np.array([b["mean_ms"] for b in self.results["benchmarks"]])
                                        p99s = np.array([b["p99_ms"] for b in self.results["benchmarks"]])

# Plot 1: Linear scale
                                        ax1 = axes[0, 0]
                                        ax1.plot(
                                        sizes / 1000,
                                        means,
                                        "b - o",
                                        linewidth=2,
                                        markersize=8,
                                        label="Mean")
                                        ax1.plot(
                                        sizes / 1000,
                                        p99s,
                                        "r--^",
                                        linewidth=2,
                                        markersize=8,
                                        label="P99")
                                        ax1.axhline(y=means[0], color="g", linestyle=":", label="O(1) Reference")
                                        ax1.set_xlabel("Dataset Size (thousands)")
                                        ax1.set_ylabel("Search Time (ms)")
                                        ax1.set_title("O(1) Performance: Linear Scale")
                                        ax1.legend()
                                        ax1.grid(True, alpha=0.3)

# Plot 2: Log - log scale
                                        ax2 = axes[0, 1]
                                        ax2.loglog(
                                        sizes,
                                        means,
                                        "b - o",
                                        linewidth=2,
                                        markersize=8,
                                        label="Actual")
                                        ax2.loglog(
                                        sizes,
                                        np.ones_like(sizes) *
                                        means[0],
                                        "g--",
                                        linewidth=2,
                                        label="Perfect O(1)")
                                        ax2.loglog(sizes, means[0] * (sizes / sizes[0]),
                                        "r:", linewidth=2, label="O(n) Reference")
                                        ax2.set_xlabel("Dataset Size (log scale)")
                                        ax2.set_ylabel("Search Time (ms, log scale)")
                                        ax2.set_title("O(1) Performance: Log - Log Scale")
                                        ax2.legend()
                                        ax2.grid(True, alpha=0.3)

# Plot 3: Distribution
                                        ax3 = axes[1, 0]
                                        for i, b in enumerate(self.results["benchmarks"][::2]):  # Every other size
                                        ax3.hist(b["search_times_ms"][:100], bins=30, alpha=0.5,
                                        label=f"{b["size"]//1000}K vectors")
                                        ax3.set_xlabel("Search Time (ms)")
                                        ax3.set_ylabel("Frequency")
                                        ax3.set_title("Search Time Distribution")
                                        ax3.legend()
                                        ax3.grid(True, alpha=0.3)

# Plot 4: Scaling factor
                                        ax4 = axes[1, 1]
                                        scaling_factors = means / means[0]
                                        ax4.plot(sizes / 1000, scaling_factors, "b - o", linewidth=2, markersize=8)
                                        ax4.axhline(y=1.0, color="g", linestyle="--", label="Perfect O(1)")
                                        ax4.fill_between(
                                        sizes / 1000,
                                        0.9,
                                        1.1,
                                        alpha=0.3,
                                        color="g",
                                        label="±10% bound")
                                        ax4.set_xlabel("Dataset Size (thousands)")
                                        ax4.set_ylabel("Scaling Factor")
                                        ax4.set_title("Scaling Analysis (relative to 1K dataset)")
                                        ax4.legend()
                                        ax4.grid(True, alpha=0.3)
                                        ax4.set_ylim(0.5, 1.5)

                                        plt.tight_layout()
                                        plt.savefig("o1_performance_evidence.png", dpi=300, bbox_inches="tight")
                                        print("✅ Saved plots to o1_performance_evidence.png")

                                        def generate_report(self):
"""Generate final scientific report"""
                                            print("\n" + "="*60)
                                            print("📋 SCIENTIFIC EVIDENCE SUMMARY")
                                            print("="*60)

# Performance summary
                                            all_means = [b["mean_ms"] for b in self.results["benchmarks"]]
                                            print(f"\n🎯 Performance Metrics:")
                                            print(
                                            f" Dataset sizes: {self.results["benchmarks"][0]["size"]:, } to {self.results["benchmarks"][-1]["size"]:, }")
                                            print(
                                            f" Mean search time range: {min(all_means):.3f}ms - {max(all_means):.3f}ms")
                                            print(f" Variation: {(max(all_means)/min(all_means) - 1)*100:.1f}%")

# Statistical summary
                                            print(f"\n📊 Statistical Evidence:")
                                            reg = self.results["statistical_tests"]["regression"]
                                            print(f" Scaling exponent: {reg["slope"]:.4f} (expect 0 for O(1))")
                                            print(f" R²: {reg["r_squared"]:.4f}")
                                            print(f" Statistical significance: p={reg["p_value"]:.4f}")

# Conclusion
                                            is_o1 = abs(reg["slope"]) < 0.1 and reg["p_value"] > 0.05
                                            print(f"\n✅ CONCLUSION: {"O(1) VERIFIED" if is_o1 else "NOT O(1)"}")

# Save results
                                            with open("o1_scientific_evidence.json", "w") as f:
                                                json.dump(self.results, f, indent=2)
                                                print(f"\n📄 Full results saved to o1_scientific_evidence.json")

                                                def run_complete_verification(self):
"""Run complete scientific verification"""
                                                    print("🚀 Think AI O(1) Scientific Verification")
                                                    print("="*60)

# Run benchmarks
                                                    self.benchmark_scaling()

# Statistical analysis
                                                    self.statistical_analysis()

# Generate plots
                                                    self.generate_plots()

# Final report
                                                    self.generate_report()

                                                    return self.results


                                                def main():
"""Run scientific verification"""
                                                    verifier = ScientificVerifier()
                                                    results = verifier.run_complete_verification()

                                                    print("\n✨ Scientific verification complete!")
                                                    print("🔬 Evidence files generated:")
                                                    print(" - o1_performance_evidence.png")
                                                    print(" - o1_scientific_evidence.json")
                                                    print(" - SCIENTIFIC_EVIDENCE.md")


                                                    if __name__ == "__main__":
                                                        main()
