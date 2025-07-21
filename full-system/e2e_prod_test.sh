#!/bin/bash

# ThinkAI Production E2E Test Suite
# Tests all endpoints and monitors for memory leaks

set -e

PROD_URL="https://thinkai.lat"
TEST_DURATION=30  # Run tests for 30 seconds to detect memory leaks
CONCURRENT_REQUESTS=5
LOG_FILE="e2e_test_$(date +%Y%m%d_%H%M%S).log"

echo "🚀 Starting ThinkAI Production E2E Test Suite"
echo "📝 Logging to: $LOG_FILE"
echo "🌐 Testing: $PROD_URL"
echo "⏱️  Duration: ${TEST_DURATION}s with $CONCURRENT_REQUESTS concurrent requests"
echo ""

# Function to log with timestamp
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Function to make a request and measure response time
make_request() {
    local endpoint=$1
    local method=$2
    local data=$3
    local headers=$4
    
    local start_time=$(date +%s.%N)
    local response=$(curl -s -w "\n%{http_code}" -X "$method" \
        -H "Content-Type: application/json" \
        -H "X-Session-ID: e2e-test-$(date +%s)" \
        $headers \
        ${data:+-d "$data"} \
        "$PROD_URL$endpoint" 2>&1)
    local end_time=$(date +%s.%N)
    
    local status_code=$(echo "$response" | tail -n1)
    local response_time=$(echo "$end_time - $start_time" | bc)
    
    echo "$status_code|$response_time"
}

# Health check
log "🏥 Running health check..."
health_response=$(curl -s -w "\n%{http_code}" "$PROD_URL/health")
health_status=$(echo "$health_response" | tail -n1)
if [ "$health_status" = "200" ]; then
    log "✅ Health check passed"
else
    log "❌ Health check failed with status: $health_status"
    exit 1
fi

# Get initial metrics for memory baseline
log "📊 Getting initial metrics baseline..."
initial_metrics=$(curl -s "$PROD_URL/api/metrics")
initial_memory=$(echo "$initial_metrics" | jq -r '.system_metrics.memory_usage // 0' 2>/dev/null || echo "0")
log "Initial memory usage: ${initial_memory}%"

# Test counters
total_requests=0
successful_requests=0
failed_requests=0
declare -A endpoint_times

# Function to run continuous load test
run_load_test() {
    local test_id=$1
    local end_time=$(($(date +%s) + TEST_DURATION))
    
    while [ $(date +%s) -lt $end_time ]; do
        # Test different endpoints randomly
        case $((RANDOM % 6)) in
            0)
                # Test chat endpoint
                result=$(make_request "/api/chat" "POST" '{"message":"E2E test message '$(date +%s)'"}' "")
                endpoint="/api/chat"
                ;;
            1)
                # Test sessions list
                result=$(make_request "/api/chat/sessions" "GET" "" "")
                endpoint="/api/chat/sessions"
                ;;
            2)
                # Test audio transcribe (will fail but generates metrics)
                result=$(make_request "/api/audio/transcribe" "POST" "test audio data" "-H 'Content-Type: audio/wav'")
                endpoint="/api/audio/transcribe"
                ;;
            3)
                # Test audio synthesis
                result=$(make_request "/api/audio/synthesize" "POST" '{"text":"E2E test speech"}' "")
                endpoint="/api/audio/synthesize"
                ;;
            4)
                # Test metrics endpoint
                result=$(make_request "/api/metrics" "GET" "" "")
                endpoint="/api/metrics"
                ;;
            5)
                # Test WhatsApp webhook
                result=$(make_request "/webhooks/whatsapp" "POST" "Body=E2E+test&From=whatsapp%3A%2B1234567890&To=whatsapp%3A%2B0987654321&MessageSid=test$(date +%s)" "-H 'Content-Type: application/x-www-form-urlencoded'")
                endpoint="/webhooks/whatsapp"
                ;;
        esac
        
        status_code=$(echo "$result" | cut -d'|' -f1)
        response_time=$(echo "$result" | cut -d'|' -f2)
        
        ((total_requests++))
        
        if [[ "$status_code" =~ ^[23][0-9][0-9]$ ]]; then
            ((successful_requests++))
            endpoint_times["$endpoint"]+="$response_time "
        else
            ((failed_requests++))
            log "⚠️  Request failed: $endpoint - Status: $status_code"
        fi
        
        # Small delay between requests
        sleep 0.1
    done
}

# Start load test with multiple concurrent workers
log "🔥 Starting load test with $CONCURRENT_REQUESTS concurrent workers..."
for i in $(seq 1 $CONCURRENT_REQUESTS); do
    run_load_test $i &
done

# Monitor memory usage during test
monitor_memory() {
    local check_interval=10
    local checks=$((TEST_DURATION / check_interval))
    local max_memory=0
    
    for i in $(seq 1 $checks); do
        sleep $check_interval
        metrics=$(curl -s "$PROD_URL/api/metrics" 2>/dev/null || echo "{}")
        current_memory=$(echo "$metrics" | jq -r '.system_metrics.memory_usage // 0' 2>/dev/null || echo "0")
        
        if (( $(echo "$current_memory > $max_memory" | bc -l) )); then
            max_memory=$current_memory
        fi
        
        log "Memory check $i/$checks: ${current_memory}% (max: ${max_memory}%)"
    done
    
    echo "$max_memory"
}

max_memory=$(monitor_memory) &
memory_monitor_pid=$!

# Wait for all load test workers to complete
wait $(jobs -p | grep -v $memory_monitor_pid)
wait $memory_monitor_pid

# Get final metrics
log "📊 Getting final metrics..."
final_metrics=$(curl -s "$PROD_URL/api/metrics")
final_memory=$(echo "$final_metrics" | jq -r '.system_metrics.memory_usage // 0' 2>/dev/null || echo "0")

# Calculate memory increase
memory_increase=$(echo "$final_memory - $initial_memory" | bc)

# Generate report
log ""
log "📋 E2E Test Report"
log "=================="
log "Total requests: $total_requests"
log "Successful: $successful_requests ($(echo "scale=2; $successful_requests * 100 / $total_requests" | bc)%)"
log "Failed: $failed_requests"
log ""
log "Memory Analysis:"
log "- Initial: ${initial_memory}%"
log "- Final: ${final_memory}%"
log "- Increase: ${memory_increase}%"
log "- Peak: ${max_memory}%"

# Check for memory leak
if (( $(echo "$memory_increase > 10" | bc -l) )); then
    log "⚠️  WARNING: Significant memory increase detected! Possible memory leak."
else
    log "✅ Memory usage stable - no leak detected"
fi

# Calculate average response times per endpoint
log ""
log "Average Response Times:"
for endpoint in "${!endpoint_times[@]}"; do
    times=(${endpoint_times[$endpoint]})
    sum=0
    for time in "${times[@]}"; do
        sum=$(echo "$sum + $time" | bc)
    done
    avg=$(echo "scale=3; $sum / ${#times[@]}" | bc)
    log "- $endpoint: ${avg}s (${#times[@]} requests)"
done

# Test dashboard accessibility
log ""
log "🎨 Testing dashboard..."
dashboard_status=$(curl -s -o /dev/null -w "%{http_code}" "$PROD_URL/stats")
if [ "$dashboard_status" = "200" ]; then
    log "✅ Dashboard accessible at $PROD_URL/stats"
else
    log "❌ Dashboard returned status: $dashboard_status"
fi

# Screenshot test preparation
log ""
log "📸 Screenshot Test Instructions:"
log "1. Open $PROD_URL/stats in your browser"
log "2. Take a screenshot of the metrics dashboard"
log "3. Look for:"
log "   - CPU and memory usage graphs"
log "   - Request volume chart showing ~$total_requests requests"
log "   - Response time trends"
log "   - Endpoint performance table"
log "   - Any errors in the error log"
log ""
log "🎯 Test completed! Check $LOG_FILE for full details."

# Return exit code based on test results
if [ "$failed_requests" -gt $((total_requests / 10)) ]; then
    log "❌ Too many failed requests (>10%)"
    exit 1
elif (( $(echo "$memory_increase > 20" | bc -l) )); then
    log "❌ Memory leak detected"
    exit 1
else
    log "✅ All tests passed!"
    exit 0
fi