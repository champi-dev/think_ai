#!/bin/bash

echo "=== Final Build for Think AI Full System ==="
echo "Date: $(date)"
echo ""

cd /home/champi/Dev/think_ai/full-system

echo "Step 1: Building full-system with cargo..."
echo "========================================="

if cargo build --release 2>&1 | tee build-output.log; then
    echo ""
    echo "✅ BUILD SUCCESSFUL!"
    echo ""
    echo "Binary location: ./target/release/think-ai-full"
    echo ""
    echo "To run the server:"
    echo "  ./target/release/think-ai-full"
    echo ""
    echo "The server will start on http://localhost:8080"
    echo "Features included:"
    echo "  - Web interface with glass morphism UI"
    echo "  - WebSocket real-time chat"
    echo "  - O(1) knowledge search"
    echo "  - AI consciousness monitoring"
    echo "  - System statistics dashboard"
else
    echo ""
    echo "❌ BUILD FAILED"
    echo ""
    echo "Error summary:"
    grep -E "error\[E[0-9]+\]" build-output.log | sort | uniq -c | sort -nr | head -10
    echo ""
    echo "Total errors: $(grep -c "error\[E" build-output.log)"
fi