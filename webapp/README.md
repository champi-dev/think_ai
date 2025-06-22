# Think AI Web Application

Award-winning web interface with stunning Three.js animations and real-time consciousness visualization.

## Features

- 🎨 **3D Consciousness Visualization**: Real-time neural network activity with Three.js
- 🚀 **Progressive Web App**: Install on any device with offline support
- ⚡ **O(1) Performance**: Optimized Go API server with intelligent caching
- 🔄 **Real-time Updates**: WebSocket streaming of consciousness states
- 📱 **Responsive Design**: Beautiful on all devices with "wow effect" animations

## Quick Start

### Option 1: Full System (Recommended)

```bash
# Start both API and webapp with process manager
python process_manager.py

# Or use the full system starter
python start_full_system.py
```

### Option 2: Individual Services

```bash
# Start API server
python start_with_patch.py

# In another terminal, start webapp
cd webapp
npm run dev  # Development
npm start    # Production
```

### 3. Access the Application

Open http://localhost:3000 in your browser.

## Production Deployment

### Railway Deployment (Recommended)

```bash
# Deploy full system to Railway
railway login
railway link
railway up

# The deployment includes:
# - API server on internal port 8080
# - Webapp on internal port 3000
# - Process manager routing on Railway's PORT
```

### Docker Deployment

```bash
# Build and run with Docker
docker build -t think-ai:latest .
docker run -p 8080:8080 think-ai:latest
```

### Manual Deployment

```bash
# Build webapp for production
cd webapp
npm run build

# Start production servers
cd ..
python process_manager.py
```

## Architecture

### Frontend Stack
- **Next.js 14**: React framework with App Router
- **Three.js**: 3D graphics via @react-three/fiber
- **Tailwind CSS**: Utility-first styling
- **Framer Motion**: Smooth animations
- **Zustand**: State management
- **Socket.io**: Real-time communication

### Backend Stack
- **Go**: High-performance API server
- **Python Bridge**: Communication with Think AI core
- **WebSocket**: Real-time consciousness streaming
- **Caching**: O(1) response times with go-cache

## Development

### API Endpoints

- `POST /api/v1/think` - Submit queries
- `POST /api/v1/generate-code` - Generate code
- `GET /api/v1/intelligence` - Get intelligence metrics
- `POST /api/v1/training/start` - Start self-training
- `POST /api/v1/training/stop` - Stop training
- `GET /api/v1/consciousness/state` - Get consciousness state
- `GET /api/v1/ws` - WebSocket connection

### Environment Variables

#### Development
Create `.env.local` in webapp directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8080
NEXT_PUBLIC_WS_URL=ws://localhost:8080
```

#### Production (Railway/Docker)
Create `.env.production` in webapp directory:

```env
# Production environment variables for Railway deployment
NEXT_PUBLIC_API_URL=/api/v1
NEXT_PUBLIC_WS_URL=/api/v1/ws
NODE_ENV=production
```

Note: In production, the webapp uses relative URLs to communicate with the API through the process manager's reverse proxy.

## Performance Optimizations

- **Service Worker**: Caches assets for offline use
- **Image Optimization**: Next.js automatic optimization
- **Code Splitting**: Automatic route-based splitting
- **Edge Caching**: Vercel Edge Network integration
- **WebGL Optimization**: Three.js performance tuning

## PWA Features

- Install prompt on compatible devices
- Offline functionality with service worker
- App shortcuts for quick actions
- Native-like experience
- Push notifications (coming soon)

## Monitoring

- Health check: http://localhost:8888/health
- API health: http://localhost:8080/api/v1/health
- Logs: `sudo journalctl -u think-ai-core -f`