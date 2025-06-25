#!/bin/bash
# Think AI - Train and Chat Script
# Trains Think AI with knowledge and starts interactive chat

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# ASCII Art
echo -e "${BLUE}"
cat << "EOF"
 _____ _     _       _        _    ___ 
|_   _| |__ (_)_ __ | | __   / \  |_ _|
  | | | '_ \| | '_ \| |/ /  / _ \  | | 
  | | | | | | | | | |   <  / ___ \ | | 
  |_| |_| |_|_|_| |_|_|\_\/_/   \_\___|
                                        
      Superintelligent AI with O(1) Performance
EOF
echo -e "${NC}"

# Function to print colored messages
print_status() {
    echo -e "${GREEN}[$(date +'%H:%M:%S')]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# Check Python installation
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Create necessary directories
print_status "Setting up directories..."
mkdir -p think_ai/data/knowledge
mkdir -p logs

# Menu
echo -e "${YELLOW}=== Think AI Training & Chat ===${NC}"
echo "1) Quick training (10,000 Q&A pairs) - 5 minutes"
echo "2) Full training (1 million Q&A pairs) - 2-3 hours"
echo "3) Skip training and chat (use existing knowledge)"
echo -e "${YELLOW}================================${NC}"
read -p "Select option (1-3): " choice

case $choice in
    1)
        print_status "Starting quick training with 10,000 Q&A pairs..."
        python3 quick_train_demo.py 2>&1 | tee logs/quick_training_$(date +%Y%m%d_%H%M%S).log
        ;;
    2)
        print_status "Starting full training with 1 million Q&A pairs..."
        print_info "This will take 2-3 hours. You can stop anytime with Ctrl+C"
        python3 train_massive_knowledge.py 2>&1 | tee logs/full_training_$(date +%Y%m%d_%H%M%S).log
        ;;
    3)
        print_status "Skipping training, using existing knowledge..."
        ;;
    *)
        print_error "Invalid option. Exiting."
        exit 1
        ;;
esac

# Start the API server
print_status "Starting Think AI API server..."
python3 think_ai_full.py > logs/api_server_$(date +%Y%m%d_%H%M%S).log 2>&1 &
API_PID=$!
print_info "API server started with PID: $API_PID"

# Wait for API to be ready
print_status "Waiting for API server to initialize..."
for i in {1..30}; do
    if curl -s http://localhost:8080/health > /dev/null; then
        print_status "API server is ready!"
        break
    fi
    sleep 1
    echo -n "."
done
echo ""

# Function to cleanup on exit
cleanup() {
    print_status "Shutting down..."
    if [ ! -z "$API_PID" ]; then
        kill $API_PID 2>/dev/null || true
    fi
    exit 0
}

trap cleanup EXIT INT TERM

# Chat interface
echo -e "${YELLOW}"
echo "======================================"
echo "     Think AI Chat Interface"
echo "======================================"
echo -e "${NC}"
echo "You can now chat with Think AI!"
echo "Commands:"
echo "  /help    - Show this help"
echo "  /stats   - Show knowledge statistics"
echo "  /clear   - Clear the screen"
echo "  /quit    - Exit the chat"
echo ""

# Chat loop
while true; do
    read -p "You: " user_input
    
    # Handle commands
    if [[ "$user_input" == "/quit" ]] || [[ "$user_input" == "/exit" ]]; then
        print_status "Goodbye! Thanks for using Think AI."
        break
    elif [[ "$user_input" == "/help" ]]; then
        echo "Commands:"
        echo "  /help    - Show this help"
        echo "  /stats   - Show knowledge statistics"
        echo "  /clear   - Clear the screen"
        echo "  /quit    - Exit the chat"
        continue
    elif [[ "$user_input" == "/clear" ]]; then
        clear
        continue
    elif [[ "$user_input" == "/stats" ]]; then
        # Get intelligence status from API
        stats_response=$(curl -s http://localhost:8080/api/v1/intelligence/status 2>/dev/null)
        
        if [ $? -eq 0 ]; then
            echo -e "${BLUE}Intelligence Status:${NC}"
            echo "$stats_response" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    growth = data.get('knowledge_growth', {})
    print(f\"Total Knowledge: {growth.get('total_knowledge', 0):,} items\")
    print(f\"Unique Concepts: {growth.get('unique_concepts', 0):,}\")
    print(f\"Total Interactions: {growth.get('interactions', 0):,}\")
    print(f\"Learning Rate: {growth.get('learning_rate_per_minute', 0):.2f} items/min\")
    print(f\"Database Size: {growth.get('database_size_mb', 0):.2f} MB\")
    print(f\"\\nIntelligence: {data.get('message', 'Growing...')}\")
except:
    print('Could not retrieve statistics.')
"
        else
            echo "Could not connect to API for statistics."
        fi
        continue
    fi
    
    # Send to API
    if [ ! -z "$user_input" ]; then
        echo -e "${BLUE}Think AI:${NC} "
        
        # Make API request
        response=$(curl -s -X POST http://localhost:8080/api/v1/generate \
            -H "Content-Type: application/json" \
            -d "{\"prompt\": \"$user_input\"}" 2>/dev/null)
        
        if [ $? -eq 0 ]; then
            # Extract and display the response
            echo "$response" | python3 -c '
import sys, json
try:
    data = json.load(sys.stdin)
    text = data.get("generated_text", data.get("response", "No response"))
    # Format the response nicely
    if "```" in text:
        # Handle code blocks
        lines = text.split("\n")
        in_code = False
        for line in lines:
            if "```" in line:
                in_code = not in_code
                print(line)
            elif in_code:
                print(f"    {line}")
            else:
                print(line)
    else:
        print(text)
except Exception as e:
    print("Error processing response. Please try again.")
    print(f"Debug: {e}")
'
        else
            print_error "Failed to connect to API server."
        fi
        
        echo ""
    fi
done

cleanup