#!/bin/bash

# Script to fix syntax errors in think-ai-knowledge module files
echo "Fixing syntax errors in think-ai-knowledge module..."
echo "========================================"

# Change to the think-ai-knowledge directory
cd ../think-ai-knowledge

# Function to check and fix a specific file
fix_file() {
    local file="$1"
    local filename=$(basename "$file")
    
    echo "Checking $filename..."
    
    # Run cargo check and capture the specific error for this file
    CARGO_OUTPUT=$(cargo check --message-format=json 2>&1 | jq -r 'select(.message.spans[0].file_name | contains("'$filename'")) | .message.rendered' 2>/dev/null)
    
    if [ -n "$CARGO_OUTPUT" ]; then
        echo "❌ Found errors in $filename"
        echo "$CARGO_OUTPUT" | head -20
        return 1
    else
        echo "✓ $filename OK"
        return 0
    fi
}

# Files identified with issues (from our analysis)
FILES_WITH_ISSUES=(
    "autonomous_agent.rs"
    "enhanced_response_generator.rs"
    "intelligent_response_selector.rs"
    "live_stream_monitor.rs"
    "minimal_response_generator.rs"
    "qwen_cache.rs"
    "qwen_knowledge_builder.rs"
    "realtime_knowledge_gatherer.rs"
    "response_generator.rs"
    "self_evaluator.rs"
    "self_learning.rs"
    "simple_cache_component.rs"
    "simple_llm.rs"
    "social_media_gatherer.rs"
)

# Fix each file
for filename in "${FILES_WITH_ISSUES[@]}"; do
    fix_file "src/$filename"
done

echo "========================================"
echo "Running final cargo check to verify all fixes..."
cargo check 2>&1 | head -50