#!/bin/bash

# Advanced Think AI Training Script with Configurable Options
# Allows customization of training parameters and modes

set -e

# Default values
TOOL_ITERATIONS=1000
CONVERSATION_ITERATIONS=1000
BATCH_SIZE=50
SELF_IMPROVEMENT="true"
MODE="comprehensive"
QUICK_MODE=false

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
NC='\033[0m'

# Help function
show_help() {
    echo "Think AI Advanced Training Script"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -t, --tool-iterations NUM      Number of tool training iterations (default: 1000)"
    echo "  -c, --conv-iterations NUM      Number of conversation iterations (default: 1000)"
    echo "  -b, --batch-size NUM           Batch size for training (default: 50)"
    echo "  -s, --self-improvement BOOL    Enable self-improvement (default: true)"
    echo "  -m, --mode MODE                Training mode: comprehensive|tool|conversation (default: comprehensive)"
    echo "  -q, --quick                    Quick training mode (100 iterations each)"
    echo "  -h, --help                     Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                             # Run full comprehensive training"
    echo "  $0 --quick                     # Quick test run"
    echo "  $0 --mode tool -t 2000         # Tool-focused training with 2000 iterations"
    echo "  $0 -t 500 -c 1500              # Custom iteration counts"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--tool-iterations)
            TOOL_ITERATIONS="$2"
            shift 2
            ;;
        -c|--conv-iterations)
            CONVERSATION_ITERATIONS="$2"
            shift 2
            ;;
        -b|--batch-size)
            BATCH_SIZE="$2"
            shift 2
            ;;
        -s|--self-improvement)
            SELF_IMPROVEMENT="$2"
            shift 2
            ;;
        -m|--mode)
            MODE="$2"
            shift 2
            ;;
        -q|--quick)
            QUICK_MODE=true
            TOOL_ITERATIONS=100
            CONVERSATION_ITERATIONS=100
            BATCH_SIZE=10
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

# Adjust iterations based on mode
if [ "$MODE" = "tool" ]; then
    CONVERSATION_ITERATIONS=0
elif [ "$MODE" = "conversation" ]; then
    TOOL_ITERATIONS=0
fi

# Header
echo -e "${PURPLE}╔════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║   Think AI Advanced Training System        ║${NC}"
echo -e "${PURPLE}╚════════════════════════════════════════════╝${NC}"
echo ""

# Display configuration
echo -e "${BLUE}📋 Training Configuration:${NC}"
echo -e "   Mode: ${YELLOW}$MODE${NC}"
if [ "$QUICK_MODE" = true ]; then
    echo -e "   Quick Mode: ${GREEN}Enabled${NC}"
fi
echo -e "   Tool Iterations: ${YELLOW}$TOOL_ITERATIONS${NC}"
echo -e "   Conversation Iterations: ${YELLOW}$CONVERSATION_ITERATIONS${NC}"
echo -e "   Batch Size: ${YELLOW}$BATCH_SIZE${NC}"
echo -e "   Self-Improvement: ${YELLOW}$SELF_IMPROVEMENT${NC}"
echo ""

# Estimate time
TOTAL_ITERATIONS=$((TOOL_ITERATIONS + CONVERSATION_ITERATIONS))
ESTIMATED_TIME=$((TOTAL_ITERATIONS * BATCH_SIZE / 1000))  # Rough estimate
echo -e "${BLUE}⏱️  Estimated training time: ~${ESTIMATED_TIME} seconds${NC}"
echo ""

# Create temporary Rust configuration file
CONFIG_FILE="training_config.rs"
cat > "$CONFIG_FILE" << EOF
use std::sync::Arc;
use think_ai_knowledge::{
    comprehensive_trainer::{ComprehensiveTrainer, ComprehensiveTrainingConfig},
    persistence::KnowledgePersistence,
    KnowledgeEngine,
};

fn main() {
    println!("🚀 Think AI Advanced Training - $MODE mode");
    
    let engine = Arc::new(KnowledgeEngine::new());
    
    // Load existing knowledge
    let persistence = KnowledgePersistence::new("knowledge_data/comprehensive_knowledge.json");
    if let Ok(nodes) = persistence.load() {
        println!("📚 Loaded {} existing knowledge nodes", nodes.len());
        engine.load_nodes(nodes);
    }

    // Configure training
    let config = ComprehensiveTrainingConfig {
        tool_iterations: $TOOL_ITERATIONS,
        conversation_iterations: $CONVERSATION_ITERATIONS,
        batch_size: $BATCH_SIZE,
        domains: think_ai_knowledge::KnowledgeDomain::all_domains(),
        enable_self_improvement: $SELF_IMPROVEMENT,
    };

    // Run training
    let mut trainer = ComprehensiveTrainer::new(engine.clone(), config);
    let result = trainer.train_comprehensive();

    // Save results
    let all_nodes = engine.get_all_nodes();
    persistence.save(&all_nodes).expect("Failed to save knowledge");
    
    println!("✅ Training complete! Saved {} knowledge nodes", all_nodes.len());
}
EOF

# Build the training system
echo -e "${BLUE}🔨 Building training system...${NC}"
cargo build --release --bin comprehensive-train

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Build failed!${NC}"
    rm -f "$CONFIG_FILE"
    exit 1
fi

# Create knowledge directory
mkdir -p knowledge_data

# Create progress monitoring script
MONITOR_PID=""
if command -v pv &> /dev/null; then
    # If pv is available, use it for progress
    echo -e "${GREEN}📊 Starting training with progress monitoring...${NC}"
else
    echo -e "${GREEN}🚀 Starting training...${NC}"
fi

# Run the training
START_TIME=$(date +%s)
./target/release/comprehensive-train

# Calculate actual time
END_TIME=$(date +%s)
ACTUAL_TIME=$((END_TIME - START_TIME))

# Clean up
rm -f "$CONFIG_FILE"

# Results summary
echo ""
echo -e "${PURPLE}╔════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║         Training Complete! 🎉              ║${NC}"
echo -e "${PURPLE}╚════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}📊 Summary:${NC}"
echo -e "   Training Mode: ${YELLOW}$MODE${NC}"
echo -e "   Total Iterations: ${YELLOW}$TOTAL_ITERATIONS${NC}"
echo -e "   Actual Time: ${YELLOW}${ACTUAL_TIME} seconds${NC}"
echo -e "   Knowledge Base: ${YELLOW}knowledge_data/comprehensive_knowledge.json${NC}"
echo ""

# Provide next steps based on mode
echo -e "${BLUE}🎯 Next Steps:${NC}"
case $MODE in
    comprehensive)
        echo -e "   1. Run ${YELLOW}./target/release/think-ai chat${NC} to test both tool and conversation abilities"
        echo -e "   2. Try asking technical questions and having natural conversations"
        ;;
    tool)
        echo -e "   1. Run ${YELLOW}./target/release/think-ai chat${NC} to test tool capabilities"
        echo -e "   2. Ask technical questions about programming, debugging, and optimization"
        ;;
    conversation)
        echo -e "   1. Run ${YELLOW}./target/release/think-ai chat${NC} to test conversation skills"
        echo -e "   2. Engage in natural dialogue and multi-turn conversations"
        ;;
esac
echo -e "   3. Check ${YELLOW}knowledge_data/${NC} for training artifacts"
echo ""

# Success message
if [ "$QUICK_MODE" = true ]; then
    echo -e "${GREEN}✨ Quick training completed successfully!${NC}"
else
    echo -e "${GREEN}✨ Full training completed successfully!${NC}"
fi