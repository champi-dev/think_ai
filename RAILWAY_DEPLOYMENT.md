# 🚀 Railway Deployment Guide for Think AI

## Quick Deploy

1. **Install Railway CLI:**
```bash
curl -fsSL https://railway.app/install.sh | sh
```

2. **Login to Railway:**
```bash
railway login
```

3. **Deploy:**
```bash
railway up
```

Or use the deployment script:
```bash
./deploy_to_railway.sh
```

## Project Structure

```
think-ai/
├── Dockerfile              # Multi-stage build for production
├── railway.toml            # Railway configuration
├── minimal_3d.html         # Clean UI with quantum animation
├── think-ai-knowledge/data/ # Knowledge base files
└── think-ai-*/             # Rust crates
```

## Environment Variables

Railway will automatically set:
- `PORT` - The port your app should listen on
- `RAILWAY_ENVIRONMENT` - The environment (production/staging)

## Health Check

The app includes a health check endpoint at `/health` that Railway uses to monitor deployment status.

## Deployment Features

✅ **Multi-stage Docker build** for optimized image size
✅ **Dependency caching** for faster builds  
✅ **Clean UI** with 3D quantum animation
✅ **O(1) performance** optimizations
✅ **Health monitoring** with automatic restarts
✅ **Hierarchical knowledge** system

## URLs

After deployment, your app will be available at:
- Main app: `https://your-app-name.railway.app`
- Health check: `https://your-app-name.railway.app/health`

## Monitoring

```bash
# Check deployment status
railway status

# View logs
railway logs

# Get app URL
railway domain
```

## Troubleshooting

If build fails:
1. Check that all Cargo.toml files exist
2. Verify minimal_3d.html is present
3. Ensure knowledge data directory exists
4. Test local build: `cargo build --release --bin full-server`