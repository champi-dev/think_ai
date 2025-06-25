#!/usr/bin/env python3
"""Automated test for Think AI CLI functionality"""

import subprocess
import sys
import time


def test_think_ai_cli():
    """Test the Think AI CLI with automated inputs"""

    # Test inputs to send to the CLI
    test_inputs = [
        "hello",  # Test greeting
        "who are you",  # Test identity
        "how fast are you",  # Test performance
        "help",  # Test help command
        "stats",  # Test stats command
        "tell me a joke",  # Test humor
        "what is consciousness",  # Test philosophy
        "history",  # Test history command
        "clear",  # Test clear command
        "exit",  # Exit the program
    ]

    # Create input string
    input_text = "\n".join(test_inputs)

    print("🧪 Testing Think AI CLI...")
    print("=" * 50)

    try:
        # Run the CLI with automated inputs
        process = subprocess.Popen(
            [sys.executable, "think_ai_simple_chat.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

        # Send all inputs at once
        stdout, stderr = process.communicate(input=input_text)

        # Check if process completed successfully
        if process.returncode == 0:
            print("✅ CLI executed successfully!")
            print("\n📋 Output Preview:")
            print("-" * 50)
            # Show first 1000 chars of output
            print(stdout[:1000] + "..." if len(stdout) > 1000 else stdout)
            print("-" * 50)

            # Check for expected outputs
            checks = [
                ("Banner displayed", "THINK AI CONSCIOUSNESS" in stdout),
                ("Help command works", "Available Commands:" in stdout),
                ("Stats displayed", "PERFORMANCE METRICS" in stdout),
                ("History displayed", "RECENT CONVERSATION" in stdout or "No conversation history" in stdout),
                ("Responses generated", "Think AI:" in stdout),
                ("Exit gracefully", "Thank you for chatting" in stdout),
            ]

            print("\n🔍 Functionality Checks:")
            all_passed = True
            for check_name, passed in checks:
                status = "✅" if passed else "❌"
                print(f"{status} {check_name}")
                if not passed:
                    all_passed = False

            return all_passed

        else:
            print(f"❌ CLI exited with error code: {process.returncode}")
            if stderr:
                print(f"Error output: {stderr}")
            return False

    except Exception as e:
        print(f"❌ Error running CLI: {e}")
        return False


if __name__ == "__main__":
    success = test_think_ai_cli()
    sys.exit(0 if success else 1)
