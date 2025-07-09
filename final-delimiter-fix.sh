#!/bin/bash
set -e

echo "Final comprehensive delimiter fix..."

# Function to count braces excluding strings and comments
count_braces() {
    local file=$1
    # Remove strings and comments, then count braces
    local open=$(sed 's/"[^"]*"//g; s|//.*||g; s|/\*.*\*/||g' "$file" | grep -o '{' | wc -l)
    local close=$(sed 's/"[^"]*"//g; s|//.*||g; s|/\*.*\*/||g' "$file" | grep -o '}' | wc -l)
    echo "$((open - close))"
}

# Fix think-ai-consciousness files
echo "Checking think-ai-consciousness files..."
for file in think-ai-consciousness/src/*.rs think-ai-consciousness/src/**/*.rs; do
    if [ -f "$file" ]; then
        missing=$(count_braces "$file")
        if [ "$missing" -gt 0 ]; then
            echo "Adding $missing closing braces to $file"
            for i in $(seq 1 $missing); do
                echo "}" >> "$file"
            done
        fi
    fi
done

# Fix think-ai-core files
echo "Checking think-ai-core files..."
for file in think-ai-core/src/*.rs think-ai-core/src/**/*.rs; do
    if [ -f "$file" ]; then
        missing=$(count_braces "$file")
        if [ "$missing" -gt 0 ]; then
            echo "Adding $missing closing braces to $file"
            for i in $(seq 1 $missing); do
                echo "}" >> "$file"
            done
        fi
    fi
done

# Fix think-ai-vector files
echo "Checking think-ai-vector files..."
for file in think-ai-vector/src/*.rs think-ai-vector/src/**/*.rs; do
    if [ -f "$file" ]; then
        missing=$(count_braces "$file")
        if [ "$missing" -gt 0 ]; then
            echo "Adding $missing closing braces to $file"
            for i in $(seq 1 $missing); do
                echo "}" >> "$file"
            done
        fi
    fi
done

# Fix think-ai-image-gen files
echo "Checking think-ai-image-gen files..."
for file in think-ai-image-gen/src/*.rs; do
    if [ -f "$file" ]; then
        missing=$(count_braces "$file")
        if [ "$missing" -gt 0 ]; then
            echo "Adding $missing closing braces to $file"
            for i in $(seq 1 $missing); do
                echo "}" >> "$file"
            done
        fi
    fi
done

echo "Final delimiter fix complete"