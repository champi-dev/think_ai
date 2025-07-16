#!/bin/bash

echo "👁️ WATCHING FOR FILE CHANGES - AUTO LINT ON SAVE"
echo "==============================================="
echo ""
echo "Press Ctrl+C to stop watching"
echo ""

# Function to fix a specific file
fix_file() {
    local file=$1
    echo "🔧 Fixing: $file"
    
    # Fix common syntax issues
    sed -i 's/:_:/\:\:/g' "$file"
    sed -i 's/^\/\/! /\/\/ /g' "$file"
    
    # Remove trailing whitespace
    sed -i 's/[[:space:]]*$//' "$file"
    
    # Run rustfmt on the specific file
    rustfmt "$file" 2>/dev/null || true
}

# Watch for Rust file changes
cargo watch -s 'echo "File saved, running lint fixes..."' \
    -w . \
    --ignore target \
    --ignore '*.lock' \
    -x 'fmt' \
    -x 'clippy --fix --allow-dirty --allow-staged 2>/dev/null || true'

# Alternative: Use inotifywait if cargo-watch has issues
# while true; do
#     inotifywait -r -e modify,create --include '.*\.rs$' . 2>/dev/null | while read path action file; do
#         if [[ "$file" =~ \.rs$ ]]; then
#             fix_file "$path$file"
#         fi
#     done
# done
