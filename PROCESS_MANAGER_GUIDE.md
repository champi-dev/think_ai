# Process Manager Documentation

## Overview

The Think AI system uses a Python-based process manager to orchestrate multiple services through a single port, making it ideal for deployment on platforms like Railway that require single-port exposure.

## Architecture

```
                    External Traffic (Railway PORT)
                              ↓
                    ┌─────────────────────┐
                    │   Process Manager   │
                    │  (Python HTTP Proxy)│
                    └─────────┬───────────┘
                              │
                ┌─────────────┴─────────────┐
                ↓                           ↓
        ┌───────────────┐           ┌───────────────┐
        │   API Server  │           │   Web App     │
        │  (Port 8080)  │           │  (Port 3000)  │
        └───────────────┘           └───────────────┘
```

## Files

### process_manager.py

The main orchestrator that:
- Starts and monitors both API and webapp services
- Implements a reverse proxy to route requests
- Handles health checks and service restarts
- Logs all service output for debugging

**Key Features:**
- Routes `/api/*` and `/health` to API server (port 8080)
- Routes all other requests to webapp (port 3000)
- Graceful shutdown handling
- Automatic service restart on failure

### start_full_system.py

Alternative startup script that:
- Provides similar functionality to process_manager.py
- Supports both local and Railway environments
- Can be used for development and testing

## Usage

### Local Development

```bash
# Using process manager
python process_manager.py

# Using full system starter
python start_full_system.py

# Services will be available at:
# - Main entry: http://localhost:8080 (or PORT env var)
# - API direct: http://localhost:8080/api/*
# - Web direct: http://localhost:3000
```

### Railway Deployment

The system automatically detects Railway environment and configures accordingly:

```bash
# Railway will run (from railway.json):
python process_manager.py

# Environment variables set by Railway:
# - PORT: Main port assigned by Railway
# - RAILWAY_ENVIRONMENT: Deployment environment
```

### Docker Deployment

```bash
# Build image
docker build -t think-ai:latest .

# Run container
docker run -p 8080:8080 think-ai:latest
```

## Routing Rules

| Path Pattern | Target Service | Port |
|--------------|----------------|------|
| `/api/*`     | API Server     | 8080 |
| `/health`    | API Server     | 8080 |
| `/ws`        | API Server     | 8080 |
| `/*`         | Web App        | 3000 |

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Main port for process manager | 8080 |
| `API_PORT` | Internal API server port | 8080 |
| `WEBAPP_PORT` | Internal webapp port | 3000 |
| `PYTHONUNBUFFERED` | Enable real-time logging | 1 |
| `NODE_ENV` | Node environment | production |

## Health Monitoring

The process manager monitors both services:
- Checks if processes are still running every 5 seconds
- Automatically exits if any service dies
- Logs all output from both services

Health check endpoint: `http://localhost:PORT/health`

## Logging

All service logs are prefixed with the service name:
- `[API]` - API server logs
- `[API-err]` - API server errors
- `[Webapp]` - Web application logs
- `[Webapp-err]` - Web application errors

## Troubleshooting

### Service Won't Start
1. Check if ports 8080 and 3000 are available
2. Ensure all dependencies are installed
3. Check logs for specific error messages

### Routing Issues
1. Verify the path patterns in your requests
2. Check process manager logs for proxy errors
3. Ensure both backend services are running

### Railway Deployment Issues
1. Ensure `railway.json` is properly configured
2. Check Railway logs for build/runtime errors
3. Verify environment variables are set correctly

## Best Practices

1. **Always use relative URLs in production webapp**
   - Use `/api/v1` instead of `http://localhost:8080/api/v1`
   
2. **Monitor service health**
   - Regularly check `/health` endpoint
   - Set up alerts for service failures

3. **Graceful shutdown**
   - Use SIGTERM for clean shutdown
   - Process manager handles cleanup automatically

4. **Resource management**
   - Monitor memory usage of both services
   - Scale horizontally on Railway if needed

## Integration with Think AI

The process manager integrates seamlessly with:
- **API Server**: Started with `start_with_patch.py` to handle transformers compatibility
- **Web App**: Production Next.js build with optimized performance
- **Docker**: Multi-service container with minimal overhead
- **Railway**: Single-port deployment with automatic routing

## Security Considerations

- Internal services (8080, 3000) are not exposed externally
- All traffic flows through the process manager proxy
- Headers are sanitized during proxying
- Connection pooling prevents resource exhaustion