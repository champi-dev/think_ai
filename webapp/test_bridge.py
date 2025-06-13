#!/usr/bin/env python3

import sys
import traceback

from think_ai.api.bridge import ThinkAIBridge

sys.path.insert(0, "/home/administrator/development/think_ai")

try:
    print("Bridge import successful")
    bridge = ThinkAIBridge()
    print("Bridge initialized successfully")
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()
