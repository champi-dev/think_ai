#!/bin/bash

echo "🔍 Monitoring Railway deployment for Ollama and Qwen availability..."
echo "=================================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Wait for initial deployment
echo "⏳ Waiting for deployment to start..."
sleep 30

# Function to check deployment status
check_deployment() {
    echo -e "\n📊 Checking deployment status at $(date '+%Y-%m-%d %H:%M:%S')"
    
    # Check if service is running
    if railway status 2>/dev/null | grep -q "running"; then
        echo -e "${GREEN}✅ Service is running${NC}"
        
        # Get the service URL
        SERVICE_URL=$(railway status 2>/dev/null | grep -oP 'https://[^ ]+' | head -1)
        if [ ! -z "$SERVICE_URL" ]; then
            echo -e "🌐 Service URL: ${SERVICE_URL}"
            
            # Check health endpoint
            echo -n "🏥 Checking health endpoint... "
            if curl -s "${SERVICE_URL}/health" >/dev/null 2>&1; then
                echo -e "${GREEN}Healthy${NC}"
            else
                echo -e "${RED}Not responding${NC}"
            fi
            
            # Test chat endpoint
            echo -n "💬 Testing chat endpoint... "
            RESPONSE=$(curl -s -X POST "${SERVICE_URL}/chat" \
                -H "Content-Type: application/json" \
                -d '{"query": "hi"}' 2>/dev/null | head -c 100)
            
            if [[ "$RESPONSE" == *"Thinking"* ]]; then
                echo -e "${YELLOW}Still thinking (Qwen might be loading)${NC}"
            elif [ ! -z "$RESPONSE" ]; then
                echo -e "${GREEN}Responding normally${NC}"
                echo "   Response preview: ${RESPONSE}..."
            else
                echo -e "${RED}No response${NC}"
            fi
        fi
    else
        echo -e "${YELLOW}⏳ Service not yet running${NC}"
    fi
}

# Monitor for 5 minutes
END_TIME=$(($(date +%s) + 300))

while [ $(date +%s) -lt $END_TIME ]; do
    check_deployment
    
    # Check logs for Ollama/Qwen status
    echo -e "\n📋 Recent deployment logs:"
    railway logs --tail 20 2>/dev/null | grep -E "(Ollama|Qwen|Starting|Error|Failed|Success|qwen2.5)" | tail -10
    
    echo -e "\n---"
    sleep 20
done

echo -e "\n✅ Monitoring complete!"
echo "Run this script again to continue monitoring, or use:"
echo "  railway logs --tail 50"
echo "to see more detailed logs."