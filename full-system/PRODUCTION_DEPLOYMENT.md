# ThinkAI Production Deployment Guide

## 🚀 Quick Deploy

1. **Build the production binary:**
   ```bash
   cargo build --release --bin think-ai-full-production
   ```

2. **Set environment variables:**
   ```bash
   export DEEPGRAM_API_KEY="e31341c95ee93fd2c8fced1bf37636f042fe038b"
   export ELEVENLABS_API_KEY="sk_aa595f99bc5842b5df837d4c47fe3a18ce00b9a39a0f2877"
   export AUDIO_CACHE_DIR="./audio_cache"
   export PORT="7777"
   ```

3. **Run the server:**
   ```bash
   ./target/release/think-ai-full-production
   ```

## 📋 Complete Deployment Checklist

### Prerequisites
- [ ] Rust installed (1.70+)
- [ ] SQLite installed (for persistent memory)
- [ ] 2GB+ RAM available
- [ ] Port 7777 (or custom PORT) available

### Environment Variables
```bash
# Required for audio services
DEEPGRAM_API_KEY=e31341c95ee93fd2c8fced1bf37636f042fe038b
ELEVENLABS_API_KEY=sk_aa595f99bc5842b5df837d4c47fe3a18ce00b9a39a0f2877

# Optional
AUDIO_CACHE_DIR=./audio_cache  # Audio cache directory
PORT=7777                       # Server port
RUST_LOG=info                   # Logging level

# WhatsApp (optional)
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
NOTIFICATION_PHONE=whatsapp:+1234567890
```

### Production Setup

1. **Create systemd service** (Linux):
   ```bash
   sudo nano /etc/systemd/system/thinkai.service
   ```

   ```ini
   [Unit]
   Description=ThinkAI Production Server
   After=network.target

   [Service]
   Type=simple
   User=thinkai
   WorkingDirectory=/opt/thinkai
   Environment="DEEPGRAM_API_KEY=e31341c95ee93fd2c8fced1bf37636f042fe038b"
   Environment="ELEVENLABS_API_KEY=sk_aa595f99bc5842b5df837d4c47fe3a18ce00b9a39a0f2877"
   Environment="AUDIO_CACHE_DIR=/opt/thinkai/audio_cache"
   Environment="PORT=7777"
   Environment="RUST_LOG=info"
   ExecStart=/opt/thinkai/think-ai-full-production
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

2. **Enable and start service:**
   ```bash
   sudo systemctl enable thinkai
   sudo systemctl start thinkai
   sudo systemctl status thinkai
   ```

3. **Setup Nginx reverse proxy:**
   ```nginx
   server {
       listen 443 ssl http2;
       server_name thinkai.lat;

       ssl_certificate /etc/letsencrypt/live/thinkai.lat/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/thinkai.lat/privkey.pem;

       location / {
           proxy_pass http://localhost:7777;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }

       # WebSocket support for future features
       location /ws {
           proxy_pass http://localhost:7777;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
       }
   }

   server {
       listen 80;
       server_name thinkai.lat;
       return 301 https://$server_name$request_uri;
   }
   ```

## 🔧 What's Fixed in Production Build

1. **Metrics Collection**: 
   - ✅ MetricsLayer middleware properly integrated
   - ✅ Request counting and endpoint statistics
   - ✅ Memory leak prevention (endpoint stats limited to 100)

2. **Audio Services**:
   - ✅ API keys properly configured
   - ✅ Error handling for missing keys
   - ✅ Metrics tracking for transcriptions/syntheses

3. **WhatsApp Integration**:
   - ✅ Webhook handlers connected
   - ✅ Message counting metrics

4. **Dashboard**:
   - ✅ Available at `/stats`
   - ✅ Real-time metrics display
   - ✅ Memory usage monitoring

## 📊 Monitoring

1. **Health Check**: `curl https://thinkai.lat/health`
2. **Metrics API**: `curl https://thinkai.lat/api/metrics`
3. **Dashboard**: https://thinkai.lat/stats

## 🚨 Troubleshooting

### Audio Service Errors (500)
- Check API keys are set correctly
- Verify audio cache directory exists and is writable
- Check Deepgram/ElevenLabs API quotas

### Metrics Not Recording
- Ensure you're using `think-ai-full-production` binary
- Check logs for middleware initialization
- Verify MetricsLayer is in the router chain

### Memory Issues
- Monitor `/api/metrics` for memory growth
- Check endpoint_stats size (should stay ≤100)
- Review request_metrics buffer (limited to 1000)

## 🔐 Security Notes

1. **API Keys**: Store in environment variables, never commit
2. **Database**: `think_ai_sessions.db` contains conversation history
3. **Audio Cache**: May contain sensitive audio/text, secure directory
4. **Metrics**: No PII in metrics, safe to expose dashboard

## 📈 Performance Tuning

1. **CPU**: Uses efficient /proc monitoring (Linux)
2. **Memory**: Buffers limited to prevent leaks
3. **Audio**: Caching reduces API calls
4. **Database**: SQLite with prepared statements

## 🔄 Updating Production

1. Pull latest code
2. Build new binary: `cargo build --release --bin think-ai-full-production`
3. Stop service: `sudo systemctl stop thinkai`
4. Replace binary: `sudo cp target/release/think-ai-full-production /opt/thinkai/`
5. Start service: `sudo systemctl start thinkai`
6. Verify: Check health endpoint and metrics

## 📱 Mobile & Safari Support

The production build includes fixes for:
- Audio playback in Safari
- Instagram WebView compatibility
- PWA install prompts
- Mobile scrollbar hiding

These are implemented in the static files served from `/full-system/static/`.