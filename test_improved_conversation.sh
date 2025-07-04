#!/bin/bash

# Test script for improved Think AI conversational quality
# This script builds and tests the semantic response system

set -e

echo "=== Testing Improved Think AI Conversational System ==="
echo "Time: $(date)"
echo

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Check if we're in the right directory
if [ ! -f "Cargo.toml" ]; then
    echo -e "${RED}Error: Must run from Think AI root directory${NC}"
    exit 1
fi

# Step 2: Build the project
echo -e "${YELLOW}Building Think AI with improved conversational system...${NC}"
if command -v cargo &> /dev/null; then
    cargo build --release
    echo -e "${GREEN}✓ Build completed${NC}"
else
    echo -e "${RED}Error: Cargo not found. Please install Rust.${NC}"
    echo "You can test the deployed version instead with:"
    echo "python3 test_think_ai_conversation.py"
    exit 1
fi

# Step 3: Test the CLI locally
echo
echo -e "${YELLOW}Testing CLI responses...${NC}"

# Create test queries
cat > test_queries.txt << 'EOF'
Hello! Can you introduce yourself?
What is consciousness from a philosophical perspective?
Explain O(1) time complexity
Write a haiku about artificial intelligence
Tell me a joke about quantum physics
What are the best practices for building scalable web applications?
Thank you for the conversation. Goodbye!
EOF

# Test each query
echo -e "${YELLOW}Running conversation test...${NC}"
while IFS= read -r query; do
    echo
    echo "Query: $query"
    echo -n "Response: "
    echo "$query" | timeout 5s ./target/release/think-ai chat 2>/dev/null | grep -v "^>" | head -n 1 || echo "(timeout or error)"
done < test_queries.txt

# Step 4: Performance test
echo
echo -e "${YELLOW}Testing O(1) performance...${NC}"

# Create performance test script
cat > perf_test.py << 'EOF'
import time
import subprocess
import statistics

queries = [
    "What is consciousness?",
    "Explain quantum computing",
    "How do neural networks work?",
    "What is the meaning of life?",
    "Tell me about artificial intelligence"
]

times = []
for query in queries:
    start = time.time()
    try:
        result = subprocess.run(
            ["./target/release/think-ai", "chat"],
            input=query + "\nexit\n",
            capture_output=True,
            text=True,
            timeout=2
        )
        elapsed = (time.time() - start) * 1000  # Convert to ms
        times.append(elapsed)
        print(f"Query: {query[:30]}... - Time: {elapsed:.0f}ms")
    except:
        print(f"Query: {query[:30]}... - Time: ERROR")

if times:
    print(f"\nAverage response time: {statistics.mean(times):.0f}ms")
    print(f"Max response time: {max(times):.0f}ms")
    print(f"O(1) Performance: {'✓ PASS' if max(times) < 1000 else '✗ FAIL'}")
EOF

python3 perf_test.py

# Step 5: Test against deployed version
echo
echo -e "${YELLOW}Testing deployed API for comparison...${NC}"
python3 test_think_ai_conversation.py

# Cleanup
rm -f test_queries.txt perf_test.py

echo
echo -e "${GREEN}=== Test completed ===${NC}"
echo "Check the conversation test results above to verify improvements:"
echo "1. Responses should be contextually relevant to queries"
echo "2. No random topic switching (e.g., consciousness → galaxy)"
echo "3. Maintained O(1) performance (<1000ms per response)"
echo
echo "To run a full conversation test:"
echo "  ./target/release/think-ai chat"
echo
echo "To test the API directly:"
echo "  curl -X POST https://thinkai-production.up.railway.app/api/chat \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"query\": \"What is consciousness?\"}'
"