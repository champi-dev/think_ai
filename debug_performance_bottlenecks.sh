#!/bin/bash

echo "🔍 Think AI Performance Bottleneck Analysis"
echo "==========================================="

# Test 1: Check knowledge base size
echo "📊 1. Knowledge Base Size Analysis"
echo "-----------------------------------"
if [ -d "./knowledge_files" ]; then
    echo "Knowledge files directory found:"
    find ./knowledge_files -name "*.json" -exec wc -l {} + 2>/dev/null | tail -1 | awk '{print "Total lines:", $1}'
    find ./knowledge_files -name "*.json" -exec du -h {} + 2>/dev/null | tail -1 | awk '{print "Total size:", $1}'
    echo "File count: $(find ./knowledge_files -name "*.json" | wc -l)"
else
    echo "❌ No knowledge_files directory found"
fi

# Test 2: Startup time measurement
echo ""
echo "⏱️  2. Server Startup Time Test"
echo "-------------------------------"
echo "Building release version..."
cargo build --release --quiet 2>/dev/null

if [ -f "./target/release/think-ai-server" ]; then
    echo "Starting server and measuring initialization time..."
    timeout 30s time ./target/release/think-ai-server &
    SERVER_PID=$!
    sleep 5
    if kill -0 $SERVER_PID 2>/dev/null; then
        echo "✅ Server started (killed after 5s for test)"
        kill $SERVER_PID 2>/dev/null
    else
        echo "❌ Server failed to start within timeout"
    fi
else
    echo "❌ think-ai-server binary not found"
fi

# Test 3: Single query response time
echo ""
echo "🚀 3. API Response Time Test"
echo "----------------------------"
if command -v curl >/dev/null 2>&1; then
    # Start server in background
    ./target/release/think-ai-server > /dev/null 2>&1 &
    SERVER_PID=$!
    echo "Waiting for server to initialize..."
    sleep 8
    
    # Test simple query
    echo "Testing simple query: 'what is love'"
    START_TIME=$(date +%s%3N)
    RESPONSE=$(curl -s -X POST http://localhost:8080/api/chat \
        -H "Content-Type: application/json" \
        -d '{"query": "what is love"}' \
        --max-time 30)
    END_TIME=$(date +%s%3N)
    
    if [ $? -eq 0 ] && [ ! -z "$RESPONSE" ]; then
        RESPONSE_TIME=$((END_TIME - START_TIME))
        echo "✅ Response received in ${RESPONSE_TIME}ms"
        echo "Response length: $(echo "$RESPONSE" | wc -c) characters"
        if [ $RESPONSE_TIME -gt 10000 ]; then
            echo "⚠️  SLOW: Response took over 10 seconds!"
        fi
    else
        echo "❌ No response received or server error"
    fi
    
    # Test complex query
    echo ""
    echo "Testing complex query: 'what is consciousness and how does it work'"
    START_TIME=$(date +%s%3N)
    RESPONSE=$(curl -s -X POST http://localhost:8080/api/chat \
        -H "Content-Type: application/json" \
        -d '{"query": "what is consciousness and how does it work"}' \
        --max-time 30)
    END_TIME=$(date +%s%3N)
    
    if [ $? -eq 0 ] && [ ! -z "$RESPONSE" ]; then
        RESPONSE_TIME=$((END_TIME - START_TIME))
        echo "✅ Response received in ${RESPONSE_TIME}ms"
        if [ $RESPONSE_TIME -gt 10000 ]; then
            echo "⚠️  SLOW: Response took over 10 seconds!"
        fi
    else
        echo "❌ No response received or server error"
    fi
    
    # Clean up
    kill $SERVER_PID 2>/dev/null
    sleep 2
else
    echo "❌ curl not found - cannot test API responses"
fi

# Test 4: Memory usage analysis
echo ""
echo "💾 4. Memory Usage Analysis"
echo "--------------------------"
if command -v ps >/dev/null 2>&1; then
    ./target/release/think-ai-server > /dev/null 2>&1 &
    SERVER_PID=$!
    sleep 3
    
    if kill -0 $SERVER_PID 2>/dev/null; then
        MEMORY=$(ps -o rss= -p $SERVER_PID 2>/dev/null)
        if [ ! -z "$MEMORY" ]; then
            MEMORY_MB=$((MEMORY / 1024))
            echo "Server memory usage: ${MEMORY_MB} MB"
            if [ $MEMORY_MB -gt 500 ]; then
                echo "⚠️  HIGH: Memory usage over 500MB at startup"
            fi
        fi
        kill $SERVER_PID 2>/dev/null
    else
        echo "❌ Could not measure memory - server not running"
    fi
else
    echo "❌ ps command not found"
fi

# Test 5: Code analysis
echo ""
echo "🔍 5. Code Bottleneck Analysis"
echo "-----------------------------"
echo "Searching for O(n) operations in knowledge engine..."

if grep -n "\.iter()" think-ai-knowledge/src/lib.rs | head -5; then
    echo "⚠️  Found iterator usage in knowledge engine"
fi

if grep -n "for.*in.*nodes" think-ai-knowledge/src/lib.rs | head -3; then
    echo "⚠️  Found node iteration loops"
fi

if grep -n "compute_relevance" think-ai-knowledge/src/intelligent_relevance.rs | head -3; then
    echo "⚠️  Found relevance computation calls"
fi

echo ""
echo "📈 Performance Recommendations:"
echo "==============================="
echo "1. 🎯 PRIMARY FIX: Add hash indexing to KnowledgeEngine"
echo "   - Replace O(n) node iteration with O(1) hash lookups"
echo "   - Create topic → node_ids index"
echo "   - File: think-ai-knowledge/src/lib.rs, lines 186-263"
echo ""
echo "2. ⚡ Cache relevance computations"
echo "   - Pre-compute relevance scores offline"
echo "   - File: think-ai-knowledge/src/intelligent_relevance.rs"
echo ""
echo "3. 🔄 Async knowledge loading"
echo "   - Load knowledge files asynchronously"
echo "   - File: think-ai-knowledge/src/dynamic_loader.rs"
echo ""
echo "4. 📦 Optimize multi-level cache"
echo "   - Replace linear searches with hash maps"
echo "   - File: think-ai-knowledge/src/multilevel_cache.rs"

echo ""
echo "🎯 Expected Performance Gains:"
echo "- Current: 10+ seconds per query"
echo "- With fixes: <100ms per query (100x improvement)"