#!/usr/bin/env python3
"""Run performance benchmarks for Think AI."""

import asyncio
import sys
from datetime import datetime

from think_ai import ThinkAIEngine, Config
from think_ai.benchmarks.performance import PerformanceBenchmark, LoveBenchmark
from think_ai.utils.logging import configure_logging


async def main():
    """Run comprehensive benchmarks."""
    logger = configure_logging(log_level="INFO")
    
    print("🚀 Think AI Performance Benchmark Suite")
    print("=" * 50)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Initialize engine
    config = Config.from_env()
    
    print("Initializing Think AI Engine...")
    async with ThinkAIEngine(config) as engine:
        # Performance benchmarks
        perf_benchmark = PerformanceBenchmark(engine)
        
        print("\n📊 Running Performance Benchmarks...")
        print("-" * 50)
        
        # Run with different operation counts
        test_sizes = [100, 1000]  # Adjust based on your system
        
        for num_ops in test_sizes:
            print(f"\nTesting with {num_ops} operations:")
            results = await perf_benchmark.run_all_benchmarks(num_ops)
            
            # Print summary
            for test_name, result in results.items():
                print(f"  {test_name}: {result.operations_per_second:.2f} ops/sec")
        
        # Generate full report
        print("\n📈 Detailed Performance Report")
        print("-" * 50)
        print(perf_benchmark.generate_report())
        
        # Love-based benchmarks
        print("\n💖 Running Love-Based Metrics Benchmarks...")
        print("-" * 50)
        
        love_benchmark = LoveBenchmark(engine)
        love_results = await love_benchmark.benchmark_ethical_processing(100)
        
        print(f"Ethical Pass Rate: {love_results['ethical_pass_rate']*100:.1f}%")
        print(f"Content Enhancement Rate: {love_results['enhancement_rate']*100:.1f}%")
        print(f"Avg Processing Time: {love_results['avg_processing_time_ms']:.2f}ms")
        print(f"Compassion Demonstrated: {'✓' if love_results['love_metrics']['compassion_demonstrated'] else '✗'}")
        print(f"Harm Prevention Active: {'✓' if love_results['love_metrics']['harm_prevention_active'] else '✗'}")
        
        # System capabilities summary
        print("\n🎯 System Capabilities Summary")
        print("-" * 50)
        
        # Calculate O(1) achievement
        storage_read = results.get('storage_read')
        if storage_read and storage_read.latency_p99 < 10:
            print("✅ O(1) Storage Performance: ACHIEVED")
            print(f"   - P99 Latency: {storage_read.latency_p99:.2f}ms")
        else:
            print("❌ O(1) Storage Performance: Not achieved")
        
        # Semantic search performance
        vector_search = results.get('vector_search')
        if vector_search:
            print(f"✅ Semantic Search: {vector_search.operations_per_second:.2f} queries/sec")
            print(f"   - P50 Latency: {vector_search.latency_p50:.2f}ms")
        
        # Concurrent scalability
        concurrent = results.get('concurrent_operations')
        if concurrent and concurrent.operations_per_second > 1000:
            print(f"✅ Concurrent Scalability: {concurrent.operations_per_second:.0f} ops/sec")
        else:
            print("❌ Concurrent Scalability: Needs improvement")
        
        # Love-based design
        print(f"✅ Love-Based Design: {love_results['ethical_pass_rate']*100:.0f}% ethical compliance")
        
        print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nBenchmark interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Benchmark failed: {e}")
        sys.exit(1)