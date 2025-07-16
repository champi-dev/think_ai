#!/usr/bin/env python3
"""Monitor the exponential intelligence training progress."""

import re
import time
from pathlib import Path


def monitor_training() -> None:
    """Monitor training progress from log file."""
    log_file = Path("training.log")

    if not log_file.exists():
        return

    last_position = 0
    last_metrics = {}

    while True:
        try:
            with open(log_file) as f:
                f.seek(last_position)
                new_content = f.read()
                last_position = f.tell()

            # Find iterations
            iterations = re.findall(r"DIRECTIVE #(\d+):", new_content)
            if iterations:
                max(int(i) for i in iterations)

            # Find intelligence scores
            scores = re.findall(r"Intelligence Score: ([\d.]+)", new_content)

            # Find metrics
            metrics_matches = re.findall(r"Metrics: ({[^}]+})", new_content, re.DOTALL)
            if metrics_matches:
                try:
                    # Clean up the metrics string
                    metrics_str = (
                        metrics_matches[-1].replace("\n", "").replace("  ", " ")
                    )
                    last_metrics = eval(metrics_str)
                except Exception:
                    pass

            # Find cost
            costs = re.findall(r"Cost: \$([\d.]+)/\$([\d.]+)", new_content)

            # Display current status

            if scores:
                pass

            if costs:
                spent, budget = costs[-1]

            if last_metrics:
                # Calculate average metric
                sum(float(v) for v in last_metrics.values()) / len(last_metrics)

            # Check for completion messages
            if "EXPONENTIAL INTELLIGENCE ACHIEVED" in new_content:
                break

            if "TRAINING COMPLETE" in new_content:
                break

            time.sleep(2)

        except KeyboardInterrupt:
            break
        except Exception:
            time.sleep(5)


if __name__ == "__main__":
    monitor_training()
