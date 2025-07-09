# Think AI Deployment Guide

## Railway Deployment

### Prerequisites
- Railway account (https://railway.app)
- Railway CLI installed (`npm install -g @railway/cli`)
- Git repository connected to Railway

### Quick Deploy

1. **Login to Railway:**
   ```bash
   railway login
   ```

2. **Create new project:**
   ```bash
   railway init
   ```

3. **Deploy:**
   ```bash
   railway up
   ```

### Manual Deploy via GitHub

1. Connect your GitHub repository to Railway
2. Railway will automatically deploy on push to main branch
3. Monitor builds at: https://railway.app/dashboard

### Configuration

The project is configured with:
- `railway.toml` - Build and deployment settings
- `Dockerfile` - Container configuration
- `start-server.sh` - Server startup script

### Environment Variables

Railway automatically sets:
- `PORT` - The port your server should listen on
- `RAILWAY_ENVIRONMENT` - Deployment environment

Optional variables you can set:
- `RUST_LOG` - Logging level (default: info)

### Troubleshooting

**Build fails:**
- Check Rust version compatibility (1.82)
- Ensure all dependencies compile
- View build logs in Railway dashboard

**Server doesn't start:**
- Verify the binary exists: `think-ai`
- Check that PORT env var is used
- Review runtime logs: `railway logs`

**Connection issues:**
- Railway provides automatic HTTPS
- No need to configure SSL certificates
- Your app will be available at: `https://your-app.up.railway.app`

## Local Development

### Running locally:
```bash
# Build
cargo build --release

# Run server
PORT=8080 ./target/release/think-ai server

# Or use the start script
./start-server.sh
```

### Testing the deployment:
```bash
# Health check
curl http://localhost:8080/api/health

# API test
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello"}'
```

## Working Binaries

The following binaries are built and deployable:
- `think-ai` - Main CLI with server command
- `think-ai-coding` - Code generation tool
- `think-ai-demos` - Demo applications
- `think-ai-llm` - LLM interface

## Architecture

```
Railway -> Dockerfile -> Rust Build -> Binary -> Server
                |
                v
          start-server.sh
                |
                v
         think-ai server
                |
                v
          Port $PORT (0.0.0.0)
```

## Author

- **champi-dev** - [danielsarcor@gmail.com](mailto:danielsarcor@gmail.com)
- GitHub: [https://github.com/champi-dev/think_ai](https://github.com/champi-dev/think_ai)