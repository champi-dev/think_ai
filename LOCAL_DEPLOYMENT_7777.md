# Think AI - Local Deployment on Port 7777

## Quick Start

Run the full Think AI system locally on port 7777:

```bash
./run-full-system-7777.sh
```

## Testing

Test the deployment:

```bash
./test-full-system-7777.sh
```

## Architecture

The local deployment includes:

1. **Backend Server** (Port 7778)
   - Stable server with O(1) performance
   - Qwen AI integration
   - Knowledge engine with 300+ legal sources
   - Vector search with LSH

2. **Webapp Server** (Port 7779) - Optional
   - 3D consciousness visualization
   - Real-time interactions

3. **Main Proxy** (Port 7777)
   - Serves static content
   - Proxies API requests to backend
   - Handles CORS and routing

## Available Endpoints

- `GET http://0.0.0.0:7777/` - Main web interface
- `GET http://0.0.0.0:7777/health` - Health check
- `GET http://0.0.0.0:7777/stats` - System statistics
- `POST http://0.0.0.0:7777/chat` - Chat API
- `POST http://0.0.0.0:7777/api/chat` - Alternative chat endpoint

## Manual Testing

```bash
# Health check
curl http://localhost:7777/health

# Chat request
curl -X POST http://localhost:7777/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is O(1) performance?"}'

# System stats
curl http://localhost:7777/stats | jq
```

## Logs

- Backend: `./backend_7778.log`
- Webapp: `./webapp_7779.log`
- Access from browser: http://localhost:7777

## Stopping the System

Press `Ctrl+C` in the terminal running the deployment script. The cleanup will automatically stop all services.