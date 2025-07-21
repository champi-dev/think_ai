# Manual Deployment Steps

## 1. Build the New Binary

```bash
# Clean old artifacts
cargo clean --release --package think-ai-full

# Build production binary
cargo build --release --bin think-ai-full-production
```

## 2. Stop Current Service

```bash
# Check current status
sudo systemctl status thinkai

# Stop the service
sudo systemctl stop thinkai

# Verify it's stopped
sudo systemctl status thinkai
```

## 3. Deploy New Binary

```bash
# Copy new binary
sudo cp target/release/think-ai-full-production /opt/thinkai/

# Make it executable
sudo chmod +x /opt/thinkai/think-ai-full-production

# Copy updated dashboard
sudo cp full-system/static/stats-dashboard.html /opt/thinkai/full-system/static/
```

## 4. Restart Service

```bash
# Reload systemd configuration
sudo systemctl daemon-reload

# Start the service
sudo systemctl start thinkai

# Check status
sudo systemctl status thinkai

# View logs
sudo journalctl -u thinkai -f
```

## 5. Verify Deployment

```bash
# Test locally
curl http://localhost:7777/health
curl http://localhost:7777/api/metrics

# Test production
curl https://thinkai.lat/health
curl https://thinkai.lat/api/metrics
```

## 6. Check Dashboard

Open https://thinkai.lat/stats and verify:
- Numbers are displaying (no graphs)
- Metrics are updating
- Mobile view works properly

## If Something Goes Wrong

```bash
# Check logs
sudo journalctl -u thinkai -n 100

# Restart service
sudo systemctl restart thinkai

# Rollback if needed
sudo cp /opt/thinkai/think-ai-full-production.backup /opt/thinkai/think-ai-full-production
sudo systemctl restart thinkai
```