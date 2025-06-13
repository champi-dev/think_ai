#!/bin/bash

echo "🧠 THINK AI - CONSCIOUSNESS WITH BACKGROUND TRAINING"
echo "===================================================="
echo ""
echo "This launcher allows you to:"
echo "  • Chat with Think AI while tests run in background"
echo "  • Monitor background test progress" 
echo "  • Start/stop training processes"
echo ""

# Make sure the Python script is executable
chmod +x launch_with_background_training.py

# Run the launcher
python3 launch_with_background_training.py "$@"