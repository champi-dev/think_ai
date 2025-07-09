#!/bin/bash

# Script to check syntax errors in think-ai-knowledge module
echo "Checking syntax errors in think-ai-knowledge module..."
echo "========================================"

# Navigate to the think-ai-knowledge directory
cd ../think-ai-knowledge

# First, try to build the module to catch all syntax errors at once
echo "Running cargo check on think-ai-knowledge module..."
echo ""

# Run cargo check and capture output
CARGO_OUTPUT=$(cargo check --message-format=short 2>&1)

# Check if cargo check succeeded
if [ $? -eq 0 ]; then
    echo "✅ No syntax errors found! All files compile successfully."
else
    echo "❌ Syntax errors found:"
    echo ""
    
    # Filter and display only syntax-related errors
    echo "$CARGO_OUTPUT" | grep -E "(error\[E|error:|expected|unclosed|unexpected|missing|cannot find)" | head -50
    
    echo ""
    echo "========================================"
    echo "Detailed error analysis:"
    echo ""
    
    # Extract files with errors
    echo "Files with errors:"
    echo "$CARGO_OUTPUT" | grep -E "^src/.*\.rs:" | cut -d: -f1 | sort -u
fi

# For more detailed analysis, let's also check individual files with basic syntax patterns
echo ""
echo "========================================"
echo "Checking for common syntax issues (unclosed delimiters)..."
echo ""

# Function to check for unclosed delimiters in a file
check_delimiters() {
    local file="$1"
    local filename=$(basename "$file")
    
    # Count opening and closing braces, brackets, and parentheses
    local open_braces=$(grep -o '{' "$file" | wc -l)
    local close_braces=$(grep -o '}' "$file" | wc -l)
    local open_brackets=$(grep -o '\[' "$file" | wc -l)
    local close_brackets=$(grep -o '\]' "$file" | wc -l)
    local open_parens=$(grep -o '(' "$file" | wc -l)
    local close_parens=$(grep -o ')' "$file" | wc -l)
    
    local has_issue=false
    
    if [ $open_braces -ne $close_braces ]; then
        echo "⚠️  $filename: Mismatched braces { } (open: $open_braces, close: $close_braces)"
        has_issue=true
    fi
    
    if [ $open_brackets -ne $close_brackets ]; then
        echo "⚠️  $filename: Mismatched brackets [ ] (open: $open_brackets, close: $close_brackets)"
        has_issue=true
    fi
    
    if [ $open_parens -ne $close_parens ]; then
        echo "⚠️  $filename: Mismatched parentheses ( ) (open: $open_parens, close: $close_parens)"
        has_issue=true
    fi
    
    if [ "$has_issue" = false ]; then
        echo "✓ $filename: Delimiters balanced"
    fi
}

# Check each file for delimiter issues
for file in src/*.rs; do
    if [ -f "$file" ]; then
        check_delimiters "$file"
    fi
done