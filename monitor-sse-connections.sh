#!/bin/bash

echo "SSE Connection Monitor"
echo "====================="
echo ""
echo "This script monitors active SSE connections to detect hanging issues."
echo ""

while true; do
    clear
    echo "SSE Connection Monitor - $(date)"
    echo "========================================"
    echo ""
    
    # Check active connections to port 8080
    echo "Active connections to port 8080:"
    netstat -tn 2>/dev/null | grep :8080 | grep ESTABLISHED | wc -l
    echo ""
    
    # Show connection details
    echo "Connection details:"
    netstat -tn 2>/dev/null | grep :8080 | grep ESTABLISHED | head -10
    echo ""
    
    # Check server process
    echo "Server process status:"
    ps aux | grep -E "(think-ai|stable-server)" | grep -v grep | head -5
    echo ""
    
    # Check for any TIME_WAIT connections (could indicate connection churn)
    echo "TIME_WAIT connections (recently closed):"
    netstat -tn 2>/dev/null | grep :8080 | grep TIME_WAIT | wc -l
    echo ""
    
    echo "Press Ctrl+C to exit"
    echo "Refreshing in 5 seconds..."
    
    sleep 5
done