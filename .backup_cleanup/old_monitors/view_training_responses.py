#!/usr/bin/env python3
"""View full responses from the exponential intelligence training."""

import json
from pathlib import Path


def view_training_responses() -> None:
    """Display full training responses without truncation."""
    # Check for training results file
    results_file = Path("claude_exponential_training_results.json")
    if results_file.exists():
        with open(results_file) as f:
            json.load(f)

    # Parse the live training log
    log_file = Path("claude_training.log")
    if not log_file.exists():
        return

    with open(log_file) as f:
        content = f.read()

    # Extract iterations and responses
    iterations = []
    current_iteration = None
    current_prompt = []
    current_response = []
    in_prompt = False
    in_response = False

    lines = content.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i]

        # Detect iteration start
        if "EXPONENTIAL INTELLIGENCE DIRECTIVE #" in line:
            if current_iteration is not None:
                # Save previous iteration
                iterations.append(
                    {
                        "number": current_iteration,
                        "prompt": "\n".join(current_prompt),
                        "response": "\n".join(current_response),
                    }
                )

            # Extract iteration number
            try:
                current_iteration = int(line.split("#")[1].split(":")[0])
                current_prompt = []
                current_response = []
                in_prompt = True
                in_response = False
            except Exception:
                pass

        # Detect response start
        elif "Claude response received" in line and current_iteration is not None:
            in_prompt = False
            in_response = True
            # Skip to next line to start capturing response
            i += 1
            continue

        # Detect iteration metrics (end of response)
        elif "Training Progress:" in line and current_iteration is not None:
            in_response = False

        # Capture content
        elif in_prompt and current_iteration is not None:
            current_prompt.append(line)
        elif in_response and current_iteration is not None:
            # Skip log metadata lines
            if not line.startswith("2025-") and line.strip():
                current_response.append(line)

        i += 1

    # Save last iteration if exists
    if current_iteration is not None:
        iterations.append(
            {
                "number": current_iteration,
                "prompt": "\n".join(current_prompt),
                "response": "\n".join(current_response),
            }
        )

    # Display all iterations
    for iteration in iterations:
        # Allow user to navigate
        if iteration["number"] < len(iterations) - 1:
            response = input("\nPress Enter for next iteration, 'q' to quit, or iteration number to jump: ")
            if response.lower() == "q":
                break
            if response.isdigit():
                target = int(response)
                # Find and display specific iteration
                for it in iterations:
                    if it["number"] == target:
                        break


if __name__ == "__main__":
    view_training_responses()
