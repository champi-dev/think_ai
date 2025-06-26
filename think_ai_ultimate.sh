#!/bin/bash

# Ultimate Think AI launcher with chat + fullstack

echo "╔═══════════════════════════════════════════════════════════════════════╗"
echo "║              🧠 THINK AI ULTIMATE QUANTUM EXPERIENCE                   ║"
echo "╠═══════════════════════════════════════════════════════════════════════╣"
echo "║     Chat + 3D Visualization + API - All in One Command!               ║"
echo "╚═══════════════════════════════════════════════════════════════════════╝"
echo

# Start fullstack in background
./launch_fullstack.sh &
FULLSTACK_PID=$!

# Wait a bit for services to start
sleep 3

echo
echo "╔═══════════════════════════════════════════════════════════════════════╗"
echo "║                      🧠 THINK AI CHAT INTERFACE                        ║"
echo "╠═══════════════════════════════════════════════════════════════════════╣"
echo "║  While you chat here, visit the 3D interface at:                      ║"
echo "║  🌐 http://localhost:8000/fullstack_3d.html                           ║"
echo "╚═══════════════════════════════════════════════════════════════════════╝"
echo

# Start chat
./target/release/think-ai chat

# Cleanup on exit
kill $FULLSTACK_PID 2>/dev/null || true