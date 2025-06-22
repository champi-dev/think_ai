#!/bin/bash
# Manual Docker build commands for Think AI

# 1. First, login to Docker Hub
echo "🔐 Step 1: Login to Docker Hub"
echo "Run: docker login"
echo "Enter your Docker Hub username and password/token"
echo ""

# 2. Build the image locally
echo "🏗️  Step 2: Build the image"
echo "Run these commands:"
echo ""
echo "# Enable BuildKit for better caching"
echo "export DOCKER_BUILDKIT=1"
echo ""
echo "# Build the hypercache image"
echo "docker build -f Dockerfile.railway-hypercache -t think-ai:hypercache ."
echo ""

# 3. Tag the image with your Docker Hub username
echo "🏷️  Step 3: Tag the image with your Docker Hub username"
echo "Replace YOUR_DOCKERHUB_USERNAME with your actual username:"
echo ""
echo "docker tag think-ai:hypercache YOUR_DOCKERHUB_USERNAME/think-ai:hypercache"
echo "docker tag think-ai:hypercache YOUR_DOCKERHUB_USERNAME/think-ai:latest"
echo ""

# 4. Push to Docker Hub
echo "📤 Step 4: Push to Docker Hub"
echo "Replace YOUR_DOCKERHUB_USERNAME with your actual username:"
echo ""
echo "docker push YOUR_DOCKERHUB_USERNAME/think-ai:hypercache"
echo "docker push YOUR_DOCKERHUB_USERNAME/think-ai:latest"
echo ""

# 5. Update Railway to use your image
echo "🚂 Step 5: Update Railway configuration"
echo "Option A: Use pre-built image from Docker Hub"
echo "Create/update railway.json:"
echo '
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKER",
    "image": "YOUR_DOCKERHUB_USERNAME/think-ai:hypercache"
  },
  "deploy": {
    "numReplicas": 1,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 3,
    "startCommand": "python railway_fast_start.py",
    "environmentVariables": {
      "PYTHONUNBUFFERED": "1",
      "THINK_AI_COLOMBIAN": "true",
      "THINK_AI_LIGHTWEIGHT": "true",
      "THINK_AI_MINIMAL_INIT": "true",
      "THINK_AI_MODEL": "lightweight",
      "PORT": "${{PORT}}"
    }
  }
}
'
echo ""
echo "Option B: Let Railway build from Dockerfile"
echo "Keep current railway.json as is"
echo ""

# Alternative: Build without BuildKit if needed
echo "📝 Alternative: If BuildKit doesn't work, use regular build:"
echo "docker build --no-cache -f Dockerfile.railway-hypercache -t YOUR_DOCKERHUB_USERNAME/think-ai:hypercache ."
echo ""

# Check image size
echo "📏 To check image size after building:"
echo "docker images | grep think-ai"
echo ""

# Test locally
echo "🧪 To test locally before pushing:"
echo "docker run -p 8080:8080 -e PORT=8080 YOUR_DOCKERHUB_USERNAME/think-ai:hypercache"
echo ""

# Troubleshooting
echo "🔧 Troubleshooting:"
echo "- If 'requested access denied': Make sure you're logged in with 'docker login'"
echo "- If push fails: Check you're using YOUR username, not 'champidev'"
echo "- If build fails: Try without --squash flag (requires experimental features)"
echo "- For private repos: docker login with personal access token instead of password"