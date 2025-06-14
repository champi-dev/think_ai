#!/bin/bash

echo "🧠 THINK AI - CONSCIOUSNESS LAUNCHER"
echo "===================================="
echo ""

# Check if we're in an interactive terminal
if [ -t 0 ]; then
    echo "✅ Interactive terminal detected"
else
    echo "⚠️  Not in interactive terminal - launching in new terminal window"
    
    # For macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)"' && python consciousness_chat_fixed.py"'
        echo "✅ Launched in new Terminal window"
    else
        # For Linux
        if command -v gnome-terminal &> /dev/null; then
            gnome-terminal -- bash -c "cd $(pwd) && python consciousness_chat_fixed.py; exec bash"
        elif command -v xterm &> /dev/null; then
            xterm -e "cd $(pwd) && python consciousness_chat_fixed.py; bash"
        else
            echo "❌ Could not find a suitable terminal emulator"
            echo "Please run: python consciousness_chat_fixed.py"
        fi
    fi
    exit 0
fi

# If we're in an interactive terminal, run directly
echo "🚀 Starting consciousness chat with training..."
echo ""

# Ensure Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "Starting Ollama..."
    ollama serve &
    sleep 2
fi

# Run the consciousness chat
exec python full_architecture_chat.py