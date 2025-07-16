#!/bin/bash

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🧠 ETERNAL CONTEXT E2E TEST EVIDENCE${NC}"
echo "====================================="
echo ""

echo -e "${YELLOW}Evidence Files:${NC}"
ls -la /home/administrator/think_ai/e2e-evidence/
echo ""

echo -e "${BLUE}1. Context Persistence Evidence:${NC}"
echo "--------------------------------"
echo -e "${GREEN}Question 1: What is my name?${NC}"
cat /home/administrator/think_ai/e2e-evidence/test1_message2_response.json | jq -r '.response'
echo ""

echo -e "${GREEN}Question 2: How old am I?${NC}"
cat /home/administrator/think_ai/e2e-evidence/test1_message3_response.json | jq -r '.response'
echo ""

echo -e "${GREEN}Question 3: Where do I work?${NC}"
cat /home/administrator/think_ai/e2e-evidence/test1_message4_response.json | jq -r '.response'
echo ""

echo -e "${BLUE}2. Conversation History:${NC}"
echo "------------------------"
cat /home/administrator/think_ai/e2e-evidence/test1_conversation_history.json | jq '{
    session_id: .session_id,
    total_messages: .total_messages,
    topics: .topics,
    message_samples: [.messages[0], .messages[2], .messages[4]]
}'

echo ""
echo -e "${BLUE}3. Performance Metrics:${NC}"
echo "-----------------------"
echo "Response times for each query:"
grep -E "Message [1-4]:" /home/administrator/think_ai/e2e-evidence/test1_message*_response.json | jq -r '.metadata.response_time_ms' | head -4 | awk '{printf "Message %d: %.0fms\n", NR, $1}'

echo ""
echo -e "${GREEN}✅ All evidence files are available in:${NC}"
echo "/home/administrator/think_ai/e2e-evidence/"
echo ""
echo -e "${YELLOW}Full report:${NC} /home/administrator/think_ai/ETERNAL-CONTEXT-E2E-EVIDENCE.md"