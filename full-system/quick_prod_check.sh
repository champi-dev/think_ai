#!/bin/bash

# Quick production health check

echo "🔍 Quick ThinkAI Production Check"
echo "================================="

# Check main site
echo -n "🌐 Main site (https://thinkai.lat): "
status=$(curl -s -o /dev/null -w "%{http_code}" https://thinkai.lat)
if [ "$status" = "200" ]; then
    echo "✅ OK ($status)"
else
    echo "❌ Failed ($status)"
fi

# Check health endpoint
echo -n "🏥 Health endpoint: "
health=$(curl -s https://thinkai.lat/health 2>/dev/null)
if echo "$health" | grep -q "healthy"; then
    echo "✅ Healthy"
else
    echo "❌ Not responding"
fi

# Check metrics endpoint
echo -n "📊 Metrics endpoint: "
metrics=$(curl -s https://thinkai.lat/api/metrics 2>/dev/null)
if echo "$metrics" | grep -q "system_metrics"; then
    cpu=$(echo "$metrics" | jq -r '.system_metrics.cpu_usage // "N/A"' 2>/dev/null)
    mem=$(echo "$metrics" | jq -r '.system_metrics.memory_usage // "N/A"' 2>/dev/null)
    reqs=$(echo "$metrics" | jq -r '.system_metrics.total_requests // "N/A"' 2>/dev/null)
    echo "✅ OK (CPU: ${cpu}%, Memory: ${mem}%, Requests: $reqs)"
else
    echo "❌ Not accessible"
fi

# Check dashboard
echo -n "🎨 Dashboard (https://thinkai.lat/stats): "
dashboard_status=$(curl -s -o /dev/null -w "%{http_code}" https://thinkai.lat/stats)
if [ "$dashboard_status" = "200" ]; then
    echo "✅ Accessible"
else
    echo "❌ Failed ($dashboard_status)"
fi

# Memory leak quick test
echo ""
echo "🧪 Quick Memory Leak Test (10 requests)..."
initial_mem=$(curl -s https://thinkai.lat/api/metrics | jq -r '.system_metrics.memory_usage // 0' 2>/dev/null)
echo "Initial memory: ${initial_mem}%"

# Make 10 quick requests
for i in {1..10}; do
    curl -s -X POST https://thinkai.lat/api/chat \
        -H "Content-Type: application/json" \
        -d '{"message":"Memory test '$(date +%s)'"}' > /dev/null 2>&1
done

sleep 2
final_mem=$(curl -s https://thinkai.lat/api/metrics | jq -r '.system_metrics.memory_usage // 0' 2>/dev/null)
echo "Final memory: ${final_mem}%"

increase=$(echo "$final_mem - $initial_mem" | bc 2>/dev/null || echo "0")
echo "Memory increase: ${increase}%"

if (( $(echo "$increase > 1" | bc -l 2>/dev/null || echo 0) )); then
    echo "⚠️  Memory increased after just 10 requests"
else
    echo "✅ Memory stable"
fi

echo ""
echo "📸 To analyze dashboard visually:"
echo "   1. Open https://thinkai.lat/stats"
echo "   2. Take a screenshot"
echo "   3. Check analyze_dashboard_screenshot.md for what to look for"