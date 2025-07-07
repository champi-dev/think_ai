#!/bin/bash

echo "🧪 Testing Think AI Coding CLI"
echo "=============================="
echo ""

# Test 1: Help
echo "Test 1: Help command"
./target/release/think-ai-coding --help
echo "✅ Help test passed"
echo ""

# Test 2: Generate Python Hello World
echo "Test 2: Generate Python Hello World"
./target/release/think-ai-coding generate "hello world" --language python > /tmp/test_hello.py
if grep -q "Hello, World!" /tmp/test_hello.py; then
    echo "✅ Python Hello World test passed"
else
    echo "❌ Python Hello World test failed"
fi
echo ""

# Test 3: Generate REST API
echo "Test 3: Generate Python REST API"
./target/release/think-ai-coding generate "rest api" --language python > /tmp/test_api.py
if grep -q "Flask" /tmp/test_api.py; then
    echo "✅ REST API test passed"
else
    echo "❌ REST API test failed"
fi
echo ""

# Test 4: Explain concept
echo "Test 4: Explain O(1)"
./target/release/think-ai-coding explain "O(1)" > /tmp/test_explain.txt
if grep -q "constant time" /tmp/test_explain.txt; then
    echo "✅ Explain test passed"
else
    echo "❌ Explain test failed"
fi
echo ""

# Test 5: Different language
echo "Test 5: Generate JavaScript code"
./target/release/think-ai-coding generate "hello world" --language javascript > /tmp/test_js.js
if grep -q "console.log" /tmp/test_js.js; then
    echo "✅ JavaScript test passed"
else
    echo "❌ JavaScript test failed"
fi
echo ""

echo "🎉 All tests completed!"
echo ""
echo "To try interactive mode, run:"
echo "  ./target/release/think-ai-coding chat"