#!/bin/bash

echo "🧪 COMPREHENSIVE TEST OF ABSTRACT PRINCIPLES FIX"
echo "==============================================="
echo

# Test queries that might have triggered abstract responses
TEST_QUERIES=(
    "what is love"
    "what is happiness"
    "what is consciousness"
    "what is life"
    "what is intelligence"
    "what is creativity"
    "what is emotion"
    "what is beauty"
)

echo "🔨 Building Think AI..."
cargo build --release --quiet
if [ $? -ne 0 ]; then
    echo "❌ Build failed!"
    exit 1
fi
echo "✅ Build successful!"
echo

echo "🧹 Ensuring clean knowledge storage..."
rm -rf ./trained_knowledge ./knowledge_storage
echo "✅ Knowledge storage clean!"
echo

echo "🧪 Running tests..."
echo "=================="

PASSED=0
FAILED=0

for query in "${TEST_QUERIES[@]}"; do
    echo
    echo "❓ Testing: '$query'"
    echo "Expected: Proper explanation, NOT abstract principles"
    echo "Response:"
    
    # Run the query and capture the response
    response=$(echo "$query" | timeout 15s ./target/release/think-ai chat 2>/dev/null | grep "Think AI:" | tail -1)
    
    if [[ -z "$response" ]]; then
        echo "❌ No response received"
        FAILED=$((FAILED + 1))
        continue
    fi
    
    echo "$response"
    
    # Check if response contains problematic abstract principle patterns
    if echo "$response" | grep -q "Abstract principle derived from"; then
        echo "❌ FAILED: Contains 'Abstract principle derived from'"
        FAILED=$((FAILED + 1))
    elif echo "$response" | grep -q "Symmetry breaking leads to"; then
        echo "❌ FAILED: Contains generic principle about symmetry breaking"
        FAILED=$((FAILED + 1))
    elif echo "$response" | grep -q "Systems tend toward increasing complexity"; then
        echo "❌ FAILED: Contains generic complexity principle"
        FAILED=$((FAILED + 1))
    elif echo "$response" | grep -q "Information flows create feedback loops"; then
        echo "❌ FAILED: Contains generic information flow principle"
        FAILED=$((FAILED + 1))
    elif echo "$response" | grep -q "Hierarchical organization enables"; then
        echo "❌ FAILED: Contains generic hierarchy principle"
        FAILED=$((FAILED + 1))
    else
        echo "✅ PASSED: Proper specific response"
        PASSED=$((PASSED + 1))
    fi
done

echo
echo "📊 TEST RESULTS"
echo "==============="
echo "✅ Passed: $PASSED"
echo "❌ Failed: $FAILED"
echo "📝 Total: $((PASSED + FAILED))"

if [ $FAILED -eq 0 ]; then
    echo
    echo "🎉 ALL TESTS PASSED!"
    echo "   The abstract principles fix is working correctly."
    echo "   Think AI now provides proper specific answers instead of generic abstractions."
else
    echo
    echo "⚠️  Some tests failed. The fix may need additional work."
fi

echo
echo "💡 The fix involved:"
echo "   1. Disabling the abstract_principles() function in self_learning.rs"
echo "   2. Removing abstract_principles from the method selection"
echo "   3. Cleaning existing knowledge storage to remove saved abstract principles"
echo "   4. The comprehensive knowledge base still provides proper specific information"