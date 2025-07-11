#!/bin/bash

# Script to copy markdown improvements to other HTML files

echo "Copying markdown rendering improvements to other files..."

# List of files to update
files=(
    "/home/administrator/think_ai/minimal_3d.html"
    "/home/administrator/think_ai/deployment/minimal_3d.html"
    "/home/administrator/think_ai/deployment-quantum/minimal_3d.html"
)

# Source file with improvements
source_file="/home/administrator/think_ai/minimal_3d_markdown.html"

echo "Source file: $source_file"
echo "Target files to update:"
for file in "${files[@]}"; do
    echo "  - $file"
done

# Copy the improved file to all locations
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        cp "$source_file" "$file"
        echo "✓ Updated: $file"
    else
        echo "✗ File not found: $file"
    fi
done

echo "Done! All files have been updated with markdown rendering improvements."