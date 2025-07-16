#!/bin/bash

# E2E test script for quantum consciousness fix
# Tests that non-philosophical queries don't get quantum responses

set -e

echo "=== Building Think AI with fixes ==="
cd /home/administrator/think_ai
cargo build --release --bin think-ai

echo -e "\n=== Testing non-philosophical queries ==="
echo "These should NOT return quantum field responses:"

# Test mathematical query
echo -e "\n1. Testing: 2+2"
echo "2+2" | timeout 5 ./target/release/think-ai chat | head -20

# Test technical query
echo -e "\n2. Testing: how to install rust"
echo "how to install rust" | timeout 5 ./target/release/think-ai chat | head -20

# Test simple greeting
echo -e "\n3. Testing: hello"
echo "hello" | timeout 5 ./target/release/think-ai chat | head -20

# Test coding query
echo -e "\n4. Testing: write a python function"
echo "write a python function" | timeout 5 ./target/release/think-ai chat | head -20

echo -e "\n=== Testing philosophical queries ==="
echo "These SHOULD return quantum/philosophical responses:"

# Test philosophical query
echo -e "\n5. Testing: what is consciousness"
echo "what is consciousness" | timeout 5 ./target/release/think-ai chat | head -20

# Test meaning query
echo -e "\n6. Testing: what is the meaning of life"
echo "what is the meaning of life" | timeout 5 ./target/release/think-ai chat | head -20

echo -e "\n=== Running unit tests ==="
cargo test -p think-ai-knowledge quantum_consciousness
cargo test -p think-ai-knowledge response_generator_integration

echo -e "\n=== E2E tests completed ==="