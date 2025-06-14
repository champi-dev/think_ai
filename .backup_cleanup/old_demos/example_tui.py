#!/usr/bin/env python3
"""Example script to demonstrate the Terminal UI."""

import sys
from think_ai.ui.app import run_ui
from think_ai.core.config import Config


def main():
    """Run the Think AI Terminal UI example."""
    print("🚀 Launching Think AI Terminal UI...")
    print("This provides a rich interactive interface for knowledge management.")
    print("\nControls:")
    print("  - Use arrow keys or mouse to navigate")
    print("  - Press 'q' to quit")
    print("  - Press 'h' to go home")
    print("  - Press 'Escape' to go back\n")
    
    try:
        # Load configuration
        config = Config.from_env()
        
        # Run the TUI
        run_ui(config)
        
    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()