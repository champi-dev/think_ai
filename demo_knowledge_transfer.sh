#!/bin/bash

# Interactive demo script for Think AI Knowledge Transfer System

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║    🧠 THINK AI KNOWLEDGE TRANSFER INTERACTIVE DEMO 🧠       ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║  This demo shows how Think AI learns from Claude's patterns  ║"
echo "║  through an innovative knowledge transfer system.             ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# Function to show section
show_section() {
    echo ""
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}$1${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# Check if binary exists
if [ ! -f "./target/release/think-ai" ]; then
    echo -e "${YELLOW}Building Think AI...${NC}"
    cargo build --release --bin think-ai || exit 1
fi

show_section "📋 SYSTEM OVERVIEW"
echo -e "${GREEN}The Knowledge Transfer System includes:${NC}"
echo ""
echo "1. ${BLUE}Knowledge Modules${NC} - 6 domains of expertise:"
echo "   • Programming & Software Engineering"
echo "   • Problem Solving & Critical Thinking"
echo "   • Communication & Teaching"
echo "   • Analysis & Research"
echo "   • Creative Problem Solving"
echo "   • Continuous Learning"
echo ""
echo "2. ${BLUE}Thinking Patterns${NC} - 5 cognitive frameworks:"
echo "   • Performance-First Thinking"
echo "   • Systematic Debugging"
echo "   • First Principles Analysis"
echo "   • Explain Like I'm Five (ELI5)"
echo "   • Meta-Cognitive Patterns"
echo ""
echo "3. ${BLUE}Q&A Training System${NC} - Adaptive learning with:"
echo "   • Progressive difficulty adjustment"
echo "   • Multi-dimensional evaluation"
echo "   • Real-time performance tracking"
echo ""
echo "4. ${BLUE}O(1) Knowledge Cache${NC} - Lightning-fast retrieval:"
echo "   • Hash-based instant lookups"
echo "   • Similarity search capability"
echo "   • Adaptive eviction policies"

show_section "🎯 DEMO OPTIONS"
echo "Choose a demo:"
echo ""
echo "1) ${GREEN}Quick Demo${NC} (10 iterations) - See the system in action"
echo "2) ${YELLOW}Standard Training${NC} (50 iterations) - Watch learning progress"
echo "3) ${MAGENTA}Extended Training${NC} (200 iterations) - See mastery develop"
echo "4) ${BLUE}View Previous Results${NC} - Examine training data"
echo "5) ${CYAN}Test Chat Interface${NC} - Chat with trained system"
echo ""
read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        show_section "🚀 RUNNING QUICK DEMO"
        echo "Training with 10 iterations..."
        ./target/release/think-ai train --iterations 10
        ;;
    2)
        show_section "📚 RUNNING STANDARD TRAINING"
        echo "Training with 50 iterations..."
        echo "Watch as the system learns across different domains!"
        ./target/release/think-ai train --iterations 50
        ;;
    3)
        show_section "🎓 RUNNING EXTENDED TRAINING"
        echo "Training with 200 iterations..."
        echo "This will show category mastery and advanced learning!"
        ./target/release/think-ai train --iterations 200
        ;;
    4)
        show_section "📁 VIEWING PREVIOUS RESULTS"
        echo "Recent training sessions:"
        ls -la training_session_*.json 2>/dev/null | tail -5
        echo ""
        echo "Select a session file to view (or press Enter to skip):"
        read session_file
        if [ -n "$session_file" ] && [ -f "$session_file" ]; then
            echo ""
            echo "Session Summary:"
            jq '{
                session_id,
                total_iterations,
                completed_iterations,
                start_time,
                end_time,
                final_metrics
            }' "$session_file" 2>/dev/null || cat "$session_file" | head -50
        fi
        ;;
    5)
        show_section "💬 TESTING CHAT INTERFACE"
        echo "Starting Think AI chat..."
        echo "Try asking questions to test the learned knowledge!"
        echo ""
        ./target/release/think-ai chat
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

show_section "📊 RESULTS ANALYSIS"
echo -e "${GREEN}Training complete!${NC}"
echo ""
echo "The system has generated:"
echo "• Training session data (performance metrics)"
echo "• Knowledge base (learned patterns)"
echo "• Knowledge cache (O(1) retrieval store)"
echo ""
echo -e "${YELLOW}💡 What to do next:${NC}"
echo "1. Run './target/release/think-ai chat' to test the system"
echo "2. Try different training durations to see learning curves"
echo "3. Examine the JSON files to understand the knowledge structure"
echo "4. Run full 1000-iteration training for production use"
echo ""
echo -e "${CYAN}Thank you for exploring Think AI's Knowledge Transfer System!${NC}"