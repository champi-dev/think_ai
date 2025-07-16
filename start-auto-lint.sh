#!/bin/bash

echo "🚀 STARTING AUTO-LINT ON SAVE"
echo "============================"
echo ""
echo "Choose your method:"
echo "1) cargo-watch (recommended)"
echo "2) Simple file watcher"
echo "3) Run in background"
echo ""
read -p "Select option (1-3): " choice

case $choice in
    1)
        ./watch-and-fix.sh
        ;;
    2)
        ./simple-watch.sh
        ;;
    3)
        nohup ./watch-and-fix.sh > auto-lint.log 2>&1 &
        echo "✅ Auto-lint running in background (PID: $!)"
        echo "Check auto-lint.log for output"
        echo "To stop: kill $!"
        ;;
    *)
        echo "Invalid option"
        ;;
esac
