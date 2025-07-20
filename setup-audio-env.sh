#!/bin/bash

# Audio Service Environment Setup
# This script sets up the required environment variables for the audio service

echo "🎵 Setting up Audio Service Environment..."

# Export the API keys
export DEEPGRAM_API_KEY="e31341c95ee93fd2c8fced1bf37636f042fe038b"
export ELEVENLABS_API_KEY="sk_aa595f99bc5842b5df837d4c47fe3a18ce00b9a39a0f2877"
export AUDIO_CACHE_DIR="./full-system/audio_cache"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    cp .env.example .env 2>/dev/null || touch .env
fi

# Update .env file with audio keys
grep -v "^DEEPGRAM_API_KEY=" .env > .env.tmp && mv .env.tmp .env
grep -v "^ELEVENLABS_API_KEY=" .env > .env.tmp && mv .env.tmp .env
grep -v "^AUDIO_CACHE_DIR=" .env > .env.tmp && mv .env.tmp .env

echo "DEEPGRAM_API_KEY=$DEEPGRAM_API_KEY" >> .env
echo "ELEVENLABS_API_KEY=$ELEVENLABS_API_KEY" >> .env
echo "AUDIO_CACHE_DIR=$AUDIO_CACHE_DIR" >> .env

echo "✅ Audio API keys configured"
echo "📂 Audio cache directory: $AUDIO_CACHE_DIR"

# Create systemd service override for audio environment
sudo mkdir -p /etc/systemd/system/think-ai.service.d/
cat << EOF | sudo tee /etc/systemd/system/think-ai.service.d/audio.conf > /dev/null
[Service]
Environment="DEEPGRAM_API_KEY=$DEEPGRAM_API_KEY"
Environment="ELEVENLABS_API_KEY=$ELEVENLABS_API_KEY"
Environment="AUDIO_CACHE_DIR=$AUDIO_CACHE_DIR"
EOF

echo "✅ Systemd service updated with audio configuration"

# Reload systemd and restart service
sudo systemctl daemon-reload
sudo systemctl restart think-ai

echo "🔄 Service restarted with audio support"
echo
echo "🎯 Audio service should now be active!"
echo "   - Transcription endpoint: POST /api/transcribe"
echo "   - Synthesis endpoint: POST /api/synthesize"