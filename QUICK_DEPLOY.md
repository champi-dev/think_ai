# Think AI Quantum Generation - Quick Deployment Guide

## Backend (GPU Server)
1. Copy deployment: `scp -r deployment-quantum/ user@gpu-server:/path/to/`
2. SSH to server: `ssh user@gpu-server`
3. Start server: `cd deployment-quantum && ./start-quantum-server.sh`
4. Note the ngrok URL shown in output

## Frontend (Vercel)
1. Update ngrok URL in `vercel-deploy/config.js`
2. Deploy: `cd vercel-deploy && vercel --prod`
3. Visit your Vercel URL

## Features
✓ Qwen-only generation (no fallback)
✓ Isolated parallel threads
✓ Shared intelligence
✓ O(1) performance

## Testing
- Chat endpoint: `[ngrok-url]/api/chat`
- Quantum chat: `[ngrok-url]/api/quantum-chat`
- Parallel chat: `[ngrok-url]/api/parallel-chat`
