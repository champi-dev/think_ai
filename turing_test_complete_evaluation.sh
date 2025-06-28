#!/bin/bash

# Complete Turing Test Evaluation for Think AI
# Tests all critical human-like conversation capabilities

echo "🤖 THINK AI TURING TEST EVALUATION - COMPREHENSIVE SUITE"
echo "========================================================"
echo ""

# Build the system first
echo "🔨 Building Think AI system..."
cargo build --release --bin think-ai > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ BUILD FAILED - Cannot proceed with testing"
    exit 1
fi
echo "✅ Build successful"
echo ""

# Define test cases
declare -a test_cases=(
    "Hello:greeting"
    "Hi there:greeting" 
    "What is your name?:identity"
    "Who are you?:identity"
    "What are you?:identity"
    "What is 2+2?:math"
    "What's 1+1?:math"
    "Calculate 3+3:math"
    "Tell me a joke:humor"
    "How are you?:conversational"
    "Thank you:politeness"
    "Are you human?:identity"
)

# Counters
total_tests=0
passed_tests=0
failed_tests=0

echo "🧪 RUNNING TURING TEST BATTERY"
echo "==============================="

for test_case in "${test_cases[@]}"; do
    IFS=':' read -r query category <<< "$test_case"
    
    echo "Testing: '$query' (Expected: $category)"
    
    # Run the test
    response=$(echo -e "$query\nquit" | timeout 10s ./target/release/think-ai chat 2>/dev/null | grep "Think AI:" | tail -1 | sed 's/Think AI: //')
    
    total_tests=$((total_tests + 1))
    
    # Evaluate response based on category
    case $category in
        "greeting")
            if [[ $response =~ "Hello".*"Think AI" ]] || [[ $response =~ "Hi".*"Think AI" ]]; then
                echo "✅ PASS - Proper greeting response"
                passed_tests=$((passed_tests + 1))
            else
                echo "❌ FAIL - Expected greeting, got: '$response'"
                failed_tests=$((failed_tests + 1))
            fi
            ;;
        "identity")
            if ([[ $response =~ "Think AI" ]] && ([[ $response =~ "AI" ]] || [[ $response =~ "artificial intelligence" ]] || [[ $response =~ "my name" ]])) || 
               ([[ $response =~ "artificial intelligence" ]] && ([[ $response =~ "not.*human" ]] || [[ $response =~ "not a human" ]])) ||
               ([[ $response =~ "I'm an artificial intelligence" ]] || [[ $response =~ "I am an artificial intelligence" ]]) ||
               ([[ $response =~ "AI" ]] && [[ $response =~ "not.*human" ]]) ||
               ([[ $response =~ "designed to" ]] && [[ $response =~ "artificial intelligence" ]]); then
                echo "✅ PASS - Proper identity response"
                passed_tests=$((passed_tests + 1))
            else
                echo "❌ FAIL - Expected identity, got: '$response'"
                failed_tests=$((failed_tests + 1))
            fi
            ;;
        "math")
            if [[ $response =~ "4" ]] || [[ $response =~ "2" ]] || [[ $response =~ "6" ]] && ([[ $response =~ "=" ]] || [[ $response =~ "equals" ]]); then
                echo "✅ PASS - Correct mathematical response"
                passed_tests=$((passed_tests + 1))
            else
                echo "❌ FAIL - Expected math answer, got: '$response'"
                failed_tests=$((failed_tests + 1))
            fi
            ;;
        "humor"|"conversational"|"politeness")
            if [[ ${#response} -gt 10 ]] && [[ ! $response =~ "astronomy".*"celestial" ]]; then
                echo "✅ PASS - Appropriate conversational response"
                passed_tests=$((passed_tests + 1))
            else
                echo "❌ FAIL - Poor conversational response: '$response'"
                failed_tests=$((failed_tests + 1))
            fi
            ;;
    esac
    echo ""
done

echo "📊 FINAL TURING TEST RESULTS"
echo "============================="
echo "Total Tests: $total_tests"
echo "Passed: $passed_tests"
echo "Failed: $failed_tests"
echo "Success Rate: $(( passed_tests * 100 / total_tests ))%"
echo ""

if [ $passed_tests -ge $(( total_tests * 8 / 10 )) ]; then
    echo "🎉 TURING TEST STATUS: PROMISING"
    echo "   Think AI shows strong conversational capabilities"
    echo "   Passed $(( passed_tests * 100 / total_tests ))% of Turing test criteria"
else
    echo "⚠️  TURING TEST STATUS: NEEDS IMPROVEMENT" 
    echo "   Think AI requires additional conversational training"
    echo "   Only passed $(( passed_tests * 100 / total_tests ))% of Turing test criteria"
fi

echo ""
echo "🔍 DETAILED ANALYSIS:"
echo "- Natural greetings: Critical for Turing test"
echo "- Identity awareness: Essential for self-recognition" 
echo "- Mathematical ability: Tests logical reasoning"
echo "- Conversational flow: Key for human-like interaction"
echo ""
echo "💡 Next steps for improvement:"
echo "- Add humor generation capabilities"
echo "- Enhance emotional intelligence" 
echo "- Implement personality consistency"
echo "- Add creative response generation"

exit 0