# Docker Hub Setup for O(1) Railway Deployments

**Last Updated:** December 22, 2024

This guide explains how Think AI achieves ultra-fast deployments using pre-built Docker images. The current production setup uses `devsarmico/think-ai-base:optimized` for instant deployments.

## Prerequisites

1. Docker installed locally
2. Docker Hub account (free tier is sufficient)
3. Railway account

## Step 1: Create Docker Hub Account

1. Go to https://hub.docker.com/signup
2. Create a free account
3. Verify your email

## Step 2: Create Repository on Docker Hub

1. Log in to Docker Hub
2. Click "Create Repository"
3. Name it `think-ai-base`
4. Set visibility to "Public" (or Private if you have a paid account)
5. Click "Create"

## Step 3: Configure Local Docker

```bash
# Login to Docker Hub
docker login

# Enter your Docker Hub username and password when prompted
```

## Current Production Setup

Think AI currently uses the optimized base image:

```dockerfile
# In Dockerfile
FROM devsarmico/think-ai-base:optimized AS final
```

This image includes:
- All Python dependencies pre-installed
- Optimized for Railway deployment
- Multi-stage build for minimal size
- Support for both API and webapp services

## Step 4: Build and Push Base Image

### Using Existing Optimized Image (Recommended)

```bash
# Pull the optimized image
docker pull devsarmico/think-ai-base:optimized

# Use it in your Dockerfile
# FROM devsarmico/think-ai-base:optimized
```

### Building Your Own Base Image

```bash
# Create base image Dockerfile
cat > Dockerfile.base << 'EOF'
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements-fast.txt .
RUN pip install --no-cache-dir -r requirements-fast.txt

# Pre-download models (optional)
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
EOF

# Build and push
export DOCKER_HUB_USERNAME="yourusername"
docker build -f Dockerfile.base -t $DOCKER_HUB_USERNAME/think-ai-base:optimized .
docker push $DOCKER_HUB_USERNAME/think-ai-base:optimized
```

## Step 5: Update Dockerfile for Your Deployment

The current `Dockerfile` uses the multi-service architecture:

```dockerfile
# Multi-service Dockerfile for Railway deployment
FROM devsarmico/think-ai-base:optimized AS final

# Install Node.js for webapp
USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends nodejs npm && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Add Railway caching labels
LABEL railway.cache=true
LABEL railway.cache.key="think-ai-full-system-v1"

# Copy application code
WORKDIR /app
COPY . .

# Set up process manager
RUN chmod +x process_manager.py start_full_system.py

# Expose ports
EXPOSE 8080 3000

# Start with process manager
CMD ["python", "process_manager.py"]
```

## Step 6: Configure Railway

### Option A: Single Service Deployment

1. Push your code to GitHub
2. In Railway, create a new project from your GitHub repo
3. Railway will automatically use `railway.json`
4. Add environment variables if needed
5. Deploy!

### Option B: Multi-Service Deployment

1. Create a new Railway project
2. Add first service:
   - Name: `think-ai-api`
   - Set `RAILWAY_CONFIG_FILE=railway.api.json`
3. Add second service:
   - Name: `think-ai-worker`
   - Set `RAILWAY_CONFIG_FILE=railway.worker.json`

## Step 7: Environment Variables

Set these in Railway dashboard:

```bash
# Required
PORT=8080

# Optional
THINK_AI_MODE=production
LOG_LEVEL=info
MAX_WORKERS=4
```

## Deployment Timeline

### First Time Setup (One-time only)
1. Build base image: 10-20 minutes
2. Push to Docker Hub: 5-10 minutes
3. Total: ~30 minutes

### Subsequent Deployments (O(1))
1. Railway pulls base image: 2-3 seconds (cached after first pull)
2. Copy application code: 1-2 seconds
3. Install Node.js: 5-10 seconds (minimal Alpine packages)
4. Start services: 3-5 seconds
5. **Total: 10-20 seconds!**

### With Railway Caching Enabled
- Subsequent deployments with no dependency changes: **5-10 seconds**
- Full rebuilds only when base image changes

## Updating Dependencies

When you need to update dependencies:

1. Modify `requirements-full.txt`
2. Run `./build_and_push_base.sh`
3. Update the `BASE_IMAGE` in railway.json files if using version tags
4. Redeploy on Railway

## Optimization Tips

### 1. Use Specific Version Tags

Instead of `latest`, use version tags in production:
```json
"buildArgs": {
  "BASE_IMAGE": "yourusername/think-ai-base:20240620-143022"
}
```

### 2. Private Registry (Optional)

For private code, use Docker Hub's private repositories or GitHub Container Registry:
```bash
# For GitHub Container Registry
docker tag think-ai-base:latest ghcr.io/yourusername/think-ai-base:latest
docker push ghcr.io/yourusername/think-ai-base:latest
```

### 3. Multi-Architecture Builds

For better compatibility:
```bash
docker buildx build --platform linux/amd64,linux/arm64 -t yourusername/think-ai-base:latest --push .
```

### 4. Cache Warming

Pre-download models in the base image:
```dockerfile
RUN python -c "from transformers import AutoModel; AutoModel.from_pretrained('model-name')"
```

## Troubleshooting

### Issue: Railway can't pull image
- Ensure the Docker Hub repository is public
- Check the image name matches exactly
- Verify Railway has internet access

### Issue: Build still takes long time
- Check Railway logs to ensure it's using Dockerfile.api
- Verify base image is being pulled (not built)
- Ensure requirements aren't being reinstalled

### Issue: Application won't start
- Check that all required files are copied in Dockerfile.api
- Verify environment variables are set
- Check Railway logs for Python errors

## Monitoring Build Times

Railway shows build duration in the deployment logs. You should see:
- Image pull: 2-5 seconds
- Build: 3-5 seconds
- Total: <10 seconds

## Cost Optimization

This approach saves:
- **Build minutes**: ~10 minutes per deployment
- **Bandwidth**: Only code changes are transferred
- **Time**: Deploy fixes in seconds, not minutes

## Security Considerations

1. **Public Images**: Don't include secrets in base image
2. **Private Code**: Use private Docker Hub repos
3. **Environment Variables**: Use Railway's secret management
4. **Version Pinning**: Use specific versions in production

## Conclusion

With this setup, you achieve true O(1) deployments:
- Dependencies are pre-built and cached
- Only application code is copied
- Deployments complete in under 10 seconds
- Perfect for rapid iteration and hotfixes