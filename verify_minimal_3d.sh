#!/bin/bash

echo "🔍 Verifying minimal_3d webapp deployment..."
echo ""

# Check if server is running
if curl -s http://localhost:8080/ > /dev/null 2>&1; then
    echo "✅ Server is responding on port 8080"
    
    # Check for O(1) optimizations
    if curl -s http://localhost:8080/ | grep -q "O(1)"; then
        echo "✅ O(1) optimizations detected"
    else
        echo "❌ O(1) optimizations NOT found - server may be running old version"
    fi
    
    # Check for lookup tables
    if curl -s http://localhost:8080/ | grep -q "lookup tables"; then
        echo "✅ Pre-computed lookup tables detected"
    else
        echo "❌ Lookup tables NOT found - server may be running old version"
    fi
    
    # Check for fastSin/fastCos functions
    if curl -s http://localhost:8080/ | grep -q "fastSin"; then
        echo "✅ Fast trigonometric functions detected"
    else
        echo "❌ Fast trig functions NOT found - server may be running old version"
    fi
    
    # Count lines to verify it's the full file
    lines=$(curl -s http://localhost:8080/ | wc -l)
    echo ""
    echo "📊 HTML file has $lines lines"
    if [ "$lines" -gt 1600 ]; then
        echo "✅ This appears to be the complete minimal_3d.html (1632 lines)"
    else
        echo "❌ This appears to be the old version (expected ~1632 lines)"
    fi
else
    echo "❌ Server is NOT responding on port 8080"
fi

echo ""
echo "💡 To manually check: curl http://localhost:8080/ | grep 'O(1)'"