#!/bin/bash

echo "🎯 Direct Natural Language Test"
echo "=============================="

# Build first
echo "Building..."
cargo build --release --bin think-ai 2>&1 | grep -E "(error|warning|Finished)" | tail -5

# Direct test of specific queries
echo -e "\n1. Testing greeting:"
echo "Hello!" | timeout 3 ./target/release/think-ai chat 2>&1 | grep -E "(Think AI:|Hello|Hi|Greetings)" -A 1

echo -e "\n2. Testing identity:"
echo "Who are you?" | timeout 3 ./target/release/think-ai chat 2>&1 | grep -E "(Think AI:|I'm|I am)" -A 1

echo -e "\n3. Testing capabilities:"
echo "What can you do?" | timeout 3 ./target/release/think-ai chat 2>&1 | grep -E "(Think AI:|help|assist|can)" -A 1

echo -e "\n4. Testing knowledge:"
echo "What is consciousness?" | timeout 3 ./target/release/think-ai chat 2>&1 | grep -E "(Think AI:|Consciousness|awareness)" -A 2

echo -e "\nDone!"