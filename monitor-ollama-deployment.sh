#!/bin/bash

echo "🔍 Monitoring Ollama deployment..."
echo "================================"
echo ""

URL="https://thinkai-production.up.railway.app"

# Function to test
test_deployment() {
    echo "$(date '+%H:%M:%S') Testing..."
    
    # Health check
    HEALTH=$(curl -s -w "HTTP:%{http_code}" "$URL/health" 2>/dev/null)
    echo "  Health: $HEALTH"
    
    # Quick chat test
    CHAT=$(curl -s -X POST "$URL/chat" \
        -H "Content-Type: application/json" \
        -d '{"query": "2+2"}' \
        --max-time 5 2>/dev/null | jq -r .response 2>/dev/null | head -c 50)
    
    if [[ "$CHAT" == *"4"* ]]; then
        echo "  Chat: ✅ Working! Response: $CHAT"
        return 0
    else
        echo "  Chat: ⏳ Not ready yet"
        return 1
    fi
}

# Monitor for 5 minutes
for i in {1..15}; do
    if test_deployment; then
        echo ""
        echo "✅ Ollama is working on Railway!"
        exit 0
    fi
    
    if [ $i -lt 15 ]; then
        sleep 20
    fi
done

echo "❌ Timeout after 5 minutes"