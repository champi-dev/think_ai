#!/bin/bash
echo "Restarting Think AI Quantum Server..."
pkill -f full-working-o1 || true
pkill -f start-quantum-server.sh || true
sleep 2
./start-quantum-server.sh
