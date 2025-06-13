#!/usr / bin / env python3
"""Simplified O(1) performance verification without plotting"""

import time
import numpy as np
from scipy import stats
import json
from datetime import datetime
from o1_vector_search import O1VectorSearch


def verify_o1_performance():
"""Verify O(1) performance with concrete measurements"""

    print("🔬 Think AI O(1) Performance Verification")
    print("=" * 60)

# Test parameters
    sizes = [1000, 5000, 10000, 50000, 100000, 500000]
    dim = 384
    num_queries = 200

    results = []

    for size in sizes:
        print(f"\n📊 Testing with {size:, } vectors...")

# Create index
        index = O1VectorSearch(dim=dim)

# Generate data
        np.random.seed(42)
        vectors = np.random.randn(size, dim).astype(np.float32)

# Index vectors
        start = time.time()
        for i, vec in enumerate(vectors):
            index.add(vec, {"id": i})
            index_time = time.time() - start

# Measure search times
            search_times = []
            queries = np.random.randn(num_queries, dim).astype(np.float32)

            for query in queries:
                start = time.perf_counter()
                _ = index.search(query, k=10)
                end = time.perf_counter()
                search_times.append((end - start) * 1000)

                search_times = np.array(search_times)

                result = {
                "size": size,
                "index_time": index_time,
                "mean_ms": float(np.mean(search_times)),
                "std_ms": float(np.std(search_times)),
                "min_ms": float(np.min(search_times)),
                "max_ms": float(np.max(search_times)),
                "p50_ms": float(np.percentile(search_times, 50)),
                "p90_ms": float(np.percentile(search_times, 90)),
                "p99_ms": float(np.percentile(search_times, 99))
                }

                results.append(result)

                print(f"✅ Mean: {result["mean_ms"]:.3f}ms, P99: {result["p99_ms"]:.3f}ms")

# Statistical analysis
                print("\n" + "="*60)
                print("📊 Statistical Analysis")
                print("="*60)

                sizes_array = np.array([r["size"] for r in results])
                means_array = np.array([r["mean_ms"] for r in results])

# Log - log regression
                log_sizes = np.log10(sizes_array)
                log_times = np.log10(means_array)

                slope, intercept, r_value, p_value, std_err = stats.linregress(
                log_sizes, log_times)

                print(f"\nLog - Log Regression:")
                print(f" Slope: {slope:.4f} ± {std_err:.4f}")
                print(f" R²: {r_value**2:.4f}")
                print(f" p - value: {p_value:.4f}")

# Complexity determination
                if abs(slope) < 0.05:
                    complexity = "O(1)"
                elif abs(slope) < 0.15:
                    complexity = "~O(1) (near constant)"
                elif abs(slope) < 0.5:
                    complexity = f"O(n^{slope:.2f})"
                else:
                    complexity = "O(n) or worse"

                    print(f"\nEmpirical Complexity: {complexity}")
                    print(f"Theoretical: O(1)")

# Performance table
                    print("\n" + "="*60)
                    print("📈 Performance Results")
                    print("="*60)
                    print(f"{"Size":>10} | {"Mean (ms)":>10} | {"Std (ms)":>10} | {"P99 (ms)":>10}")
                    print("-"*50)

                    for r in results:
                        print(
                        f"{
                        r["size"]:>10, } | {
                        r["mean_ms"]:>10.3f} | {
                        r["std_ms"]:>10.3f} | {
                        r["p99_ms"]:>10.3f}")

# Scaling analysis
                        print("\n" + "="*60)
                        print("📊 Scaling Analysis")
                        print("="*60)

                        base_time = results[0]["mean_ms"]
                        print(f"\nScaling relative to {results[0]["size"]:, } vectors:")

                        for r in results:
                            scaling = r["mean_ms"] / base_time
                            print(f" {r["size"]:>10, } vectors: {scaling:>6.3f}x")

# Save results
                            output = {
                            "timestamp": datetime.now().isoformat(),
                            "results": results,
                            "analysis": {
                            "slope": float(slope),
                            "stderr": float(std_err),
                            "r_squared": float(r_value**2),
                            "p_value": float(p_value),
                            "complexity": complexity
                            }
                            }

                            with open("o1_performance_results.json", "w") as f:
                                json.dump(output, f, indent=2)

                                print("\n✅ Results saved to o1_performance_results.json")

# Final verdict
                                print("\n" + "="*60)
                                if abs(slope) < 0.1 and p_value > 0.05:
                                    print("✅ VERDICT: O(1) PERFORMANCE VERIFIED!")
                                    print(" Think AI achieves constant - time vector search")
                                else:
                                    print("⚠️ VERDICT: Performance shows some scaling")
                                    print(f" Empirical complexity: {complexity}")
                                    print("="*60)


                                    if __name__ == "__main__":
                                        verify_o1_performance()
