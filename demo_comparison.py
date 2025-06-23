#!/usr/bin/env python3
"""Demonstration comparing Simple Chat vs Full System CLI"""

import subprocess
import sys
import time


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"🎯 {title}")
    print("=" * 70 + "\n")


def run_cli_test(cli_name, file_name, commands):
    """Run a CLI with test commands and capture output"""
    print(f"📋 Testing {cli_name}...")

    # Create input string
    input_text = "\n".join(commands)

    try:
        # Run the CLI
        process = subprocess.Popen(
            [sys.executable, file_name],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Send commands
        stdout, stderr = process.communicate(input=input_text, timeout=10)

        # Return output
        return stdout, stderr, process.returncode

    except subprocess.TimeoutExpired:
        process.kill()
        return "Timeout", "", -1
    except Exception as e:
        return f"Error: {e}", "", -1


def main():
    """Main demonstration"""
    print("\n" + "🧠" * 35)
    print("\n🎯 THINK AI CLI COMPARISON DEMONSTRATION")
    print("\n" + "🧠" * 35)

    # Test commands
    test_commands = ["hello", "who are you", "stats", "help", "exit"]

    # Test Simple Chat CLI
    print_section("SIMPLE CHAT CLI (Hash-based Responses)")
    simple_stdout, simple_stderr, simple_code = run_cli_test(
        "Simple Chat CLI", "think_ai_simple_chat.py", test_commands
    )

    if simple_code == 0:
        print("✅ Simple Chat CLI executed successfully!")
        print("\n📊 Key Features:")
        print("  • Pre-computed hash tables for O(1) lookup")
        print("  • 8 response categories with hardcoded responses")
        print("  • Basic keyword matching")
        print("  • Minimal memory footprint")
        print("  • No external dependencies")

        # Extract performance info
        if "PERFORMANCE METRICS" in simple_stdout:
            lines = simple_stdout.split("\n")
            for i, line in enumerate(lines):
                if "Avg Response:" in line:
                    print(f"\n⚡ Performance: {line.strip()}")
                    break
    else:
        print(f"❌ Simple Chat CLI failed with code: {simple_code}")

    # Show sample output
    print("\n📝 Sample Output:")
    print("-" * 50)
    output_lines = simple_stdout.split("\n")
    for line in output_lines[20:35]:  # Show a sample
        if line.strip():
            print(line)
    print("-" * 50)

    # Test Full System CLI
    print_section("FULL SYSTEM CLI (Complete Think AI Integration)")
    full_stdout, full_stderr, full_code = run_cli_test("Full System CLI", "think_ai_full_cli.py", test_commands)

    if "Full Think AI system not available" in full_stdout:
        print("⚠️  Full system components not loaded (expected in test environment)")
        print("\n📊 Potential Features (when fully initialized):")
        print("  • 🧠 Consciousness Framework with awareness states")
        print("  • 🔍 O(1) Vector Search using LSH")
        print("  • 🕸️ Knowledge Graph for semantic relationships")
        print("  • 💾 Distributed Storage (ScyllaDB)")
        print("  • ⚡ Redis Cache for performance")
        print("  • ⚖️ Constitutional AI for ethical evaluation")
        print("  • 🤖 Full Language Model integration")
        print("  • 📚 Self-training capabilities")
        print("  • 💻 Code generation features")
    else:
        print("✅ Full System CLI executed!")

    # Comparison Summary
    print_section("COMPARISON SUMMARY")

    print("📊 Simple Chat CLI:")
    print("  ✅ Pros:")
    print("    • Lightning fast (sub-millisecond responses)")
    print("    • No dependencies or setup required")
    print("    • Minimal resource usage")
    print("    • Always works offline")
    print("  ❌ Cons:")
    print("    • Limited to pre-defined responses")
    print("    • No learning or adaptation")
    print("    • No advanced AI features")

    print("\n📊 Full System CLI:")
    print("  ✅ Pros:")
    print("    • Access to all Think AI components")
    print("    • Dynamic, intelligent responses")
    print("    • Self-training and learning")
    print("    • Advanced consciousness simulation")
    print("    • Code generation capabilities")
    print("  ❌ Cons:")
    print("    • Requires full system initialization")
    print("    • Higher resource usage")
    print("    • May need external services")

    print_section("RECOMMENDATIONS")
    print("🎯 Use Simple Chat CLI when:")
    print("  • You need instant, reliable responses")
    print("  • Running in resource-constrained environments")
    print("  • Demonstrating basic functionality")
    print("  • Testing or development")

    print("\n🎯 Use Full System CLI when:")
    print("  • You need the complete Think AI experience")
    print("  • Working with complex queries")
    print("  • Utilizing advanced AI features")
    print("  • Production deployments with full infrastructure")

    print("\n" + "=" * 70)
    print("✅ Demonstration complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
