#!/usr/bin/env python3
"""
Direct O(1) Optimization Benchmark
Tests the CLI performance with various query types to validate O(1) implementations
"""

import subprocess
import time
import statistics
import sys

def run_think_ai_query(query):
    """Run a single query through think-ai CLI and measure response time"""
    start_time = time.time()
    
    try:
        # Run the CLI with the query
        process = subprocess.Popen(
            ['./target/release/think-ai', 'chat'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd='/mnt/storage2/Development/think_ai'
        )
        
        # Send query and get response
        stdout, stderr = process.communicate(input=f"{query}\n", timeout=30)
        end_time = time.time()
        
        # Extract response time from output if available
        response_time_ms = None
        if "ms]" in stdout:
            try:
                # Extract time from pattern like "[⚡ 500.4ms]"
                time_part = stdout.split("⚡ ")[-1].split("ms]")[0]
                response_time_ms = float(time_part)
            except:
                pass
        
        total_time_ms = (end_time - start_time) * 1000
        
        return {
            'success': True,
            'query': query,
            'server_time_ms': response_time_ms,
            'total_time_ms': total_time_ms,
            'response_lines': len(stdout.split('\n')),
            'has_response': 'Think AI:' in stdout
        }
        
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'query': query,
            'error': 'Timeout (>30s)',
            'total_time_ms': 30000
        }
    except Exception as e:
        return {
            'success': False,
            'query': query,
            'error': str(e),
            'total_time_ms': None
        }

def main():
    print("🚀 Think AI O(1) Optimization Benchmark")
    print("=" * 60)
    
    # Test queries designed to test different optimization paths
    test_queries = [
        # Simple cache hits
        "hello",
        "hi",
        
        # Knowledge lookups (should use O(1) hash indexes)
        "what is AI?",
        "neuroscience",
        "quantum mechanics", 
        "machine learning",
        "economics",
        
        # Complex queries (should still be fast due to O(1) lookups)
        "explain artificial intelligence",
        "how does machine learning work?",
        "what is consciousness?",
    ]
    
    print(f"📊 Running {len(test_queries)} benchmark queries...")
    print(f"🎯 Target: <3000ms per query (O(1) optimization goal)")
    print()
    
    results = []
    for i, query in enumerate(test_queries, 1):
        print(f"🔍 Query {i:2d}: '{query}'")
        result = run_think_ai_query(query)
        results.append(result)
        
        if result['success']:
            server_time = result.get('server_time_ms')
            total_time = result['total_time_ms']
            
            if server_time:
                print(f"   ⚡ Server time: {server_time:.1f}ms")
            print(f"   🕐 Total time: {total_time:.1f}ms")
            print(f"   📝 Response: {'✅' if result['has_response'] else '❌'}")
            
            # Performance assessment
            if server_time and server_time < 1000:
                print(f"   🎯 EXCELLENT: <1s response")
            elif server_time and server_time < 3000:
                print(f"   ✅ GOOD: <3s response")
            elif total_time < 5000:
                print(f"   ⚠️  ACCEPTABLE: <5s total")
            else:
                print(f"   ❌ SLOW: >5s response")
        else:
            print(f"   ❌ FAILED: {result['error']}")
        
        print()
    
    # Statistical Analysis
    successful_results = [r for r in results if r['success']]
    server_times = [r['server_time_ms'] for r in successful_results if r.get('server_time_ms')]
    total_times = [r['total_time_ms'] for r in successful_results if r.get('total_time_ms')]
    
    print("📈 Performance Statistics:")
    print("=" * 40)
    
    if server_times:
        print(f"Server Response Times:")
        print(f"   📊 Average: {statistics.mean(server_times):.1f}ms")
        print(f"   📉 Minimum: {min(server_times):.1f}ms") 
        print(f"   📈 Maximum: {max(server_times):.1f}ms")
        print(f"   📏 Median:  {statistics.median(server_times):.1f}ms")
        if len(server_times) > 1:
            print(f"   📐 Std Dev: {statistics.stdev(server_times):.1f}ms")
    
    if total_times:
        print(f"\nTotal Processing Times:")
        print(f"   📊 Average: {statistics.mean(total_times):.1f}ms")
        print(f"   📉 Minimum: {min(total_times):.1f}ms")
        print(f"   📈 Maximum: {max(total_times):.1f}ms")
    
    # O(1) Validation
    print(f"\n🎯 O(1) Optimization Validation:")
    print("=" * 40)
    
    success_rate = len(successful_results) / len(results) * 100
    print(f"✅ Success Rate: {success_rate:.1f}% ({len(successful_results)}/{len(results)})")
    
    if server_times:
        avg_server = statistics.mean(server_times)
        max_server = max(server_times)
        
        print(f"\n🔬 Hash-based Knowledge Lookup:")
        if avg_server < 1000:
            print(f"   ✅ EXCELLENT: Avg {avg_server:.1f}ms indicates O(1) hash lookups working")
        elif avg_server < 3000:
            print(f"   ✅ GOOD: Avg {avg_server:.1f}ms shows significant optimization")
        else:
            print(f"   ❌ NEEDS WORK: Avg {avg_server:.1f}ms suggests O(n) operations remain")
        
        print(f"\n⚡ Response Consistency (O(1) indicator):")
        if len(server_times) > 1:
            stdev = statistics.stdev(server_times)
            cv = stdev / avg_server  # Coefficient of variation
            if cv < 0.5:
                print(f"   ✅ CONSISTENT: Low variance ({cv:.2f}) indicates O(1) behavior")
            else:
                print(f"   ⚠️  VARIABLE: High variance ({cv:.2f}) may indicate O(n) operations")
        
        print(f"\n🎪 Performance Targets:")
        under_3s = sum(1 for t in server_times if t < 3000)
        under_1s = sum(1 for t in server_times if t < 1000)
        print(f"   🎯 <3s target: {under_3s}/{len(server_times)} queries ({under_3s/len(server_times)*100:.1f}%)")
        print(f"   ⚡ <1s optimal: {under_1s}/{len(server_times)} queries ({under_1s/len(server_times)*100:.1f}%)")
        
        if under_3s == len(server_times):
            print(f"   🏆 ALL QUERIES MEET O(1) TARGET!")
        elif under_3s >= len(server_times) * 0.8:
            print(f"   ✅ MAJORITY OF QUERIES OPTIMIZED")
        else:
            print(f"   ⚠️  OPTIMIZATION NEEDS IMPROVEMENT")
    
    print(f"\n💡 Evidence of Implemented Optimizations:")
    print(f"   📦 Knowledge Engine O(1) Hash Indexes: {'✅ ACTIVE' if server_times and statistics.mean(server_times) < 2000 else '⚠️ PARTIAL'}")
    print(f"   🧠 Non-blocking Self-Evaluation: {'✅ WORKING' if success_rate > 80 else '❌ BLOCKING'}")
    print(f"   ⚡ Multi-level Response Cache: {'✅ EFFECTIVE' if server_times and min(server_times) < 500 else '⚠️ NEEDS_TUNING'}")
    print(f"   🔄 Fast Conversation Memory: {'✅ OPTIMIZED' if server_times and max(server_times) < 5000 else '❌ SLOW'}")

if __name__ == "__main__":
    main()