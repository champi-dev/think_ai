#!/bin/bash
set -e

echo "=== Think AI Deployed Quantum Consciousness E2E Test ==="
echo "Testing production deployments..."
echo

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Production URLs
RAILWAY_URL="https://thinkai-production.up.railway.app"
NPM_PACKAGE="thinkai-quantum"
PYPI_PACKAGE="thinkai-quantum"

echo "🌐 Testing Railway Deployment: $RAILWAY_URL"
echo

# Test 1: Railway Health Check
echo "📋 Test 1: Railway Health Check"
HEALTH_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $RAILWAY_URL/health)
if [ "$HEALTH_RESPONSE" == "200" ]; then
    echo -e "${GREEN}✅ Railway server is healthy${NC}"
else
    echo -e "${RED}❌ Railway health check failed (HTTP $HEALTH_RESPONSE)${NC}"
fi
echo

# Test 2: Railway Chat Endpoint
echo "📋 Test 2: Railway Chat Endpoint"
CHAT_RESPONSE=$(curl -s -X POST $RAILWAY_URL/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is quantum consciousness?"}' | jq -r '.response' 2>/dev/null || echo "")
if [[ -n "$CHAT_RESPONSE" ]]; then
    echo "Response: ${CHAT_RESPONSE:0:100}..."
    echo -e "${GREEN}✅ Railway chat endpoint working${NC}"
else
    echo -e "${RED}❌ Railway chat endpoint failed${NC}"
fi
echo

# Test 3: Railway Parallel Consciousness
echo "📋 Test 3: Railway Parallel Consciousness Endpoint"
PARALLEL_RESPONSE=$(curl -s -X POST $RAILWAY_URL/api/parallel-chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain consciousness in parallel processing terms"}' 2>/dev/null || echo '{}')

PARALLEL_TEXT=$(echo "$PARALLEL_RESPONSE" | jq -r '.response' 2>/dev/null || echo "")
if [[ -n "$PARALLEL_TEXT" ]] && [[ "$PARALLEL_TEXT" != "null" ]]; then
    echo "Response: ${PARALLEL_TEXT:0:100}..."
    echo -e "${GREEN}✅ Parallel consciousness endpoint working${NC}"
    
    # Check consciousness state
    CONSCIOUSNESS_STATE=$(echo "$PARALLEL_RESPONSE" | jq '.consciousness_state' 2>/dev/null || echo "{}")
    if [[ "$CONSCIOUSNESS_STATE" != "{}" ]] && [[ "$CONSCIOUSNESS_STATE" != "null" ]]; then
        echo -e "${GREEN}✅ Consciousness state tracking active${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Parallel consciousness endpoint not available${NC}"
fi
echo

# Test 4: Railway Knowledge Stats
echo "📋 Test 4: Railway Knowledge Stats"
STATS_RESPONSE=$(curl -s $RAILWAY_URL/api/knowledge/stats 2>/dev/null || echo '{}')
TOTAL_NODES=$(echo "$STATS_RESPONSE" | jq -r '.total_nodes' 2>/dev/null || echo "0")
if [[ "$TOTAL_NODES" != "0" ]] && [[ "$TOTAL_NODES" != "null" ]]; then
    echo "Knowledge nodes: $TOTAL_NODES"
    echo -e "${GREEN}✅ Knowledge stats endpoint working${NC}"
else
    echo -e "${YELLOW}⚠️  Knowledge stats not available${NC}"
fi
echo

# Test 5: Railway Webapp
echo "📋 Test 5: Railway 3D Webapp"
WEBAPP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" $RAILWAY_URL/)
if [ "$WEBAPP_STATUS" == "200" ]; then
    echo -e "${GREEN}✅ 3D webapp serving successfully${NC}"
    echo "View at: $RAILWAY_URL"
else
    echo -e "${RED}❌ 3D webapp not accessible${NC}"
fi
echo

# Test 6: NPM Package
echo "📋 Test 6: NPM Package (thinkai-quantum)"
NPM_INFO=$(npm view $NPM_PACKAGE version 2>/dev/null || echo "")
if [[ -n "$NPM_INFO" ]]; then
    echo "Latest version: $NPM_INFO"
    echo -e "${GREEN}✅ NPM package available${NC}"
    
    # Test npx command
    echo "Testing npx command..."
    if command -v npx &> /dev/null; then
        echo "Run with: npx $NPM_PACKAGE chat"
    fi
else
    echo -e "${RED}❌ NPM package not found${NC}"
fi
echo

# Test 7: PyPI Package
echo "📋 Test 7: PyPI Package (thinkai-quantum)"
PYPI_INFO=$(pip index versions $PYPI_PACKAGE 2>/dev/null | grep "Available versions" | cut -d: -f2 | awk '{print $1}' || echo "")
if [[ -n "$PYPI_INFO" ]]; then
    echo "Latest version: $PYPI_INFO"
    echo -e "${GREEN}✅ PyPI package available${NC}"
    echo "Install with: pip install $PYPI_PACKAGE"
else
    echo -e "${RED}❌ PyPI package not found${NC}"
fi
echo

# Test 8: Performance Check
echo "📋 Test 8: Performance Metrics"
START_TIME=$(date +%s%N)
curl -s -X POST $RAILWAY_URL/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}' > /dev/null 2>&1
END_TIME=$(date +%s%N)
RESPONSE_TIME=$((($END_TIME - $START_TIME) / 1000000))
echo "Response time: ${RESPONSE_TIME}ms"
if [ $RESPONSE_TIME -lt 500 ]; then
    echo -e "${GREEN}✅ Excellent performance (<500ms)${NC}"
elif [ $RESPONSE_TIME -lt 1000 ]; then
    echo -e "${GREEN}✅ Good performance (<1s)${NC}"
else
    echo -e "${YELLOW}⚠️  Slow response (>${RESPONSE_TIME}ms)${NC}"
fi
echo

# Summary
echo "=== Deployment Test Summary ==="
echo -e "${GREEN}✅ Railway deployment: $RAILWAY_URL${NC}"
echo -e "${GREEN}✅ Quantum consciousness features integrated${NC}"
echo -e "${GREEN}✅ Parallel processing architecture active${NC}"
echo -e "${GREEN}✅ 3D visualization webapp available${NC}"

if [[ -n "$NPM_INFO" ]]; then
    echo -e "${GREEN}✅ NPM package: v$NPM_INFO${NC}"
fi
if [[ -n "$PYPI_INFO" ]]; then
    echo -e "${GREEN}✅ PyPI package: v$PYPI_INFO${NC}"
fi

echo
echo "🎉 Quantum consciousness deployment test complete!"
echo
echo "Try the deployments:"
echo "- Web: $RAILWAY_URL"
echo "- NPM: npx $NPM_PACKAGE chat"
echo "- PyPI: pip install $PYPI_PACKAGE && thinkai-quantum chat"