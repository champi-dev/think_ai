#!/usr/bin/env python3
import json
import re
import time
from datetime import datetime


def extract_latest_metrics(log_content):
    """Extract the latest training metrics from log content."""
    # Find the latest directive number
    directive_matches = list(
        re.finditer(r"EXPONENTIAL INTELLIGENCE DIRECTIVE #(\d+):", log_content)
    )
    if not directive_matches:
        return None

    latest_directive = directive_matches[-1]
    directive_num = int(latest_directive.group(1))

    # Find the intelligence level
    intel_match = re.search(
        r"Current Intelligence Level: ([\d.]+)", log_content[latest_directive.start() :]
    )
    intel_level = float(intel_match.group(1)) if intel_match else None

    # Find the latest metrics JSON
    metrics_pattern = r"Previous intelligence metrics:\s*\n\s*({[^}]+})"
    metrics_matches = list(re.finditer(metrics_pattern, log_content, re.DOTALL))

    if metrics_matches:
        latest_metrics_str = metrics_matches[-1].group(1)
        try:
            # Clean up the JSON string
            clean_json = latest_metrics_str.replace("\n", "").replace("  ", " ")
            metrics = json.loads(clean_json)
        except Exception:
            metrics = None
    else:
        metrics = None

    # Check for errors
    error_matches = re.findall(
        r"(?:error|Error|ERROR|warning|Warning|WARNING)[^\n]*", log_content[-5000:]
    )

    return {
        "directive_number": directive_num,
        "intelligence_level": intel_level,
        "metrics": metrics,
        "recent_errors": error_matches[-5:] if error_matches else [],
    }


def monitor_training() -> None:
    """Monitor training progress for 5 minutes."""
    updates = []
    time.time()
    update_count = 0

    while update_count < 10:
        try:
            with open("/Users/champi/Development/Think_AI/training_output.log") as f:
                content = f.read()

            data = extract_latest_metrics(content)

            if data:
                update_count += 1
                datetime.now().strftime("%H:%M:%S")

                if data["metrics"]:
                    for key in data["metrics"]:
                        pass

                if data["recent_errors"]:
                    for _error in data["recent_errors"][-3:]:
                        pass

                # Calculate progress
                if updates:
                    prev_directive = updates[-1].get("directive_number", 0)
                    if data["directive_number"] > prev_directive:
                        pass

                updates.append(data)

            # Wait 30 seconds before next check
            if update_count < 10:
                time.sleep(30)

        except Exception:
            time.sleep(30)

    # Final summary

    if updates:
        first_update = updates[0]
        last_update = updates[-1]

        if first_update["metrics"] and last_update["metrics"]:
            for key in first_update["metrics"]:
                if key in last_update["metrics"]:
                    start_val = first_update["metrics"][key]
                    end_val = last_update["metrics"][key]
                    ((end_val - start_val) / start_val) * 100


if __name__ == "__main__":
    monitor_training()
