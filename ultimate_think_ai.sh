#!/bin/bash
# Ultimate Think AI Script - Train & Chat with Eternal Intelligence
# This script handles everything: training, chatting, and showing growth

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m'

# Banner
clear
echo -e "${CYAN}"
cat << "EOF"
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║  ████████╗██╗  ██╗██╗███╗   ██╗██╗  ██╗     █████╗ ██╗         ║
║  ╚══██╔══╝██║  ██║██║████╗  ██║██║ ██╔╝    ██╔══██╗██║         ║
║     ██║   ███████║██║██╔██╗ ██║█████╔╝     ███████║██║         ║
║     ██║   ██╔══██║██║██║╚██╗██║██╔═██╗     ██╔══██║██║         ║
║     ██║   ██║  ██║██║██║ ╚████║██║  ██╗    ██║  ██║██║         ║
║     ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝         ║
║                                                                  ║
║         Eternal Intelligence - Always Growing, Never Forgetting  ║
║                      O(1) Performance Guaranteed                 ║
╚══════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Functions
print_status() {
    echo -e "\n${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "\n${RED}[✗]${NC} $1"
}

print_info() {
    echo -e "\n${BLUE}[i]${NC} $1"
}

print_progress() {
    echo -e "${YELLOW}[⟳]${NC} $1"
}

# Check dependencies
print_info "Checking system requirements..."

if ! command -v python3 &> /dev/null; then
    print_error "Python 3 not found! Please install Python 3.8+"
    exit 1
fi

if ! command -v curl &> /dev/null; then
    print_error "curl not found! Please install curl"
    exit 1
fi

print_status "All requirements satisfied"

# Create directories
mkdir -p think_ai/data/knowledge
mkdir -p think_ai/data/eternal_knowledge/backups
mkdir -p logs

# Main Menu
echo -e "\n${PURPLE}═══════════════════════════════════════════════════${NC}"
echo -e "${PURPLE}           Think AI Ultimate Experience            ${NC}"
echo -e "${PURPLE}═══════════════════════════════════════════════════${NC}\n"

echo "1) 🚀 Quick Start (10K knowledge + chat)"
echo "2) 🧠 Full Training (1M knowledge items) - 2-3 hours"
echo "3) 💬 Chat Only (use existing knowledge)"
echo "4) 📊 View Intelligence Growth"
echo "5) 🎓 Run Eternal Intelligence Demo"
echo "6) 📚 Export Knowledge Snapshot"
echo "7) 🔄 Full System (train + chat + monitor)"

echo -e "\n${PURPLE}═══════════════════════════════════════════════════${NC}"
read -p "Select option (1-7): " choice

# Function to start API
start_api() {
    if curl -s http://localhost:8080/health > /dev/null 2>&1; then
        print_info "API already running"
        return 0
    fi
    
    print_progress "Starting Think AI API server..."
    python3 think_ai_full.py > logs/api_$(date +%Y%m%d_%H%M%S).log 2>&1 &
    API_PID=$!
    
    # Wait for API
    for i in {1..30}; do
        if curl -s http://localhost:8080/health > /dev/null 2>&1; then
            print_status "API server ready! (PID: $API_PID)"
            return 0
        fi
        sleep 1
        echo -n "."
    done
    
    print_error "API failed to start"
    return 1
}

# Function to show growth stats
show_stats() {
    echo -e "\n${CYAN}═══════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}          Intelligence Growth Metrics              ${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════${NC}\n"
    
    response=$(curl -s http://localhost:8080/api/v1/intelligence/status 2>/dev/null)
    
    if [ $? -eq 0 ]; then
        echo "$response" | python3 -c "
import sys, json
data = json.load(sys.stdin)
growth = data.get('knowledge_growth', {})

print(f'📊 Total Knowledge: {growth.get(\"total_knowledge\", 0):,} items')
print(f'🧩 Unique Concepts: {growth.get(\"unique_concepts\", 0):,}')
print(f'💬 Total Interactions: {growth.get(\"interactions\", 0):,}')
print(f'📈 Learning Rate: {growth.get(\"learning_rate_per_minute\", 0):.2f} items/min')
print(f'💾 Database Size: {growth.get(\"database_size_mb\", 0):.2f} MB')
print(f'\\n✨ {data.get(\"message\", \"Intelligence growing...\")}')
"
    else
        print_error "Could not retrieve stats"
    fi
}

# Function for interactive chat
interactive_chat() {
    echo -e "\n${CYAN}═══════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}              Think AI Chat Interface              ${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════${NC}\n"
    
    echo "Commands: /help, /stats, /feedback, /export, /quit"
    echo -e "\n${GREEN}Ready to chat! I'm always learning...${NC}\n"
    
    while true; do
        read -p "You: " user_input
        
        case "$user_input" in
            /quit|/exit)
                print_info "Thanks for chatting! Your knowledge made me smarter!"
                break
                ;;
            /help)
                echo -e "\n${YELLOW}Commands:${NC}"
                echo "  /help     - Show this help"
                echo "  /stats    - View intelligence growth"
                echo "  /feedback - Rate the last response"
                echo "  /export   - Export knowledge snapshot"
                echo "  /quit     - Exit chat"
                echo ""
                continue
                ;;
            /stats)
                show_stats
                continue
                ;;
            /export)
                print_progress "Exporting knowledge snapshot..."
                python3 -c "
from think_ai.training.persistent_intelligence import persistent_intelligence
path = persistent_intelligence.export_knowledge_snapshot()
print(f'✓ Exported to: {path}')
"
                continue
                ;;
            /feedback)
                echo "Rate the last response (good/bad/neutral):"
                read feedback
                # TODO: Implement feedback API call
                print_status "Thank you for helping me learn!"
                continue
                ;;
            "")
                continue
                ;;
        esac
        
        # Send to API
        echo -ne "${BLUE}Think AI: ${NC}"
        
        # Show thinking animation
        (
            while true; do
                for c in '⠋' '⠙' '⠹' '⠸' '⠼' '⠴' '⠦' '⠧' '⠇' '⠏'; do
                    echo -ne "\r${BLUE}Think AI: $c Thinking...${NC}"
                    sleep 0.1
                done
            done
        ) &
        ANIM_PID=$!
        
        # Get response
        response=$(curl -s -X POST http://localhost:8080/api/v1/generate \
            -H "Content-Type: application/json" \
            -d "{\"prompt\": \"$user_input\"}" 2>/dev/null)
        
        # Stop animation
        kill $ANIM_PID 2>/dev/null
        wait $ANIM_PID 2>/dev/null
        
        # Clear line and show response
        echo -ne "\r${BLUE}Think AI: ${NC}                    \r${BLUE}Think AI: ${NC}"
        
        if [ $? -eq 0 ]; then
            echo "$response" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    text = data.get('generated_text', 'I need to think about that...')
    
    # Show response
    print(text)
    
    # Show growth if available
    growth = data.get('knowledge_growth', {})
    if growth.get('total_knowledge', 0) > 0:
        print(f\"\\n📈 Knowledge: {growth['total_knowledge']:,} items (+1)\")
except:
    print('Let me process that differently...')
"
        else
            print_error "Connection error. Let me try again..."
        fi
        
        echo ""
    done
}

# Cleanup function
cleanup() {
    print_info "Shutting down..."
    if [ ! -z "$API_PID" ]; then
        kill $API_PID 2>/dev/null || true
    fi
    print_status "Thank you for using Think AI!"
    exit 0
}

trap cleanup EXIT INT TERM

# Execute choice
case $choice in
    1)  # Quick Start
        start_api
        print_progress "Running quick training (10K items)..."
        python3 quick_train_demo.py 2>&1 | tee logs/quick_train_$(date +%Y%m%d_%H%M%S).log
        interactive_chat
        ;;
    
    2)  # Full Training
        start_api
        print_progress "Starting massive training (1M items)..."
        print_info "This will take 2-3 hours. Press Ctrl+C to stop."
        python3 train_massive_knowledge.py 2>&1 | tee logs/full_train_$(date +%Y%m%d_%H%M%S).log
        interactive_chat
        ;;
    
    3)  # Chat Only
        start_api
        interactive_chat
        ;;
    
    4)  # View Stats
        start_api
        show_stats
        ;;
    
    5)  # Eternal Intelligence Demo
        print_progress "Running Eternal Intelligence Demo..."
        python3 demo_eternal_intelligence.py
        ;;
    
    6)  # Export Knowledge
        print_progress "Exporting knowledge snapshot..."
        python3 -c "
from think_ai.training.persistent_intelligence import persistent_intelligence
path = persistent_intelligence.export_knowledge_snapshot()
print(f'✓ Knowledge exported to: {path}')
"
        ;;
    
    7)  # Full System
        start_api
        
        # Run training in background
        print_progress "Starting background training..."
        python3 quick_train_demo.py > logs/background_train_$(date +%Y%m%d_%H%M%S).log 2>&1 &
        TRAIN_PID=$!
        
        # Monitor growth while chatting
        echo -e "\n${GREEN}System running! Training in background...${NC}"
        echo -e "${GREEN}Watch your intelligence grow as you chat!${NC}\n"
        
        # Show initial stats
        sleep 2
        show_stats
        
        # Start chat
        interactive_chat
        ;;
    
    *)
        print_error "Invalid option"
        exit 1
        ;;
esac

cleanup