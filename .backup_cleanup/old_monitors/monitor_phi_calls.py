#!/usr/bin/env python3
"""Monitor Phi-3.5 calls in real-time."""

import subprocess
import time
from datetime import datetime


def monitor_ollama() -> None:
    """Monitor Ollama/Phi-3.5 calls."""
    last_log_line = None

    try:
        while True:
            # Check Ollama logs
            try:
                # Get last few lines of training output
                result = subprocess.run(
                    ["tail", "-20", "training_output.log"],
                    check=False,
                    capture_output=True,
                    text=True,
                )

                if result.stdout:
                    for line in result.stdout.split("\n"):
                        if "Phi-3.5 Mini" in line and line != last_log_line:
                            datetime.now().strftime("%H:%M:%S")
                            last_log_line = line

                # Also check if Ollama is running
                ps_result = subprocess.run(
                    ["ps", "aux"],
                    check=False,
                    capture_output=True,
                    text=True,
                )

                if "ollama" in ps_result.stdout:
                    # Check Ollama API status
                    api_check = subprocess.run(
                        ["curl", "-s", "http://localhost:11434/api/tags"],
                        check=False,
                        capture_output=True,
                        text=True,
                    )

                    if "phi3" in api_check.stdout:
                        pass
                    else:
                        pass

            except Exception:
                pass

            time.sleep(2)

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    monitor_ollama()
