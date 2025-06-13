#!/usr/bin/env python3
"""Example script to demonstrate the Terminal UI."""

import sys

from think_ai.core.config import Config
from think_ai.ui.app import run_ui

def main() -> None:
    """Run the Think AI Terminal UI example."""
    try:
        # Load configuration
        config = Config.from_env()

        # Run the TUI
        run_ui(config)

    except KeyboardInterrupt:
        sys.exit(0)
    except Exception:
        sys.exit(1)

if __name__ == "__main__":
    main()
