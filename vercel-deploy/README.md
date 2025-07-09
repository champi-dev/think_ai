# Think AI Webapp - Vercel Deployment

This is the static frontend for Think AI, deployed on Vercel for global CDN distribution.

## Architecture
- **Frontend**: Static PWA on Vercel (this deployment)
- **Backend**: GPU server at http://69.197.178.37:8080 (handles all computation)

## Features
- O(1) performance algorithms
- PWA with offline support
- Real-time chat interface
- GPU-accelerated AI processing

## API Endpoints
All API calls are proxied to the GPU server:
- `/api/chat` → `http://69.197.178.37:8080/api/chat`
- `/api/process` → `http://69.197.178.37:8080/api/process`
- `/health` → `http://69.197.178.37:8080/health`
