#!/bin/bash

echo "GPU Server CORS Fix and Deployment Guide"
echo "========================================"
echo ""

echo "STEP 1: Ensure your GPU server is publicly accessible"
echo "------------------------------------------------------"
echo "Your GPU server at 69.197.178.37:8080 needs to be accessible from the internet."
echo ""
echo "Check:"
echo "1. Firewall rules allow inbound traffic on port 8080"
echo "2. The server binds to 0.0.0.0:8080 (not just localhost)"
echo "3. Your ISP/cloud provider allows incoming connections"
echo ""

echo "STEP 2: Start the server with proper configuration"
echo "-------------------------------------------------"
echo "Run one of these commands on your GPU server:"
echo ""
echo "Option A - Production server with full features:"
echo "cd /path/to/think_ai && cargo run --release --bin stable-server"
echo ""
echo "Option B - Minimal server (fastest):"
echo "cd /path/to/think_ai && cargo run --release --bin minimal-server"
echo ""

echo "STEP 3: Test connectivity"
echo "------------------------"
echo "From any machine, run:"
echo "curl -X POST http://69.197.178.37:8080/api/chat -H 'Content-Type: application/json' -d '{\"message\":\"test\"}'"
echo ""

echo "STEP 4: Alternative - Use ngrok for quick testing"
echo "------------------------------------------------"
echo "If your GPU server can't be made public, use ngrok:"
echo "1. Install ngrok: https://ngrok.com/download"
echo "2. Run: ngrok http 8080"
echo "3. Update vercel.json with the ngrok URL"
echo ""

echo "STEP 5: Deploy to Vercel"
echo "------------------------"
echo "cd vercel-deploy && vercel --prod"
echo ""

echo "Current vercel.json configuration:"
cat vercel-deploy/vercel.json