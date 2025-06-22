# Think AI v3.1.0 Docker Images

## Available Dockerfiles

1. **Dockerfile.railway** - Optimized for Railway deployment
   - Minimal size
   - Fast build times
   - Production ready

2. **Dockerfile.v3** - Full featured image
   - All ML libraries included
   - Development tools
   - Larger size

## Build Commands

```bash
# Railway optimized
docker build -f Dockerfile.railway -t think-ai:railway .

# Full featured
docker build -f Dockerfile.v3 -t think-ai:full .

# Minimal
docker build -f Dockerfile.minimal -t think-ai:minimal .
```

## Push to Registry

```bash
# Tag for Docker Hub
docker tag think-ai:railway YOUR_USERNAME/think-ai:v3.1.0

# Push
docker push YOUR_USERNAME/think-ai:v3.1.0
```
