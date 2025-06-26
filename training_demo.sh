#!/bin/bash

# Think AI Training Demonstration Script
# Shows the capabilities after comprehensive training

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${PURPLE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${PURPLE}     Think AI - Comprehensive Training Demonstration${NC}"
echo -e "${PURPLE}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Function to demonstrate a capability
demo_capability() {
    local category=$1
    local question=$2
    local description=$3
    
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}🎯 $category${NC}"
    echo -e "${BLUE}$description${NC}"
    echo ""
    echo -e "${GREEN}Q: $question${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

# Introduction
echo -e "${BLUE}Welcome to the Think AI training demonstration!${NC}"
echo -e "${BLUE}This showcases the AI's capabilities after comprehensive training.${NC}"
echo ""
echo -e "${GREEN}The AI has been trained with:${NC}"
echo -e "  ✓ 1,000 iterations for tool capabilities"
echo -e "  ✓ 1,000 iterations for conversational abilities"
echo -e "  ✓ Self-improvement optimization"
echo ""
echo -e "${YELLOW}Let's see what it can do!${NC}"
echo ""

# Tool Capabilities Demonstrations
echo -e "${PURPLE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║              📧 Tool Capabilities Demo                     ║${NC}"
echo -e "${PURPLE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

demo_capability \
    "Debugging Assistance" \
    "My Rust program has a memory leak. How can I debug it?" \
    "Testing debugging and troubleshooting capabilities"

demo_capability \
    "Implementation Guidance" \
    "How do I implement a hash table with O(1) lookup in Rust?" \
    "Testing code implementation and best practices knowledge"

demo_capability \
    "Performance Optimization" \
    "How can I optimize my database queries for O(1) performance?" \
    "Testing optimization and performance tuning abilities"

demo_capability \
    "Learning Path" \
    "What's the best way to learn Rust programming from scratch?" \
    "Testing educational guidance and learning recommendations"

demo_capability \
    "Problem Solving" \
    "How should I design a distributed caching system?" \
    "Testing architectural and design problem-solving skills"

# Conversational Capabilities Demonstrations
echo -e "${PURPLE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║           💬 Conversational Abilities Demo                 ║${NC}"
echo -e "${PURPLE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

demo_capability \
    "Natural Greeting" \
    "Hi! I'm working on a project and could use some help." \
    "Testing natural conversation initiation"

demo_capability \
    "Context Awareness" \
    "Following up on that, what specific tools would you recommend?" \
    "Testing ability to maintain conversation context"

demo_capability \
    "Empathetic Response" \
    "I've been struggling with this bug for hours and I'm frustrated." \
    "Testing supportive and understanding responses"

demo_capability \
    "Progressive Disclosure" \
    "Can you explain recursion? I'm a beginner." \
    "Testing ability to adapt explanations to user level"

# Interactive Demo Option
echo -e "${PURPLE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║              🚀 Try It Yourself!                           ║${NC}"
echo -e "${PURPLE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}Ready to interact with the trained AI?${NC}"
echo ""
echo -e "${BLUE}Run: ${YELLOW}./target/release/think-ai chat${NC}"
echo ""
echo -e "${CYAN}Example questions to try:${NC}"
echo -e "  • ${GREEN}How do I implement a binary search tree?${NC}"
echo -e "  • ${GREEN}What's the difference between async and sync?${NC}"
echo -e "  • ${GREEN}Can you help me debug a race condition?${NC}"
echo -e "  • ${GREEN}Explain machine learning in simple terms${NC}"
echo -e "  • ${GREEN}What are the best practices for API design?${NC}"
echo ""
echo -e "${CYAN}Example conversations to start:${NC}"
echo -e "  • ${GREEN}Hi! I'm new to programming and want to learn${NC}"
echo -e "  • ${GREEN}I'm building a web app and need architecture advice${NC}"
echo -e "  • ${GREEN}Can you help me understand why my code isn't working?${NC}"
echo ""

# Training Statistics
if [ -f "knowledge_data/comprehensive_knowledge.json" ]; then
    SIZE=$(du -h knowledge_data/comprehensive_knowledge.json | cut -f1)
    echo -e "${PURPLE}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║              📊 Training Statistics                        ║${NC}"
    echo -e "${PURPLE}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BLUE}Knowledge Base Size: ${YELLOW}$SIZE${NC}"
    echo -e "${BLUE}Location: ${YELLOW}knowledge_data/comprehensive_knowledge.json${NC}"
fi

echo ""
echo -e "${GREEN}✨ The AI is now ready to provide intelligent, helpful assistance!${NC}"
echo ""