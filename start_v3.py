#!/usr/bin/env python3
"""
Start script that ensures Think AI v3.1.0 runs
Prevents fallback to broken original code
"""

import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Ensure we're in the right directory
if os.path.exists("think_ai_v3/app.py"):
    logger.info("Starting Think AI v3.1.0...")

    # Set environment variables
    os.environ["PYTHONUNBUFFERED"] = "1"
    if not os.environ.get("THINK_AI_COLOMBIAN"):
        os.environ["THINK_AI_COLOMBIAN"] = "true"

    # Import and run v3
    try:
        # Add v3 to path
        sys.path.insert(0, ".")

        # Import the v3 app
        from think_ai_v3.app import main

        # Run it
        main()
    except ImportError:
        # If main doesn't exist, run the module directly
        import subprocess

        subprocess.run([sys.executable, "think_ai_v3/app.py"])
else:
    logger.error("Think AI v3 not found! Directory structure:")
    os.system("ls -la")
    logger.error("Cannot start Think AI v3.1.0")
    sys.exit(1)
