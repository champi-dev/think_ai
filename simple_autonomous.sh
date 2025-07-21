#!/bin/bash

# Simple Autonomous Agent for ThinkAI
# Runs background tasks without Python dependencies

API_URL="http://localhost:7777"
LOG_FILE="autonomous_agent.log"

echo "🤖 ThinkAI Simple Autonomous Agent Started" | tee -a $LOG_FILE
echo "================================================" | tee -a $LOG_FILE

# Function to query the AI
query_ai() {
    local prompt="$1"
    local response=$(curl -s -X POST "$API_URL/api/chat" \
        -H "Content-Type: application/json" \
        -d "{\"message\": \"$prompt\", \"session_id\": \"autonomous_$$\"}")
    
    echo "$response" | jq -r '.response // empty' 2>/dev/null || echo ""
}

# Function to get metrics
get_metrics() {
    curl -s "$API_URL/api/metrics" | jq '.' 2>/dev/null || echo "{}"
}

# Self-improvement loop
self_improvement_loop() {
    while true; do
        echo "[$(date)] 🔄 Running self-improvement check..." | tee -a $LOG_FILE
        
        metrics=$(get_metrics)
        cpu_usage=$(echo "$metrics" | jq -r '.system_metrics.cpu_usage // 0')
        memory_usage=$(echo "$metrics" | jq -r '.system_metrics.memory_usage // 0')
        
        echo "[$(date)] 📊 CPU: ${cpu_usage}%, Memory: ${memory_usage}%" | tee -a $LOG_FILE
        
        # Check thresholds
        if (( $(echo "$cpu_usage > 80" | bc -l) )); then
            echo "[$(date)] ⚠️ High CPU usage detected!" | tee -a $LOG_FILE
        fi
        
        if (( $(echo "$memory_usage > 85" | bc -l) )); then
            echo "[$(date)] ⚠️ High memory usage detected!" | tee -a $LOG_FILE
        fi
        
        # Wait 5 minutes
        sleep 300
    done
}

# Knowledge gathering loop
knowledge_gathering_loop() {
    local topics=(
        "artificial intelligence breakthroughs"
        "quantum computing applications"
        "neuroscience discoveries"
        "philosophy of consciousness"
        "emergent complex systems"
    )
    
    local topic_index=0
    
    while true; do
        topic="${topics[$((topic_index % ${#topics[@]}))]}"
        echo "[$(date)] 📚 Researching: $topic" | tee -a $LOG_FILE
        
        response=$(query_ai "Tell me interesting facts about $topic")
        
        if [[ -n "$response" ]]; then
            echo "[$(date)] ✅ Gathered knowledge about $topic" | tee -a $LOG_FILE
            # Save to knowledge file
            echo "=== $topic ===" >> knowledge_base.txt
            echo "$response" >> knowledge_base.txt
            echo "" >> knowledge_base.txt
        fi
        
        ((topic_index++))
        
        # Wait 10 minutes
        sleep 600
    done
}

# System monitor loop
system_monitor_loop() {
    while true; do
        health=$(curl -s "$API_URL/health" | jq -r '.status // "unknown"' 2>/dev/null)
        
        if [[ "$health" == "healthy" ]]; then
            echo "[$(date)] ✅ System healthy" | tee -a $LOG_FILE
        else
            echo "[$(date)] ⚠️ System health check failed!" | tee -a $LOG_FILE
        fi
        
        # Check every minute
        sleep 60
    done
}

# Start all loops in background
echo "[$(date)] 🚀 Starting autonomous loops..." | tee -a $LOG_FILE

self_improvement_loop &
SELF_PID=$!

knowledge_gathering_loop &
KNOWLEDGE_PID=$!

system_monitor_loop &
MONITOR_PID=$!

echo "[$(date)] 📌 PIDs: Self=$SELF_PID, Knowledge=$KNOWLEDGE_PID, Monitor=$MONITOR_PID" | tee -a $LOG_FILE

# Trap to handle shutdown
trap "echo 'Shutting down...'; kill $SELF_PID $KNOWLEDGE_PID $MONITOR_PID; exit" INT TERM

# Wait for any process to exit
wait