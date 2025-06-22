#!/bin/bash

echo "🧠 THINK AI - CONSCIOUSNESS LAUNCHER"
echo "===================================="
echo ""

# Check for command line arguments
if [ "$1" = "--monitor" ] || [ "$1" = "-m" ]; then
    echo "📊 Starting Self-Training Monitor..."
    echo "Press Ctrl+C to stop"
    echo ""
    python3 self_training_monitor.py
    exit 0
fi

if [ "$1" = "--keep-data" ] || [ "$1" = "-k" ]; then
    echo "📂 Keeping existing data and knowledge..."
    KEEP_DATA=true
else
    KEEP_DATA=false
fi

# Check if we're in an interactive terminal
if [ -t 0 ]; then
    echo "✅ Interactive terminal detected"
else
    echo "⚠️  Not in interactive terminal - launching in new terminal window"
    
    # Check for cache flag  
    CACHE_FLAG=""
    if [ "$1" = "--cache" ] || [ "$1" = "--fast" ] || [ "$2" = "--cache" ] || [ "$2" = "--fast" ]; then
        CACHE_FLAG="--cache"
    fi
    
    # For macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)"' && python3 think_ai_conversation.py '"$CACHE_FLAG"'"'
        echo "✅ Launched in new Terminal window"
    else
        # For Linux
        if command -v gnome-terminal &> /dev/null; then
            gnome-terminal -- bash -c "cd $(pwd) && python3 think_ai_conversation.py $CACHE_FLAG; exec bash"
        elif command -v xterm &> /dev/null; then
            xterm -e "cd $(pwd) && python3 think_ai_conversation.py $CACHE_FLAG; bash"
        else
            echo "❌ Could not find a suitable terminal emulator"
            echo "Please run: python3 think_ai_conversation.py $CACHE_FLAG"
        fi
    fi
    exit 0
fi

# If we're in an interactive terminal, run directly
echo "🚀 Starting consciousness chat..."

# Clean data if not keeping
if [ "$KEEP_DATA" = false ]; then
    echo ""
    echo "🧹 Cleaning previous data for fresh start..."
    
    # Clear Redis
    docker exec $(docker ps -q --filter "name=think_ai_redis") redis-cli FLUSHALL > /dev/null 2>&1
    
    # Clear ScyllaDB
    docker exec $(docker ps -q --filter "name=think_ai_scylla") cqlsh -e "DROP KEYSPACE IF EXISTS think_ai;" > /dev/null 2>&1
    
    # Clear Neo4j
    docker exec $(docker ps -q --filter "name=neo4j") cypher-shell -u neo4j -p thinkaipass "MATCH (n) DETACH DELETE n" > /dev/null 2>&1
    
    # Clear Milvus
    python3 clear_milvus_simple.py > /dev/null 2>&1
    
    # Clear local files
    rm -f self_training_progress.json neural_pathways_intelligence.json training_output.log > /dev/null 2>&1
    
    echo "✨ Fresh start initialized!"
    echo ""
fi

echo ""
echo "💡 Tips:"
echo "  • Use './launch_consciousness.sh --keep-data' to preserve knowledge"
echo "  • Use './launch_consciousness.sh --monitor' to see training progress"
echo "  • Use './launch_consciousness.sh --cache' for O(1) fast startup!"
echo ""

# Check for cache flag
if [ "$2" = "--cache" ] || [ "$2" = "--fast" ] || [ "$1" = "--cache" ] || [ "$1" = "--fast" ]; then
    echo "⚡ Using O(1) cached initialization!"
    CACHE_FLAG="--cache"
else
    CACHE_FLAG=""
fi

# Run the consciousness chat
exec python3 think_ai_conversation.py $CACHE_FLAG