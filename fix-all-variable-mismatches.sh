#!/bin/bash
set -e

echo "Fixing all variable name mismatches..."

# Function to fix variable mismatches in a file
fix_mismatches() {
    local file=$1
    echo "Fixing $file..."
    
    # Fix parameter mismatches (___param or param___)
    sed -i 's/\b\([a-zA-Z_][a-zA-Z0-9_]*\)___:/\1:/g' "$file"
    sed -i 's/\b___\([a-zA-Z_][a-zA-Z0-9_]*\):/\1:/g' "$file"
    
    # Fix variable definitions (let ___var or let var___)
    sed -i 's/let ___\([a-zA-Z_][a-zA-Z0-9_]*\)\b/let \1/g' "$file"
    sed -i 's/let \([a-zA-Z_][a-zA-Z0-9_]*\)___\b/let \1/g' "$file"
    
    # Fix const definitions
    sed -i 's/const ___\([a-zA-Z_][a-zA-Z0-9_]*\)\b/const \1/g' "$file"
    sed -i 's/const \([a-zA-Z_][a-zA-Z0-9_]*\)___\b/const \1/g' "$file"
    
    # Fix function parameters
    sed -i 's/(\([^)]*\)\b\([a-zA-Z_][a-zA-Z0-9_]*\)___\b/(\1\2/g' "$file"
    sed -i 's/(\([^)]*\)\b___\([a-zA-Z_][a-zA-Z0-9_]*\)\b/(\1\2/g' "$file"
    sed -i 's/, \([a-zA-Z_][a-zA-Z0-9_]*\)___\b/, \1/g' "$file"
    sed -i 's/, ___\([a-zA-Z_][a-zA-Z0-9_]*\)\b/, \1/g' "$file"
}

# Find all Rust files with variable mismatches
echo "Finding files with variable mismatches..."
files=$(find . -name "*.rs" -type f | xargs grep -l "___\|[a-zA-Z_][a-zA-Z0-9_]*___" 2>/dev/null || true)

if [ -z "$files" ]; then
    echo "No files with variable mismatches found."
    exit 0
fi

# Fix each file
for file in $files; do
    fix_mismatches "$file"
done

echo "All variable mismatches fixed!"