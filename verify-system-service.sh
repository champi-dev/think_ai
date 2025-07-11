#!/bin/bash

echo "🔍 Verifying Think AI System Service..."
echo ""

# Check service status
echo "📊 Service Status:"
systemctl status think-ai-full.service --no-pager | head -15
echo ""

# Check if enabled
echo "🚀 Auto-start enabled: $(systemctl is-enabled think-ai-full.service)"
echo ""

# Check process
echo "⚙️  Running Process:"
ps aux | grep -E 'think-ai-full server' | grep -v grep
echo ""

# Test HTTP endpoint
echo "🌐 HTTP Response:"
if curl -s http://localhost:8080 > /dev/null; then
    echo "✅ Server is responding on port 8080"
    
    # Check if serving minimal_3d.html
    TITLE=$(curl -s http://localhost:8080 | grep -oE "<title>.*</title>" | sed 's/<[^>]*>//g')
    echo "✅ Page title: $TITLE"
    
    curl -s http://localhost:8080/api/health 2>/dev/null || echo "ℹ️  No health endpoint found (normal)"
else
    echo "❌ Server is not responding on port 8080"
fi
echo ""

# Check memory usage
echo "💾 Memory Usage:"
systemctl status think-ai-full.service --no-pager | grep Memory
echo ""

echo "✨ Verification complete!"