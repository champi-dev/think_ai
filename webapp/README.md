# Think AI Web Application

Award-winning web interface with stunning Three.js animations and real-time consciousness visualization.

## Features

- 🎨 **3D Consciousness Visualization**: Real-time neural network activity with Three.js
- 🚀 **Progressive Web App**: Install on any device with offline support
- ⚡ **O(1) Performance**: Optimized Go API server with intelligent caching
- 🔄 **Real-time Updates**: WebSocket streaming of consciousness states
- 📱 **Responsive Design**: Beautiful on all devices with "wow effect" animations

## Quick Start

### 1. Install Dependencies

```bash
# Go server dependencies
cd server
go mod download

# Webapp dependencies
cd ../webapp
npm install
```

### 2. Start Services

```bash
# Start Think AI core services
docker-compose up -d

# Start Think AI background service
python -m think_ai.core.background_service

# Start Go API server
cd server
go run cmd/api/main.go

# Start webapp development server
cd webapp
npm run dev
```

### 3. Access the Application

Open http://localhost:3000 in your browser.

## Production Deployment

### System Services

```bash
# Install and enable services
sudo ./scripts/install_webapp_services.sh

# Services will auto-start on boot
sudo systemctl status think-ai-core
sudo systemctl status think-ai-api
```

### Vercel Deployment

```bash
cd webapp
npm run build
vercel deploy --prod
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

Create `.env.local` in webapp directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8080
NEXT_PUBLIC_WS_URL=ws://localhost:8080
```

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