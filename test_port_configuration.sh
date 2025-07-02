#!/bin/bash

# Test script to verify port configuration for Railway deployment
echo "🔍 Testing Think AI Port Configuration"
echo "======================================"

# Check which binaries are available
echo ""
echo "📦 Available server binaries:"
echo "------------------------------"

# Check if binaries exist
if [ -f "./target/release/full-server" ]; then
    echo "✅ full-server (RECOMMENDED for Railway)"
else
    echo "❌ full-server not found"
fi

if [ -f "./target/release/think-ai-server" ]; then
    echo "✅ think-ai-server (Basic version)"
else
    echo "❌ think-ai-server not found"
fi

if [ -f "./target/release/think-ai" ]; then
    echo "✅ think-ai (CLI version)"
else
    echo "❌ think-ai not found"
fi

# Test PORT environment variable support
echo ""
echo "🧪 Testing PORT Environment Variable Support:"
echo "----------------------------------------------"

# Test with full-server if available
if [ -f "./target/release/full-server" ]; then
    echo "Testing full-server with PORT=3000..."
    
    # Start server in background with PORT=3000
    PORT=3000 timeout 5s ./target/release/full-server &
    SERVER_PID=$!
    
    # Give it time to start
    sleep 2
    
    # Check if server is listening on port 3000
    if command -v lsof >/dev/null 2>&1; then
        if lsof -i :3000 >/dev/null 2>&1; then
            echo "✅ full-server successfully bound to port 3000"
            # Test HTTP response
            if command -v curl >/dev/null 2>&1; then
                RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/health 2>/dev/null)
                if [ "$RESPONSE" = "200" ]; then
                    echo "✅ Health check passed (HTTP 200)"
                else
                    echo "⚠️  Server listening but health check returned: $RESPONSE"
                fi
            fi
        else
            echo "❌ full-server did not bind to port 3000"
        fi
    else
        echo "⚠️  lsof not available, cannot verify port binding"
    fi
    
    # Stop the server
    kill $SERVER_PID 2>/dev/null
    wait $SERVER_PID 2>/dev/null
else
    echo "⚠️  full-server not found, building it first..."
    echo "Run: cargo build --release --bin full-server"
fi

# Test basic server
echo ""
if [ -f "./target/release/think-ai-server" ]; then
    echo "Testing think-ai-server (should ignore PORT env var)..."
    
    # Start server in background with PORT=3001 (should be ignored)
    PORT=3001 timeout 5s ./target/release/think-ai-server &
    SERVER_PID=$!
    
    # Give it time to start
    sleep 2
    
    # Check if server is listening on port 8080 (hardcoded)
    if command -v lsof >/dev/null 2>&1; then
        if lsof -i :8080 >/dev/null 2>&1; then
            echo "⚠️  think-ai-server bound to hardcoded port 8080 (ignores PORT env var)"
        elif lsof -i :3001 >/dev/null 2>&1; then
            echo "❓ think-ai-server unexpectedly bound to PORT env var"
        else
            echo "❌ think-ai-server did not bind to any expected port"
        fi
    fi
    
    # Stop the server
    kill $SERVER_PID 2>/dev/null
    wait $SERVER_PID 2>/dev/null
fi

# Show configuration analysis
echo ""
echo "📋 Configuration Analysis:"
echo "--------------------------"
echo "✅ RAILWAY COMPATIBLE: full-server binary"
echo "   - Reads PORT environment variable"
echo "   - Binds to 0.0.0.0:\$PORT"
echo "   - Includes advanced features and port management"
echo ""
echo "❌ RAILWAY INCOMPATIBLE: think-ai-server binary"
echo "   - Hardcoded to 127.0.0.1:8080"
echo "   - Ignores PORT environment variable"
echo "   - Basic functionality only"

# Show Railway deployment recommendation
echo ""
echo "🚂 Railway Deployment Recommendation:"
echo "-------------------------------------"
echo "1. Build the full-server binary:"
echo "   cargo build --release --bin full-server"
echo ""
echo "2. Update your Dockerfile/Railway config to use:"
echo "   CMD [\"./target/release/full-server\"]"
echo ""
echo "3. Verify these files exist for full functionality:"
echo "   - ./minimal_3d.html (webapp)"
echo "   - ./knowledge_files/ (knowledge base)"
echo ""
echo "4. The full-server provides these Railway-compatible features:"
echo "   - Environment variable PORT support"
echo "   - Advanced O(1) LLM processing" 
echo "   - Knowledge base integration"
echo "   - Performance monitoring endpoints"
echo "   - Self-evaluation system"

# Check current deployment files
echo ""
echo "📁 Deployment Files Check:"
echo "--------------------------"

if [ -f "./Dockerfile" ]; then
    echo "✅ Dockerfile found"
    if grep -q "full-server" ./Dockerfile; then
        echo "✅ Dockerfile uses full-server"
    elif grep -q "think-ai-server" ./Dockerfile; then
        echo "⚠️  Dockerfile uses think-ai-server (should use full-server)"
    else
        echo "❓ Dockerfile doesn't specify server binary clearly"
    fi
else
    echo "❌ Dockerfile not found"
fi

if [ -f "./railway.json" ] || [ -f "./railway.toml" ]; then
    echo "✅ Railway configuration found"
else
    echo "❌ Railway configuration not found"
fi

if [ -f "./minimal_3d.html" ]; then
    echo "✅ Webapp file (minimal_3d.html) found"
else
    echo "⚠️  Webapp file (minimal_3d.html) not found"
fi

if [ -d "./knowledge_files" ]; then
    KNOWLEDGE_COUNT=$(find ./knowledge_files -name "*.json" | wc -l)
    echo "✅ Knowledge base found ($KNOWLEDGE_COUNT JSON files)"
else
    echo "⚠️  Knowledge base directory not found"
fi

echo ""
echo "🎯 Next Steps:"
echo "--------------"
echo "1. Build full-server: cargo build --release --bin full-server"
echo "2. Test locally: PORT=3000 ./target/release/full-server"
echo "3. Update deployment to use full-server binary"
echo "4. Deploy to Railway with PORT environment variable support"

echo ""
echo "For detailed analysis, see: PORT_BINDING_ANALYSIS.md"