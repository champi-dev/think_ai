#!/bin/bash

echo "🎵 Checking Audio Service Configuration..."
echo

# Check for required API keys
if [ -z "$DEEPGRAM_API_KEY" ]; then
    echo "❌ DEEPGRAM_API_KEY is not set"
    echo "   Set it with: export DEEPGRAM_API_KEY='your_key_here'"
else
    echo "✅ DEEPGRAM_API_KEY is set (${#DEEPGRAM_API_KEY} chars)"
fi

if [ -z "$ELEVENLABS_API_KEY" ]; then
    echo "❌ ELEVENLABS_API_KEY is not set"
    echo "   Set it with: export ELEVENLABS_API_KEY='your_key_here'"
else
    echo "✅ ELEVENLABS_API_KEY is set (${#ELEVENLABS_API_KEY} chars)"
fi

# Check audio cache directory
AUDIO_CACHE_DIR="${AUDIO_CACHE_DIR:-./audio_cache}"
echo
echo "📂 Audio cache directory: $AUDIO_CACHE_DIR"

if [ -d "$AUDIO_CACHE_DIR" ]; then
    echo "✅ Cache directory exists"
    echo "   Files: $(ls -1 "$AUDIO_CACHE_DIR" 2>/dev/null | wc -l)"
else
    echo "📝 Cache directory will be created on first use"
fi

# Check if .env file exists
echo
if [ -f ".env" ]; then
    echo "📄 .env file found"
    # Check if keys are in .env
    if grep -q "DEEPGRAM_API_KEY" .env; then
        echo "   - DEEPGRAM_API_KEY defined in .env"
    fi
    if grep -q "ELEVENLABS_API_KEY" .env; then
        echo "   - ELEVENLABS_API_KEY defined in .env"
    fi
else
    echo "⚠️  No .env file found"
    echo "   Copy .env.example to .env and add your API keys"
fi

echo
echo "🔧 To enable audio service:"
echo "1. Get API keys from:"
echo "   - Deepgram: https://console.deepgram.com/"
echo "   - ElevenLabs: https://elevenlabs.io/"
echo "2. Set environment variables or add to .env file"
echo "3. Restart the service"