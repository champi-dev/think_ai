# Deploying Think AI to Railway

## Quick Deploy

1. Push your changes to GitHub:
```bash
git add .
git commit -m "Fix webapp deployment"
git push
```

2. In Railway:
   - Connect your GitHub repo
   - Railway will auto-detect the Dockerfile
   - Deploy will start automatically

## Manual Deploy

If you need to deploy manually:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link project
railway link

# Deploy
railway up
```

## Environment Variables

Set these in Railway dashboard if needed:
- `PORT` - Railway sets this automatically
- `RUST_LOG=info` - For logging
- `KNOWLEDGE_DIR=/app/knowledge` - Knowledge directory path

## Verify Deployment

After deployment:
1. Visit your Railway URL
2. You should see the 3D quantum visualization
3. Test the chat interface
4. Check `/api/stats` endpoint

## Troubleshooting

If you see 404 errors for JS files:
- This is expected - Think AI uses a single HTML file
- The webapp is self-contained in `fullstack_3d.html`
- Not a Next.js/React app

If webapp doesn't load:
- Check Railway logs: `railway logs`
- Ensure `fullstack_3d.html` exists in repo
- Verify Dockerfile copies the HTML file