# Docker Hub Setup for O(1) Railway Deployments

This guide will help you set up Docker Hub integration for true 10-second Railway deployments.

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

## Step 4: Build and Push Base Image

```bash
# Set your Docker Hub username
export DOCKER_HUB_USERNAME="yourusername"

# Run the build script
./build_and_push_base.sh
```

This will:
- Build the base image with all dependencies (~2-3 GB)
- Tag it with both a timestamp and 'latest'
- Push to Docker Hub
- This process takes 10-20 minutes but only needs to be done once

## Step 5: Update Dockerfiles

Replace `yourusername` in these files with your actual Docker Hub username:

1. `Dockerfile.api`
2. `Dockerfile.worker`
3. `railway.json`
4. `railway.api.json`
5. `railway.worker.json`

Example:
```dockerfile
ARG BASE_IMAGE=johndoe/think-ai-base:latest
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
1. Railway pulls base image: 2-3 seconds
2. Copy application code: 1-2 seconds
3. Start container: 3-5 seconds
4. **Total: <10 seconds!**

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