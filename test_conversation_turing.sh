#!/bin/bash
# Turing Test Conversation Validator for Think AI
# Tests basic conversational abilities required for human-like interaction

echo "🧪 Testing Think AI Conversational Turing Test Readiness..."
echo "========================================================"

# Ensure binary exists
if [[ ! -f "./target/release/think-ai" ]]; then
    echo "❌ think-ai binary not found. Run 'cargo build --release' first."
    exit 1
fi

# Create test results directory
mkdir -p ./turing_test_results
cd turing_test_results

# Test 1: Basic Greeting Response
echo "Test 1: Basic Greeting Recognition..."
echo -e "Hello, how are you?\nquit" | timeout 20 ../target/release/think-ai chat 2>/dev/null > greeting_test.log
if grep -i -E "(hello|hi|good|fine|well|great)" greeting_test.log | grep -v "Philosophy\|Bitcoin\|mathematical"; then
    echo "✅ PASSED: Responds appropriately to greetings"
    GREETING_PASS=1
else
    echo "❌ FAILED: Does not respond appropriately to greetings"
    echo "   Actual response:"
    grep "Think AI:" greeting_test.log | head -1 | sed 's/Think AI: /   /'
    GREETING_PASS=0
fi

# Test 2: Identity Awareness
echo ""
echo "Test 2: Self-Identity Recognition..."
echo -e "What is your name?\nquit" | timeout 20 ../target/release/think-ai chat 2>/dev/null > identity_test.log
if grep -i -E "(think ai|my name|i am|i'm)" identity_test.log | grep -v "Philosophy\|history\|mathematical"; then
    echo "✅ PASSED: Correctly identifies itself"
    IDENTITY_PASS=1
else
    echo "❌ FAILED: Does not correctly identify itself"
    echo "   Actual response:"
    grep "Think AI:" identity_test.log | head -1 | sed 's/Think AI: /   /'
    IDENTITY_PASS=0
fi

# Test 3: Simple Mathematics
echo ""
echo "Test 3: Basic Arithmetic..."
echo -e "What is 2+2?\nquit" | timeout 20 ../target/release/think-ai chat 2>/dev/null > math_test.log
if grep -E "(^|[^0-9])4($|[^0-9])|four" math_test.log; then
    echo "✅ PASSED: Can perform basic arithmetic"
    MATH_PASS=1
else
    echo "❌ FAILED: Cannot perform basic arithmetic"
    echo "   Actual response:"
    grep "Think AI:" math_test.log | head -1 | sed 's/Think AI: /   /'
    MATH_PASS=0
fi

# Test 4: Humor Recognition
echo ""
echo "Test 4: Humor/Joke Handling..."
echo -e "Tell me a joke\nquit" | timeout 20 ../target/release/think-ai chat 2>/dev/null > humor_test.log
if grep -i -E "(joke|funny|laugh|humor|haha|lol)" humor_test.log || grep -E "Why|What do you call|How many" humor_test.log; then
    echo "✅ PASSED: Recognizes and responds to humor requests"
    HUMOR_PASS=1
else
    echo "❌ FAILED: Does not recognize humor requests"
    echo "   Actual response:"
    grep "Think AI:" humor_test.log | head -1 | sed 's/Think AI: /   /'
    HUMOR_PASS=0
fi

# Test 5: Context Awareness
echo ""
echo "Test 5: Contextual Conversation..."
echo -e "I like cats\nWhat do you think about them?\nquit" | timeout 20 ../target/release/think-ai chat 2>/dev/null > context_test.log
if grep -i -E "(cat|feline|pet|animal)" context_test.log | grep -v "Bitcoin\|philosophy\|mathematical"; then
    echo "✅ PASSED: Shows contextual awareness"
    CONTEXT_PASS=1
else
    echo "❌ FAILED: No contextual awareness"
    echo "   Actual response:"
    grep "Think AI:" context_test.log | tail -1 | sed 's/Think AI: /   /'
    CONTEXT_PASS=0
fi

# Test 6: Unexpected Question Handling
echo ""
echo "Test 6: Unexpected Question Handling..."
echo -e "What's your favorite color?\nquit" | timeout 20 ../target/release/think-ai chat 2>/dev/null > unexpected_test.log
if grep -i -E "(color|don't have|preference|like|blue|red|green)" unexpected_test.log | grep -v "Bitcoin\|philosophy\|mathematical"; then
    echo "✅ PASSED: Handles unexpected questions appropriately"
    UNEXPECTED_PASS=1
else
    echo "❌ FAILED: Does not handle unexpected questions well"
    echo "   Actual response:"
    grep "Think AI:" unexpected_test.log | head -1 | sed 's/Think AI: /   /'
    UNEXPECTED_PASS=0
fi

# Calculate overall score
TOTAL_TESTS=6
PASSED_TESTS=$((GREETING_PASS + IDENTITY_PASS + MATH_PASS + HUMOR_PASS + CONTEXT_PASS + UNEXPECTED_PASS))
SCORE=$((PASSED_TESTS * 100 / TOTAL_TESTS))

echo ""
echo "========================================================"
echo "🏆 TURING TEST RESULTS SUMMARY"
echo "========================================================"
echo "Tests Passed: $PASSED_TESTS/$TOTAL_TESTS"
echo "Overall Score: $SCORE%"
echo ""

# Provide assessment
if [ $SCORE -eq 100 ]; then
    echo "🎉 EXCELLENT: System shows strong Turing test potential!"
    echo "   Ready for advanced human-like conversation testing."
elif [ $SCORE -ge 80 ]; then
    echo "✅ GOOD: System shows basic conversational abilities."
    echo "   Some improvements needed for full Turing test readiness."
elif [ $SCORE -ge 50 ]; then
    echo "⚠️  FAIR: System has partial conversational functionality."
    echo "   Significant improvements needed for Turing test readiness."
elif [ $SCORE -ge 20 ]; then
    echo "❌ POOR: System has minimal conversational abilities."
    echo "   Major redesign required for Turing test readiness."
else
    echo "💥 CRITICAL FAILURE: System lacks basic conversational functionality."
    echo "   Complete conversation system rebuild required."
fi

echo ""
echo "Test logs saved in: $(pwd)"
echo "Use these logs to identify specific issues and improvements needed."

cd ..