#!/bin/bash

echo "Checking compilation errors for full-system..."
cd /home/champi/Dev/think_ai/full-system

echo "Building with cargo check for faster error detection..."
cargo check 2>&1 | grep -E "(error\[|warning:|error:)" | head -50

echo ""
echo "Summary of unique error types:"
cargo check 2>&1 | grep "error\[" | cut -d':' -f1 | sort | uniq -c