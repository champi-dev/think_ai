#!/usr/bin/env python3
"""Pre-commit QA Environment - Manual testing interface for Think AI."""

import subprocess
import sys

# Use the browser-based QA environment
if __name__ == "__main__":
    result = subprocess.run([sys.executable, "scripts/precommit_qa_environment_browser.py"])
    sys.exit(result.returncode)
