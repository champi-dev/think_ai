# Think AI Railway Deployment Checklist

## Pre-deployment Verification

- [ ] You are in the Think AI directory with Rust code
- [ ] `ls Cargo.toml` shows the file exists  
- [ ] `ls package.json` shows "No such file"
- [ ] `cat THIS_IS_RUST_THINK_AI.txt` shows the marker file

## Files to Commit

```bash
git add Dockerfile
git add railway.json
git add .dockerignore
git add THIS_IS_RUST_THINK_AI.txt
git add fullstack_3d.html
git add knowledge/*.json
git add think-ai-cli/src/bin/full-server.rs  # Updated PORT handling
git commit -m "Fix Railway deployment - Rust server with PORT env"
git push
```

## Railway Configuration

1. **In Railway Dashboard**:
   - Project Settings > General
   - Verify "Source" shows your Rust Think AI repo
   - Should show branch: main (or your branch)

2. **Environment Variables**:
   - Railway auto-sets PORT
   - Add: `RUST_LOG=info` (optional)

3. **Build Settings**:
   - Builder: Dockerfile (should auto-detect)
   - Start Command: (leave empty, Dockerfile handles it)

## Build Verification

Watch the Railway build logs. You should see:

✅ **CORRECT BUILD**:
```
#1 [internal] load build definition from Dockerfile
#4 [builder 1/5] FROM docker.io/library/rust:1.80-slim
#5 [builder 2/5] RUN apt-get update && apt-get install -y --no-install-recommends pkg-config libssl-dev
#7 [builder 4/5] COPY . .
#8 [builder 5/5] RUN cargo build --release --bins
```

❌ **WRONG BUILD** (Next.js):
```
Installing dependencies...
npm install
Creating an optimized production build...
```

## Post-deployment Tests

```bash
# Set your Railway URL
RAILWAY_URL="https://think-ai-api-production.up.railway.app"

# 1. Health check
curl $RAILWAY_URL/health
# Expected: OK

# 2. Stats API
curl $RAILWAY_URL/api/stats | jq
# Expected: JSON with status, domains, etc.

# 3. Chat API
curl -X POST $RAILWAY_URL/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello"}' | jq
# Expected: JSON response

# 4. No Next.js files
curl $RAILWAY_URL/_next/static/
# Expected: 404

# 5. Webapp loads
curl $RAILWAY_URL/ | grep -q "Think AI"
# Expected: Success
```

## Troubleshooting

### Still seeing Next.js errors?

1. **Wrong repository**:
   - Railway is deploying a different repo
   - Disconnect and reconnect the correct repo

2. **Wrong branch**:
   - Check if main branch has Next.js code
   - Switch to correct branch with Rust code

3. **Cached build**:
   - Add dummy env var to force rebuild
   - Or use Railway CLI: `railway up --no-cache`

4. **Check deployment source**:
   ```bash
   # In your local Think AI directory
   git remote -v
   # Should show your Think AI repo, not a Next.js project
   ```

### Build fails?

Check build logs for:
- Missing Rust dependencies
- Cargo.toml issues
- Docker build errors

### Runs but 404 on all routes?

- Check if fullstack_3d.html is included in Docker image
- Verify PORT env var is being used
- Check server logs in Railway