# Deployment

The Think AI system is designed to be deployed as a standalone service with a responsive React frontend and Rust backend. The system provides comprehensive deployment options for both development and production environments.

## Production Deployment

The production version of the Think AI system is deployed at [https://thinkai.lat](https://thinkai.lat). This deployment includes:

- **Backend**: `think-ai-full-fixed` binary running on port 8080
- **Frontend**: React application with Vite build system
- **Infrastructure**: DatabaseMart GPU server with high-performance computing capabilities
- **Features**: 
  - Responsive UI that works on desktop and mobile devices
  - Server-Side Events (SSE) for streaming responses
  - WebSocket support for real-time communication
  - PWA support with offline capabilities
  - Session persistence with SQLite database

### System Requirements

- Rust 1.70+ for backend compilation
- Node.js 18+ for frontend build
- SQLite for session storage
- 4GB+ RAM recommended
- GPU access (optional, for enhanced AI processing)

## Local Development

### Quick Start

1. **Clone and setup**:
```bash
git clone https://github.com/champi-dev/think_ai.git
cd think_ai
npm run install:all
```

2. **Run development servers**:
```bash
# Run both frontend and backend in parallel
npm run dev

# Or run separately:
# Backend
cd full-system && cargo run --bin think-ai-full-fixed

# Frontend
cd frontend && npm run dev
```

3. **Access the application**:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8080

### Build for Production

```bash
# Build everything
npm run build

# Or build separately:
# Backend
cd full-system && cargo build --release --bin think-ai-full-fixed

# Frontend  
cd frontend && npm run build
```

## Docker Deployment

```dockerfile
# Multi-stage build for optimal image size
FROM rust:1.70 as backend-builder
WORKDIR /app
COPY full-system ./full-system
COPY lib ./lib
WORKDIR /app/full-system
RUN cargo build --release --bin think-ai-full-fixed

FROM node:18 as frontend-builder
WORKDIR /app
COPY frontend ./frontend
WORKDIR /app/frontend
RUN npm ci && npm run build

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=backend-builder /app/full-system/target/release/think-ai-full-fixed /usr/local/bin/
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist
WORKDIR /app
ENV PORT=8080
EXPOSE 8080
CMD ["think-ai-full-fixed"]
```

## Systemd Service

For production deployments on Linux:

```ini
[Unit]
Description=Think AI Service
After=network.target

[Service]
Type=simple
User=think-ai
WorkingDirectory=/opt/think-ai
ExecStart=/opt/think-ai/full-system/target/release/think-ai-full-fixed
Restart=on-failure
RestartSec=10
Environment="RUST_LOG=info"
Environment="PORT=8080"
Environment="THINK_AI_DB_PATH=/var/lib/think-ai/sessions.db"

[Install]
WantedBy=multi-user.target
```

## Environment Variables

```bash
# Server Configuration
PORT=8080                                    # Server port
RUST_LOG=info,think_ai=debug                # Logging level

# Database
THINK_AI_DB_PATH=./think_ai_sessions.db     # Session database path

# AI Model Configuration  
QWEN_API_KEY=your_api_key                   # Qwen API key (if using cloud)
QWEN_MODEL_PATH=/path/to/model              # Local model path (if self-hosted)

# Optional Features
ENABLE_METRICS=true                         # Enable Prometheus metrics
METRICS_PORT=9090                           # Metrics endpoint port
ENABLE_TRACING=true                         # Enable OpenTelemetry tracing
```

## NGINX Configuration

For production deployments behind NGINX:

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name thinkai.lat;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name thinkai.lat;

    ssl_certificate /etc/letsencrypt/live/thinkai.lat/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/thinkai.lat/privkey.pem;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Proxy to backend
    location /api {
        proxy_pass http://localhost:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket support
    location /ws {
        proxy_pass http://localhost:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }

    # Serve frontend
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Monitoring and Health Checks

The system provides health check endpoints:

- `/health` - Basic health check (returns "OK")
- `/api/health` - Detailed health status with service info
- `/api/knowledge/stats` - System statistics and metrics

### Prometheus Metrics

When metrics are enabled, the following are exposed:

- Request latency histograms
- Active session counts
- Token usage metrics
- Error rates
- System resource usage

## Backup and Recovery

### Database Backup

```bash
# Backup sessions database
sqlite3 /var/lib/think-ai/sessions.db ".backup /backup/sessions-$(date +%Y%m%d).db"

# Restore from backup
sqlite3 /var/lib/think-ai/sessions.db ".restore /backup/sessions-20240716.db"
```

### Full System Backup

```bash
#!/bin/bash
BACKUP_DIR="/backup/think-ai-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Backup database
sqlite3 /var/lib/think-ai/sessions.db ".backup $BACKUP_DIR/sessions.db"

# Backup configuration
cp -r /opt/think-ai/config "$BACKUP_DIR/"

# Backup logs
cp -r /var/log/think-ai "$BACKUP_DIR/logs"

# Create archive
tar -czf "$BACKUP_DIR.tar.gz" "$BACKUP_DIR"
rm -rf "$BACKUP_DIR"
```

## Scaling Considerations

For high-traffic deployments:

1. **Horizontal Scaling**: Deploy multiple instances behind a load balancer
2. **Database Scaling**: Use PostgreSQL instead of SQLite for session storage
3. **Caching**: Implement Redis for session and response caching
4. **CDN**: Serve static assets through a CDN
5. **GPU Clustering**: Distribute AI workload across multiple GPUs

## Security Best Practices

1. Always use HTTPS in production
2. Implement rate limiting
3. Regular security updates
4. Monitor for suspicious activity
5. Use environment variables for sensitive configuration
6. Enable CORS only for trusted origins
7. Implement proper authentication for admin endpoints
