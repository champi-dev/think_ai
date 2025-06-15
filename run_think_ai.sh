#!/bin/bash
# Universal Think AI Runner - Works on Mobile (Termux) and MacBook
# Detects environment and runs appropriately

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🧠 Think AI Universal Runner${NC}"
echo "=============================="

# Detect environment
detect_environment() {
    if [[ -d "/data/data/com.termux" ]]; then
        echo "mobile"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    else
        echo "unknown"
    fi
}

ENV=$(detect_environment)
echo -e "Detected environment: ${GREEN}$ENV${NC}"

# Function to check if running with root/sudo
check_root() {
    if [[ $EUID -eq 0 ]]; then
        return 0
    else
        return 1
    fi
}

# Function to install dependencies on MacOS
install_macos_deps() {
    echo -e "${YELLOW}Installing dependencies for macOS...${NC}"
    
    # Check for Homebrew
    if ! command -v brew &> /dev/null; then
        echo "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    
    # Install services
    brew install redis neo4j python@3.11
    
    # Start services
    brew services start redis
    brew services start neo4j
    
    echo -e "${GREEN}✅ macOS dependencies installed${NC}"
}

# Function to run on mobile (Termux)
run_mobile() {
    echo -e "${YELLOW}Running on Mobile (Termux)${NC}"
    echo ""
    
    # Check if VM is set up
    if [[ ! -f "vm-think-ai/alpine-disk.qcow2" ]]; then
        echo -e "${RED}VM not set up yet!${NC}"
        echo "Run: ./vm-think-ai/setup-alpine-vm.sh"
        exit 1
    fi
    
    # Check if Alpine is installed
    if [[ ! -f "vm-think-ai/.installed" ]]; then
        echo -e "${YELLOW}First time setup required:${NC}"
        echo "1. Run: ./vm-think-ai/run-alpine-vm.sh"
        echo "2. Follow QUICKSTART.md to install Alpine"
        echo "3. This script will then work automatically"
        
        # Create helper script for inside VM
        cat > vm-think-ai/install-in-vm.sh << 'EOF'
#!/bin/sh
# Run this inside the Alpine VM

echo "📦 Installing Think AI in VM..."

# Install dependencies
apk update
apk add python3 py3-pip git redis postgresql

# Start services
rc-service redis start
rc-update add redis default

# Clone and setup Think AI
cd /root
if [ ! -d "think_ai" ]; then
    # Copy from host or clone
    echo "Please copy Think AI code to /root/think_ai"
else
    cd think_ai
    pip install -r requirements.txt
    python run_full_system.py
fi
EOF
        chmod +x vm-think-ai/install-in-vm.sh
        
        echo ""
        echo "Helper script created: vm-think-ai/install-in-vm.sh"
        echo "Copy it to VM and run after Alpine setup"
    else
        echo -e "${GREEN}Starting VM with Think AI...${NC}"
        ./vm-think-ai/run-alpine-vm.sh
    fi
}

# Function to run on MacBook
run_macos() {
    echo -e "${YELLOW}Running on macOS${NC}"
    echo ""
    
    # Check for required services
    if ! pgrep -x "redis-server" > /dev/null; then
        echo "Redis not running. Starting..."
        if command -v brew &> /dev/null; then
            brew services start redis
        else
            install_macos_deps
        fi
    fi
    
    # Check Python environment
    if [[ ! -d "venv" ]]; then
        echo "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate venv and install deps
    source venv/bin/activate
    
    if [[ ! -f ".deps_installed" ]]; then
        echo "Installing Python dependencies..."
        pip install -r requirements.txt
        touch .deps_installed
    fi
    
    # Run the system
    echo -e "${GREEN}Starting Think AI Full System...${NC}"
    python run_full_system.py
}

# Function to run on Linux
run_linux() {
    echo -e "${YELLOW}Running on Linux${NC}"
    echo ""
    
    if check_root; then
        echo -e "${GREEN}Running with root access${NC}"
        
        # Install system dependencies if needed
        if ! command -v redis-server &> /dev/null; then
            echo "Installing Redis..."
            apt-get update && apt-get install -y redis-server
            systemctl start redis
        fi
        
        # Run the system
        python3 run_full_system.py
    else
        echo -e "${YELLOW}No root access. Using mock services...${NC}"
        python3 run_full_system.py
    fi
}

# Main execution
case $ENV in
    mobile)
        run_mobile
        ;;
    macos)
        run_macos
        ;;
    linux)
        run_linux
        ;;
    *)
        echo -e "${RED}Unknown environment!${NC}"
        echo "You can still run manually:"
        echo "  python3 run_full_system.py"
        exit 1
        ;;
esac