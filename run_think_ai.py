#!/usr/bin/env python3
"""Simple launcher for Think AI CLI."""

import sys
import asyncio
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

# Import and run CLI
from think_ai.cli.main import main

if __name__ == "__main__":
    asyncio.run(main())