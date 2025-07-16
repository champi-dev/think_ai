#!/bin/bash

# Real-time GPU Performance Monitor for Think AI
# Provides live metrics and alerts for GPU utilization

set -euo pipefail

# Configuration
ALERT_GPU_UTIL_THRESHOLD=90
ALERT_MEM_UTIL_THRESHOLD=85
ALERT_TEMP_THRESHOLD=85
LOG_DIR="/var/log/think-ai/gpu"
WEBHOOK_URL="${THINK_AI_ALERT_WEBHOOK:-}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Create log directory
mkdir -p "$LOG_DIR"

# Send alert if webhook is configured
send_alert() {
    local message="$1"
    if [[ -n "$WEBHOOK_URL" ]]; then
        curl -s -X POST "$WEBHOOK_URL" \
            -H 'Content-Type: application/json' \
            -d "{\"text\": \"GPU Alert: $message\"}" || true
    fi
}

# Format bytes to human readable
format_bytes() {
    local bytes=$1
    if (( bytes < 1024 )); then
        echo "${bytes}B"
    elif (( bytes < 1048576 )); then
        echo "$(( bytes / 1024 ))KB"
    elif (( bytes < 1073741824 )); then
        echo "$(( bytes / 1048576 ))MB"
    else
        echo "$(( bytes / 1073741824 ))GB"
    fi
}

# Get current GPU metrics
get_gpu_metrics() {
    nvidia-smi --query-gpu=index,name,utilization.gpu,utilization.memory,memory.total,memory.used,memory.free,temperature.gpu,power.draw,clocks.current.graphics,clocks.current.memory --format=csv,noheader,nounits
}

# Monitor Think AI process GPU usage
monitor_think_ai_gpu() {
    local pids=$(pgrep -f "think-ai" || true)
    if [[ -n "$pids" ]]; then
        echo -e "\n${BLUE}Think AI Process GPU Usage:${NC}"
        for pid in $pids; do
            local cmd=$(ps -p "$pid" -o comm= 2>/dev/null || echo "unknown")
            echo -e "  PID $pid ($cmd):"
            
            # Get GPU memory usage for process
            local gpu_mem=$(nvidia-smi --query-compute-apps=pid,used_memory --format=csv,noheader,nounits | grep "^$pid" | cut -d',' -f2 || echo "0")
            if [[ -n "$gpu_mem" && "$gpu_mem" != "0" ]]; then
                echo -e "    GPU Memory: $(format_bytes $((gpu_mem * 1024 * 1024)))"
            else
                echo -e "    GPU Memory: Not using GPU"
            fi
        done
    fi
}

# Display header
display_header() {
    clear
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}           Think AI GPU Performance Monitor${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "Time: $(date '+%Y-%m-%d %H:%M:%S')\n"
}

# Display metrics with color coding
display_metrics() {
    local line="$1"
    IFS=',' read -r idx name gpu_util mem_util mem_total mem_used mem_free temp power clk_gpu clk_mem <<< "$line"
    
    # Color code based on thresholds
    local gpu_color=$GREEN
    local mem_color=$GREEN
    local temp_color=$GREEN
    
    if (( $(echo "$gpu_util > $ALERT_GPU_UTIL_THRESHOLD" | bc -l) )); then
        gpu_color=$RED
        send_alert "GPU $idx utilization high: ${gpu_util}%"
    elif (( $(echo "$gpu_util > 70" | bc -l) )); then
        gpu_color=$YELLOW
    fi
    
    if (( $(echo "$mem_util > $ALERT_MEM_UTIL_THRESHOLD" | bc -l) )); then
        mem_color=$RED
        send_alert "GPU $idx memory utilization high: ${mem_util}%"
    elif (( $(echo "$mem_util > 70" | bc -l) )); then
        mem_color=$YELLOW
    fi
    
    if (( $(echo "$temp > $ALERT_TEMP_THRESHOLD" | bc -l) )); then
        temp_color=$RED
        send_alert "GPU $idx temperature high: ${temp}°C"
    elif (( $(echo "$temp > 75" | bc -l) )); then
        temp_color=$YELLOW
    fi
    
    # Display GPU info
    echo -e "${BLUE}GPU $idx: $name${NC}"
    echo -e "├─ Utilization: ${gpu_color}${gpu_util}%${NC} GPU, ${mem_color}${mem_util}%${NC} Memory"
    echo -e "├─ Memory: $(format_bytes $((mem_used * 1024 * 1024))) / $(format_bytes $((mem_total * 1024 * 1024))) ($(format_bytes $((mem_free * 1024 * 1024))) free)"
    echo -e "├─ Temperature: ${temp_color}${temp}°C${NC}"
    echo -e "├─ Power Draw: ${power}W"
    echo -e "└─ Clocks: ${clk_gpu}MHz GPU, ${clk_mem}MHz Memory\n"
}

# Log metrics to file
log_metrics() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local metrics="$1"
    local log_file="$LOG_DIR/gpu-metrics-$(date '+%Y%m%d').csv"
    
    # Create header if file doesn't exist
    if [[ ! -f "$log_file" ]]; then
        echo "timestamp,gpu_index,gpu_name,gpu_utilization,memory_utilization,memory_total_mb,memory_used_mb,memory_free_mb,temperature,power_draw,gpu_clock_mhz,memory_clock_mhz" > "$log_file"
    fi
    
    # Append metrics
    while IFS= read -r line; do
        echo "$timestamp,$line" >> "$log_file"
    done <<< "$metrics"
}

# Performance analysis
analyze_performance() {
    local log_file="$LOG_DIR/gpu-metrics-$(date '+%Y%m%d').csv"
    if [[ -f "$log_file" && $(wc -l < "$log_file") -gt 10 ]]; then
        echo -e "${BLUE}Performance Analysis (Last Hour):${NC}"
        
        # Calculate averages using awk
        tail -n 60 "$log_file" 2>/dev/null | awk -F',' '
        NR>1 {
            gpu_sum += $4
            mem_sum += $5
            temp_sum += $9
            power_sum += $10
            count++
        }
        END {
            if (count > 0) {
                printf "├─ Average GPU Utilization: %.1f%%\n", gpu_sum/count
                printf "├─ Average Memory Utilization: %.1f%%\n", mem_sum/count
                printf "├─ Average Temperature: %.1f°C\n", temp_sum/count
                printf "└─ Average Power Draw: %.1fW\n", power_sum/count
            }
        }'
        echo
    fi
}

# Main monitoring loop
main() {
    # Check if nvidia-smi is available
    if ! command -v nvidia-smi &> /dev/null; then
        echo -e "${RED}Error: nvidia-smi not found. Please install NVIDIA drivers.${NC}"
        exit 1
    fi
    
    # Trap to handle clean exit
    trap 'echo -e "\n${GREEN}GPU monitoring stopped${NC}"; exit 0' SIGINT SIGTERM
    
    echo -e "${GREEN}Starting GPU performance monitoring...${NC}"
    echo -e "Press Ctrl+C to stop\n"
    
    # Main loop
    while true; do
        display_header
        
        # Get and display metrics
        metrics=$(get_gpu_metrics)
        while IFS= read -r line; do
            display_metrics "$line"
        done <<< "$metrics"
        
        # Monitor Think AI processes
        monitor_think_ai_gpu
        
        # Show performance analysis
        analyze_performance
        
        # Log metrics
        log_metrics "$metrics"
        
        # Update interval
        sleep 2
    done
}

# Run if called directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi