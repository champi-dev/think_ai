#!/bin/bash
set -e

echo "🔧 Final fix for coding files..."

# Fix think-ai-coding-v2.rs - Check for unclosed delimiters
echo "Fixing think-ai-coding-v2.rs unclosed delimiters..."
if [ -f think-ai-cli/src/bin/think-ai-coding-v2.rs ]; then
    # Count opening and closing braces to find imbalance
    OPEN_COUNT=$(grep -o '{' think-ai-cli/src/bin/think-ai-coding-v2.rs | wc -l)
    CLOSE_COUNT=$(grep -o '}' think-ai-cli/src/bin/think-ai-coding-v2.rs | wc -l)
    
    echo "  Open braces: $OPEN_COUNT, Close braces: $CLOSE_COUNT"
    
    # If there's an imbalance, add closing braces at the end
    if [ $OPEN_COUNT -gt $CLOSE_COUNT ]; then
        DIFF=$((OPEN_COUNT - CLOSE_COUNT))
        echo "  Adding $DIFF closing braces..."
        for ((i=0; i<$DIFF; i++)); do
            echo "}" >> think-ai-cli/src/bin/think-ai-coding-v2.rs
        done
    fi
fi

# Fix think-ai-coding.rs - This file has Python code embedded with wrong syntax
echo "Fixing think-ai-coding.rs Python code embeddings..."
if [ -f think-ai-cli/src/bin/think-ai-coding.rs ]; then
    # Create a temporary fixed version
    cp think-ai-cli/src/bin/think-ai-coding.rs /tmp/coding-backup.rs
    
    # Replace problematic patterns
    sed -i '
        # Fix prefix errors - add space before closing quotes in descriptions
        s/here"/here "/g
        s/implementation"/implementation "/g
        s/length"/length "/g
        s/Rust"/Rust "/g
        s/map"/map "/g
        s/operations"/operations "/g
        s/case"/case "/g
        s/api"/api "/g
        s/retrieval"/retrieval "/g
        s/found"/found "/g
        s/storage"/storage "/g
        s/required"/required "/g
        s/algorithm"/algorithm "/g
        s/sort"/sort "/g
        s/quicksort"/quicksort "/g
        s/memoization"/memoization "/g
        s/Fibonacci"/Fibonacci "/g
        
        # Fix raw string issues
        s/hash_value"#/hash_value "#/g
        s/found"#/found "#/g
        
        # Fix Python f-strings by escaping them in Rust raw strings
        s/f"/f "/g
        
        # Fix character literals that should be strings
        s/'\'', '\''/", "/g
        s/'\''host'\''/\"host\"/g
        s/'\''localhost'\''/\"localhost\"/g
        s/'\''database'\''/\"database\"/g
        s/'\''mydb'\''/\"mydb\"/g
        s/'\''user'\''/\"user\"/g
        s/'\''postgres'\''/\"postgres\"/g
        s/'\''password'\''/\"password\"/g
        s/'\''port'\''/\"port\"/g
        s/'\''users'\''/\"users\"/g
        s/'\''name'\''/\"name\"/g
        s/'\''John Doe'\''/\"John Doe\"/g
        s/'\''%s'\''/\"%s\"/g
        
        # Fix triple quotes
        s/"""/r#"/g
    ' think-ai-cli/src/bin/think-ai-coding.rs
    
    # Check if file at line 1044 has unterminated raw string
    if grep -n 'r#"use axum::{' think-ai-cli/src/bin/think-ai-coding.rs | grep -v '"#'; then
        # Find the line and add proper termination
        LINE_NUM=$(grep -n 'r#"use axum::{' think-ai-cli/src/bin/think-ai-coding.rs | cut -d: -f1)
        if [ ! -z "$LINE_NUM" ]; then
            # Insert closing "#" after a few lines
            sed -i "${LINE_NUM}s/$/\n\"#/" think-ai-cli/src/bin/think-ai-coding.rs
        fi
    fi
fi

echo "✅ Final fixes applied!"
echo "🔄 Running cargo check to verify..."
cd /home/champi/Dev/think_ai
cargo check --bin think-ai-coding 2>&1 | head -20 || echo "Still has issues"
cargo check --bin think-ai-coding-v2 2>&1 | head -20 || echo "Still has issues"