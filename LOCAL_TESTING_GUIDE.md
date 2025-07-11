# Local Testing Guide for Think AI on Cloud GPU Server

This guide helps you test Think AI running on a cloud GPU server from your local machine.

## Quick Start

1. **Get your cloud server's IP address**
   ```bash
   # On cloud server
   curl ifconfig.me
   ```

2. **Choose a connection method:**

### Method 1: Direct Connection (Simple but less secure)
```bash
# Run this on your local machine
./test-from-local.sh <CLOUD_SERVER_IP>

# Example:
./test-from-local.sh 123.45.67.89
```

### Method 2: SSH Tunnel (Recommended for security)
```bash
# On your local machine, create SSH tunnel
ssh -L 7777:localhost:8080 user@<CLOUD_SERVER_IP>

# In another terminal, test locally
./test-from-local.sh localhost 7777

# Or use the helper script
./ssh-tunnel-helper.sh ubuntu 123.45.67.89
```

### Method 3: Using Python Test Client
```bash
# With SSH tunnel active
python3 test-client.py

# Or direct connection
python3 test-client.py http://123.45.67.89:8080
```

## Available Test Scripts

### 1. **test-from-local.sh** - Basic connectivity and health checks
```bash
./test-from-local.sh <IP> [PORT] [LOCAL_PORT]
```
- Tests server connectivity
- Checks all endpoints
- Runs performance benchmarks
- Provides SSH tunnel instructions

### 2. **test-all-endpoints.sh** - Comprehensive endpoint testing
```bash
# Through SSH tunnel
./test-all-endpoints.sh http://localhost:7777

# Direct connection
./test-all-endpoints.sh http://123.45.67.89:8080

# With verbose output
./test-all-endpoints.sh http://localhost:7777 true
```
- Tests all API endpoints
- Verifies O(1) performance
- Stress tests with concurrent requests
- Provides detailed performance metrics

### 3. **test-client.py** - Interactive Python client
```bash
# Interactive chat mode
python3 test-client.py

# Benchmark mode (type 'bench' in interactive mode)
python3 test-client.py http://123.45.67.89:8080
```

## Secure Access Options

### SSH Tunnel (Recommended)
```bash
# Basic tunnel
ssh -L 7777:localhost:8080 user@cloud-server

# With compression (for slow connections)
ssh -C -L 7777:localhost:8080 user@cloud-server

# Multiple ports
ssh -L 7777:localhost:8080 -L 7778:localhost:8081 user@cloud-server
```

### Ngrok (Temporary public access)
```bash
# On cloud server
ngrok http 8080

# Use the provided URL from anywhere
```

### Tailscale (Persistent secure network)
```bash
# Install on both machines
curl -fsSL https://tailscale.com/install.sh | sh

# Access using Tailscale IP (100.x.x.x)
```

## Testing Checklist

1. **Server Health**
   - [ ] Server is running: `cargo run --release --bin think-ai-http`
   - [ ] Port 8080 is open on cloud server
   - [ ] Firewall allows incoming connections

2. **Local Setup**
   - [ ] Scripts are executable: `chmod +x *.sh`
   - [ ] Python 3 installed for test client
   - [ ] curl and bc installed for bash scripts

3. **Performance Verification**
   - [ ] Response times < 10ms (O(1) performance)
   - [ ] Concurrent requests handled smoothly
   - [ ] Memory usage stable under load

## Troubleshooting

### Connection Refused
```bash
# Check if server is running
ssh user@cloud-server "ps aux | grep think-ai"

# Check if port is listening
ssh user@cloud-server "netstat -tlnp | grep 8080"

# Check firewall
ssh user@cloud-server "sudo ufw status"
```

### Slow Performance
```bash
# Test network latency
ping -c 10 cloud-server-ip

# Use compression for SSH tunnel
ssh -C -L 7777:localhost:8080 user@cloud-server
```

### SSL/TLS Issues
```bash
# For HTTPS, use proper certificates or SSH tunnel
# SSH tunnel automatically encrypts traffic
```

## Example Testing Session

```bash
# 1. Start SSH tunnel
./ssh-tunnel-helper.sh ubuntu 123.45.67.89

# 2. In new terminal, run basic tests
./test-from-local.sh localhost 7777

# 3. Run comprehensive tests
./test-all-endpoints.sh http://localhost:7777 true

# 4. Interactive testing
python3 test-client.py

# 5. Close SSH tunnel with Ctrl+C when done
```

## Performance Expectations

With Think AI's O(1) architecture:
- Health check: < 1ms
- Simple queries: < 5ms
- Complex queries: < 10ms
- Concurrent handling: 1000+ req/s

Network latency will add to these times based on your connection to the cloud server.

## Security Best Practices

1. Always use SSH tunnels for production testing
2. Don't expose port 8080 publicly without authentication
3. Use strong SSH keys instead of passwords
4. Monitor access logs on cloud server
5. Rotate any API keys or tokens regularly

Need help? Check server logs:
```bash
ssh user@cloud-server "tail -f ~/think_ai/server.log"
```