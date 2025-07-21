#!/bin/bash

# PRODUCTION DEPLOYMENT COMMANDS
# Run these commands on your production server

echo "🚀 Production Deployment Commands"
echo "================================"
echo ""
echo "Run these commands:"
echo ""

cat << 'EOF'
# 1. Stop the current service
sudo systemctl stop thinkai

# 2. Backup old binary (optional but recommended)
sudo cp /opt/thinkai/think-ai-full-production /opt/thinkai/think-ai-full-production.backup

# 3. Copy new binary from your local machine to server
# From your LOCAL machine, run:
scp /home/champi/Dev/think_ai/target/release/think-ai-full-production YOUR_SERVER:/tmp/

# 4. On the SERVER, move the binary to the correct location
sudo mv /tmp/think-ai-full-production /opt/thinkai/
sudo chmod +x /opt/thinkai/think-ai-full-production

# 5. Copy updated dashboard from LOCAL to server
# From your LOCAL machine, run:
scp /home/champi/Dev/think_ai/full-system/static/stats-dashboard.html YOUR_SERVER:/tmp/

# 6. On the SERVER, move the dashboard
sudo mkdir -p /opt/thinkai/full-system/static
sudo mv /tmp/stats-dashboard.html /opt/thinkai/full-system/static/

# 7. Reload systemd and start service
sudo systemctl daemon-reload
sudo systemctl start thinkai

# 8. Check status
sudo systemctl status thinkai

# 9. Test endpoints
curl http://localhost:7777/health
curl http://localhost:7777/api/metrics | jq .

# 10. Check production
curl https://thinkai.lat/health
curl https://thinkai.lat/api/metrics | jq '.system_metrics'

# 11. View logs if needed
sudo journalctl -u thinkai -f
EOF

echo ""
echo "📊 After deployment, check https://thinkai.lat/stats"
echo "   - Should show simple numbers (no graphs)"
echo "   - Metrics should start incrementing"
echo "   - Mobile view should work properly"