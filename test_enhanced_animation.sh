#!/bin/bash

echo "🎬 Testing Enhanced Award-Winning 3D Animation"
echo "=============================================="

# Check if server is running
echo "📡 Checking server status..."
if curl -s http://localhost:8080/health > /dev/null; then
    echo "✅ Server is running on http://localhost:8080"
else
    echo "🚀 Starting server..."
    cargo build --release
    ./target/release/full-server &
    SERVER_PID=$!
    echo "🔄 Waiting for server to start..."
    sleep 3
fi

echo ""
echo "🌟 Enhanced Animation Features:"
echo "==============================="
echo "• Ultra-slow elegant oscillation (0.0003-0.0007 frequency)"
echo "• Multi-layered glow effects (outer, middle, core)"
echo "• Dynamic color transitions with harmonic waves" 
echo "• Elegant spiral motion with circular components"
echo "• Award-winning gradient connections with energy flow"
echo "• Quantum wave emanations with dash patterns"
echo "• Subtle background quantum flow patterns"
echo "• Dynamic depth with screen overlays"
echo "• Enhanced field density (30 points)"
echo "• Sophisticated pulse and shimmer effects"

echo ""
echo "🎯 Animation Performance:"
echo "========================"
echo "• Time progression: 0.8x (ultra-slow)"
echo "• Fade intensity: Dynamic with sine wave"
echo "• Field connections: Gradient-based with shadows"
echo "• Energy ripples: Rare (0.5% chance) for elegance"
echo "• Visual richness: Multi-layered with 3 glow layers"

echo ""
echo "🌐 Access the enhanced webapp:"
echo "=============================="
echo "Open: http://localhost:8080"
echo ""
echo "🎨 What you'll see:"
echo "• Slowly pulsing quantum field points"
echo "• Elegant circular and spiral motion"
echo "• Beautiful color gradients (blue to violet spectrum)"
echo "• Smooth energy flow connections"
echo "• Occasional quantum wave ripples"
echo "• Award-winning visual depth and effects"

echo ""
echo "🧪 Test the animation by:"
echo "========================"
echo "1. Opening the webapp in your browser"
echo "2. Observing the slow, elegant quantum field motion"
echo "3. Notice the multi-layered glow effects"
echo "4. Watch for rare energy ripples and waves"
echo "5. See the dynamic color transitions"
echo "6. Test the chat functionality with hierarchical knowledge"

echo ""
echo "Press Ctrl+C to stop the server when done testing."