#!/bin/bash

echo "=== EVIDENCE OF CURRENT STATE ==="
echo "================================="
echo

echo "1. Current running processes:"
ps aux | grep -E "(think-ai|ngrok)" | grep -v grep
echo

echo "2. Port 8080 status:"
sudo lsof -i :8080
echo

echo "3. Frontend code check (looking for JSON parsing):"
echo "   Local file (minimal_3d.html):"
grep -c "data\.chunk" /home/administrator/think_ai/minimal_3d.html
echo "   Static directory file:"
if [ -f /home/administrator/think_ai/static/index.html ]; then
    grep -c "data\.chunk" /home/administrator/think_ai/static/index.html
else
    echo "   File not found: /home/administrator/think_ai/static/index.html"
fi
echo

echo "4. What's being served at thinkai.lat:"
curl -s https://thinkai.lat 2>&1 | grep -E "(data\.chunk|Think AI|quantum_3d)" | head -5
echo

echo "5. API test - Streaming endpoint:"
curl -s -X POST https://thinkai.lat/api/chat/stream \
    -H "Content-Type: application/json" \
    -d '{"message": "test", "session_id": "test123"}' \
    --max-time 5 2>&1 | head -3
echo

echo "6. Last 5 server log entries:"
tail -5 /home/administrator/think_ai/webapp_server.log
echo

echo "7. Systemd service status:"
systemctl is-active think-ai.service

echo
echo "=== END OF EVIDENCE ==="