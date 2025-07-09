#!/bin/bash

echo "=== Testing Syntax Fixes Locally ==="
echo

cd /home/champi/Dev/think_ai

echo "1. Running cargo check to count errors..."
ERROR_COUNT=$(cargo check 2>&1 | grep -E "^error" | wc -l)
echo "   Current error count: $ERROR_COUNT"
echo

echo "2. Main fixes applied:"
echo "   ✓ Fixed duplicate ProcessMessage struct in types.rs"
echo "   ✓ Fixed variable naming in evidence.rs (f__ to f)"
echo "   ✓ Fixed variable naming in shared_knowledge.rs (item___ to item, and others)"
echo "   ✓ Fixed missing ConversationContext type in response_generator.rs"
echo "   ✓ Added missing serde imports in llm_benchmarks.rs and o1_benchmark_monitor.rs"
echo "   ✓ Fixed format string placeholders in responder.rs"
echo "   ✓ Fixed format string arguments in automated_benchmark_runner.rs"
echo

echo "3. Progress summary:"
echo "   Initial errors: 51"
echo "   After fixes: $ERROR_COUNT"
echo "   Errors fixed: $((51 - ERROR_COUNT))"
echo "   Progress: $((100 * (51 - ERROR_COUNT) / 51))%"
echo

echo "4. Remaining error types:"
cargo check 2>&1 | grep -E "^error\[E" | cut -d']' -f1 | sort | uniq -c
echo

echo "5. Files with most remaining errors:"
cargo check 2>&1 | grep -E "^ --> " | cut -d' ' -f3 | cut -d':' -f1 | sort | uniq -c | sort -nr | head -10
echo

echo "To see full error details, run: cargo check"
echo "To continue fixing, focus on the files listed above."