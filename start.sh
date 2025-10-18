#!/bin/bash

# Quick start script - runs both server and client in one terminal using tmux

if ! command -v tmux &> /dev/null; then
    echo "tmux is not installed. Installing dependencies and starting manually..."
    echo ""
    echo "Starting server in background..."
    cd server && npm run dev &
    SERVER_PID=$!

    echo "Starting client..."
    cd ../client && npm run dev

    # Cleanup on exit
    kill $SERVER_PID
else
    echo "Starting AI Chat with tmux..."

    # Create new tmux session
    tmux new-session -d -s ai-chat

    # Split window vertically
    tmux split-window -h

    # Run server in left pane
    tmux select-pane -t 0
    tmux send-keys "cd server && npm run dev" C-m

    # Run client in right pane
    tmux select-pane -t 1
    tmux send-keys "cd client && npm run dev" C-m

    # Attach to session
    tmux attach-session -t ai-chat
fi
