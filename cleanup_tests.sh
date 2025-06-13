#!/bin/bash
# Cleanup test files created during debugging

echo "🧹 Cleaning up test files..."

# List of test files to keep
KEEP_FILES=(
    "test_simple_generation.py"
    "test_meta_tensor_fix.py"
    "quick_fix_test.py"
)

# Convert to associative array for faster lookup
declare -A keep_map
for f in "${KEEP_FILES[@]}"; do
    keep_map["$f"]=1
done

# Count files
total=0
removed=0

# Process test files
for file in test_*.py; do
    if [ -f "$file" ]; then
        total=$((total + 1))
        if [ -z "${keep_map[$file]}" ]; then
            echo "  Removing: $file"
            rm "$file"
            removed=$((removed + 1))
        else
            echo "  Keeping: $file"
        fi
    fi
done

echo ""
echo "✅ Cleanup complete!"
echo "   Total test files: $total"
echo "   Removed: $removed"
echo "   Kept: $((total - removed))"