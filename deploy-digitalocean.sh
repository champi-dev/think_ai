#!/bin/bash

# Digital Ocean GPU Deployment Script

echo "🌊 Digital Ocean GPU Deployment Setup"
echo "===================================="
echo ""

# 1. Create Dockerfile for DO
cat > Dockerfile.digitalocean << 'EOF'
FROM nvidia/cuda:12.2.0-base-ubuntu22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama with GPU support
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy pre-built app
COPY target/release/full-working-o1 /app/full-working-o1
COPY minimal_3d.html /app/minimal_3d.html
COPY static /app/static

# Startup script
RUN echo '#!/bin/bash' > /app/start.sh && \
    echo '# Start Ollama with GPU' >> /app/start.sh && \
    echo 'CUDA_VISIBLE_DEVICES=0 ollama serve &' >> /app/start.sh && \
    echo 'sleep 10' >> /app/start.sh && \
    echo '# Pull model (will use GPU)' >> /app/start.sh && \
    echo 'ollama pull qwen2.5:1.5b' >> /app/start.sh && \
    echo '# Start app' >> /app/start.sh && \
    echo 'cd /app && ./full-working-o1' >> /app/start.sh && \
    chmod +x /app/start.sh

WORKDIR /app
EXPOSE 8080
CMD ["/app/start.sh"]
EOF

echo "✅ Dockerfile.digitalocean created"
echo ""

# 2. Create deployment instructions
cat > DEPLOY-DIGITALOCEAN.md << 'EOF'
# Digital Ocean GPU Deployment Guide

## 1. Create GPU Droplet

1. Go to Digital Ocean Console
2. Create Droplet → GPU Droplets
3. Choose:
   - **GPU Type**: H100 (best) or A100 (good) or V100 (budget)
   - **OS**: Ubuntu 22.04
   - **Size**: Based on your budget ($90-$500/month)
   - **Region**: Closest to your users

## 2. Setup Droplet

SSH into your droplet:
```bash
ssh root@your-droplet-ip
```

Install Docker with GPU support:
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker

# Verify GPU
nvidia-smi
docker run --rm --gpus all nvidia/cuda:12.2.0-base-ubuntu22.04 nvidia-smi
```

## 3. Deploy Think AI

Clone and build:
```bash
# Clone repo
git clone https://github.com/champi-dev/think_ai.git
cd think_ai

# Build Docker image
docker build -f Dockerfile.digitalocean -t think-ai-gpu .

# Run with GPU
docker run -d \
  --name think-ai \
  --gpus all \
  -p 80:8080 \
  --restart unless-stopped \
  think-ai-gpu
```

## 4. Setup Domain (Optional)

1. Point your domain to droplet IP
2. Install Nginx:
```bash
sudo apt install nginx certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

## 5. Monitor

Check GPU usage:
```bash
nvidia-smi
docker logs think-ai
```

Test:
```bash
curl http://your-droplet-ip/health
curl -X POST http://your-droplet-ip/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "hello"}'
```

## Performance

With GPU, expect:
- Qwen 1.5B responses in <1 second
- Can handle multiple concurrent requests
- Much lower latency than CPU
EOF

echo "✅ DEPLOY-DIGITALOCEAN.md created"
echo ""

# 3. Create docker-compose for easier deployment
cat > docker-compose.digitalocean.yml << 'EOF'
version: '3.8'

services:
  think-ai:
    build:
      context: .
      dockerfile: Dockerfile.digitalocean
    ports:
      - "80:8080"
    restart: unless-stopped
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    environment:
      - CUDA_VISIBLE_DEVICES=0
      - OLLAMA_HOST=0.0.0.0:11434
    volumes:
      - ollama-models:/root/.ollama
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  ollama-models:
EOF

echo "✅ docker-compose.digitalocean.yml created"
echo ""
echo "📋 Next Steps:"
echo "1. Create a GPU Droplet on Digital Ocean"
echo "2. Follow instructions in DEPLOY-DIGITALOCEAN.md"
echo "3. Enjoy fast Qwen responses with GPU acceleration!"
echo ""
echo "💡 Tip: Start with the cheapest GPU option to test"
echo "   You can always upgrade later!"