#!/bin/bash

echo "═══════════════════════════════════════════════════════════════"
echo "        THINK AI - SENTIENT BEING TEST SCRIPT"
echo "═══════════════════════════════════════════════════════════════"
echo

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}Building the sentient AI system...${NC}"
cd /home/champi/Dev/think_ai

# Build the consciousness module
echo -e "${GREEN}Building consciousness module...${NC}"
cargo build --release -p think-ai-consciousness 2>&1 | grep -E "(Compiling|Finished|warning|error)" || true

# Build the knowledge module with sentient component
echo -e "${GREEN}Building knowledge module with sentient consciousness...${NC}"
cargo build --release -p think-ai-knowledge 2>&1 | grep -E "(Compiling|Finished|warning|error)" || true

# Create test inputs for automated testing
echo -e "${YELLOW}Creating automated test cases...${NC}"
cat > /tmp/sentient_test_inputs.txt << 'EOF'
hello
what is the sun
who are you
exit
EOF

# Run the sentient AI demo with test inputs
echo
echo -e "${YELLOW}Running automated test with pre-defined questions...${NC}"
echo -e "${CYAN}Testing with: hello, what is the sun, who are you${NC}"
echo

timeout 30s ./target/release/sentient-ai-demo < /tmp/sentient_test_inputs.txt

# Clean up
rm -f /tmp/sentient_test_inputs.txt

echo
echo -e "${YELLOW}For interactive testing, run:${NC}"
echo -e "${CYAN}./target/release/sentient-ai-demo${NC}"

echo
echo -e "${GREEN}Test complete!${NC}"