# Railway Deployment with Lightweight Docker Image

## Current Configuration

Railway is now configured to use the pre-built lightweight Docker image from Docker Hub.

### Configuration Files Updated:

1. **railway.json** - Uses Docker image instead of building
```json
{
  "build": {
    "builder": "DOCKER_IMAGE",
    "image": "champidev/think-ai:lightweight"
  }
}
```

2. **railway.toml** - Alternative config format
```toml
[build]
builder = "docker"
image = "champidev/think-ai:lightweight"
```

## Deployment Steps

### 1. Push Docker Image to Hub (One-time)
```bash
# Login to Docker Hub
docker login -u champidev

# Push the images
docker push champidev/think-ai:lightweight
docker push champidev/think-ai:latest
docker push champidev/think-ai:v2.0
```

### 2. Deploy to Railway
```bash
# Commit and push the configuration changes
git add railway.json railway.toml RAILWAY_DEPLOYMENT.md
git commit -m "Configure Railway to use lightweight Docker image from Hub"
git push origin main
```

### 3. Railway will automatically:
- Pull the image from Docker Hub (champidev/think-ai:lightweight)
- Skip the build process entirely
- Deploy using the lightweight image
- Start with `python railway_startup.py`

## Benefits

1. **Faster Deployments**: No build step, just pull and run
2. **Consistent**: Same image every time
3. **Small Size**: 173MB vs 2.5GB+
4. **No Dependencies**: All mocked with O(1) implementations
5. **Instant Startup**: < 1 second to be ready

## Environment Variables

Railway will set these automatically:
- `PYTHONUNBUFFERED=1`
- `THINK_AI_COLOMBIAN=true`
- `THINK_AI_LIGHTWEIGHT=true`
- `THINK_AI_MODEL=lightweight`
- `PORT=${{PORT}}` (Railway provides this)

## Health Check

- Endpoint: `/health`
- Expected: `200 OK`
- Response: `{"status": "healthy", "mode": "lightweight"}`

## Troubleshooting

If deployment fails:

1. **Check Docker Hub**: Ensure image is public
   ```bash
   docker pull champidev/think-ai:lightweight
   ```

2. **Check Logs**: Look for lightweight mode confirmation
   ```
   🚀 Lightweight mode installed - all dependencies replaced with O(1) implementations
   ```

3. **Verify Health**: 
   ```bash
   curl https://your-app.railway.app/health
   ```

## Rolling Back

To use local Dockerfile build instead:
```json
{
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile.lightweight-optimized"
  }
}
```

But the Docker Hub image is recommended for consistency and speed!