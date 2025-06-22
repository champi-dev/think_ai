# Think AI Deployment Documentation

## Overview

This document provides comprehensive deployment instructions for the Think AI system across various platforms and environments.

## Deployment Options

### 1. Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python start_full_system.py
```

### 2. Docker Deployment
```bash
# Build the Docker image
docker build -t think-ai:latest .

# Run the container
docker run -p 8000:8000 think-ai:latest
```

### 3. Railway Deployment
```bash
# Deploy to Railway
./deploy_railway.sh

# Or use the optimized deployment
./railway-deploy-optimized.sh
```

### 4. Kubernetes Deployment
```bash
# Apply Kubernetes manifests
kubectl apply -f kubernetes/

# Check deployment status
kubectl get pods -l app=think-ai
```

## Environment Variables

Required environment variables for deployment:

- `THINK_AI_PORT`: Port to run the application (default: 8000)
- `THINK_AI_ENV`: Environment (development/production)
- `REDIS_URL`: Redis connection URL (for caching)
- `DATABASE_URL`: Database connection string

## Pre-deployment Checklist

- [ ] Run all tests: `python run_all_tests.sh`
- [ ] Check linting: `python scripts/think_ai_linter.py`
- [ ] Build Docker images: `./build_optimized_base.sh`
- [ ] Verify environment variables
- [ ] Review security configurations

## Production Considerations

1. **Performance Optimization**
   - Enable Redis caching
   - Use optimized Docker images
   - Configure proper resource limits

2. **Security**
   - Use HTTPS in production
   - Set secure environment variables
   - Enable authentication

3. **Monitoring**
   - Set up logging aggregation
   - Configure health checks
   - Enable performance monitoring

## Deployment Scripts

- `deploy_railway.sh` - Deploy to Railway platform
- `build_optimized_base.sh` - Build optimized base image
- `scripts/deployment/deploy_full_system.sh` - Full system deployment
- `scripts/deploy-all-libs.sh` - Deploy all libraries to PyPI/npm

## Troubleshooting

### Common Issues

1. **Port conflicts**: Check if port 8000 is available
2. **Missing dependencies**: Run `pip install -r requirements.txt`
3. **Docker build failures**: Ensure Docker daemon is running
4. **Railway deployment issues**: Check Railway logs with `railway logs`

### Support

For deployment support, please refer to:
- Documentation: `/docs`
- Issues: GitHub Issues
- Community: Discord/Slack channels

## Version Information

Current version: v3.1.0
Last updated: 2025-06-22