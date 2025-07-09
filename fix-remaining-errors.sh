#!/bin/bash

echo "=== Fixing Remaining Compilation Errors ==="
echo

# Navigate to project root
cd /home/champi/Dev/think_ai

# Count initial errors
INITIAL_ERRORS=$(cargo check 2>&1 | grep -E "^error" | wc -l)
echo "Initial error count: $INITIAL_ERRORS"
echo

# Get detailed error summary
echo "Error summary by type:"
cargo check 2>&1 | grep -E "^error\[E" | cut -d']' -f1 | sort | uniq -c
echo

# Show first 10 errors with context
echo "First 10 errors with context:"
cargo check 2>&1 | grep -E "^error" -A3 | head -40
echo

# Summary of files with errors
echo "Files with errors:"
cargo check 2>&1 | grep -E "^ --> " | cut -d' ' -f3 | cut -d':' -f1 | sort | uniq -c | sort -nr | head -20
echo

# Check for undefined variable patterns
echo "Common variable naming issues (with underscores):"
cargo check 2>&1 | grep "cannot find value" | grep -E "___[a-zA-Z_]+" -o | sort | uniq -c

echo
echo "Run 'cargo check' for full error details"