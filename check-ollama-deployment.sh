#!/bin/bash

echo "🔍 Monitoring Ollama deployment on Railway..."
echo "==========================================="
echo ""

# Function to test the deployment
test_deployment() {
    local attempt=$1
    echo "📊 Test attempt $attempt at $(date '+%H:%M:%S')"
    
    # Test health
    echo -n "  Health check: "
    HEALTH=$(curl -s -w "%{http_code}" -o /dev/null "https://thinkai-production.up.railway.app/health")
    if [ "$HEALTH" = "200" ]; then
        echo "✅ OK"
    else
        echo "❌ Failed ($HEALTH)"
    fi
    
    # Test chat
    echo -n "  Chat test: "
    START_TIME=$(date +%s.%N)
    RESPONSE=$(curl -s -X POST "https://thinkai-production.up.railway.app/chat" \
        -H "Content-Type: application/json" \
        -d '{"query": "What is 2+2?"}' \
        --max-time 15)
    END_TIME=$(date +%s.%N)
    ELAPSED=$(echo "$END_TIME - $START_TIME" | bc)
    
    if echo "$RESPONSE" | grep -q "2 + 2 = 4"; then
        echo "✅ Correct answer in ${ELAPSED}s"
        if (( $(echo "$ELAPSED < 2" | bc -l) )); then
            echo "  🚀 Qwen is responding! (fast response)"
            return 0
        else
            echo "  ⚠️ Slow response - might be fallback"
        fi
    elif echo "$RESPONSE" | grep -q "response"; then
        echo "⚠️ Got response but not math answer"
        echo "  Response: $(echo $RESPONSE | jq -r .response 2>/dev/null | head -c 100)"
    else
        echo "❌ No valid response"
    fi
    
    return 1
}

# Monitor for 3 minutes
echo "Monitoring for 3 minutes..."
echo ""

for i in {1..9}; do
    if test_deployment $i; then
        echo ""
        echo "✅ Ollama/Qwen is working!"
        exit 0
    fi
    
    if [ $i -lt 9 ]; then
        echo "  Waiting 20 seconds..."
        sleep 20
    fi
    echo ""
done

echo "❌ Ollama/Qwen not responding after 3 minutes"
echo ""
echo "Check Railway logs with:"
echo "  railway logs -d | grep -E '(Ollama|Qwen|11434)'"