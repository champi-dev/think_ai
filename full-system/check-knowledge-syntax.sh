#!/bin/bash

# Script to check syntax errors in think-ai-knowledge module
echo "Checking syntax errors in think-ai-knowledge module..."
echo "========================================"

# Create a temporary file to store errors
ERROR_FILES=""
HAS_ERRORS=false

# Function to check a single file
check_file() {
    local file="$1"
    echo "Checking: $file"
    
    # Use rustc to check syntax (parse only, no compilation)
    # We use 2>&1 to capture stderr where syntax errors are reported
    OUTPUT=$(rustc --crate-type lib --edition 2021 "$file" -Z parse-only 2>&1)
    
    if [ $? -ne 0 ]; then
        echo "❌ SYNTAX ERROR in $file:"
        echo "$OUTPUT" | grep -E "(error|expected|unclosed|unexpected)" | head -20
        echo ""
        ERROR_FILES="$ERROR_FILES$file\n"
        HAS_ERRORS=true
    else
        echo "✓ OK"
    fi
}

# Check each .rs file
while IFS= read -r file; do
    check_file "$file"
done < <(find ../think-ai-knowledge/src -name "*.rs" -type f | sort)

echo "========================================"
if [ "$HAS_ERRORS" = true ]; then
    echo "❌ FILES WITH SYNTAX ERRORS:"
    echo -e "$ERROR_FILES"
else
    echo "✅ All files passed syntax check!"
fi