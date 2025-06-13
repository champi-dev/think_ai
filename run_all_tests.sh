#!/bin/bash
# Think AI Comprehensive Test Runner
# Runs all tests and generates evidence

set -e

echo "🚀 Think AI Comprehensive Test Suite"
echo "===================================="
echo "Starting at: $(date)"
echo

# Create test results directory
TEST_DIR="test_results_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$TEST_DIR"

# Function to run test and capture output
run_test() {
    local test_name=$1
    local test_command=$2
    local output_file="$TEST_DIR/${test_name}.log"
    
    echo "Running: $test_name..."
    if $test_command > "$output_file" 2>&1; then
        echo "✅ $test_name: PASSED"
        return 0
    else
        echo "❌ $test_name: FAILED (see $output_file)"
        return 1
    fi
}

# Install dependencies if needed
echo "📦 Installing dependencies..."
pip install -r requirements-fast.txt > "$TEST_DIR/install.log" 2>&1 || true

# Install Think AI CLI
echo "📦 Installing Think AI CLI..."
cd think-ai-cli/python
pip install -e . > "$TEST_DIR/cli_install.log" 2>&1 || true
cd ../..

# Run tests
TOTAL_TESTS=0
PASSED_TESTS=0

# 1. Unit tests
((TOTAL_TESTS++))
if run_test "unit_tests" "python -m pytest tests/unit/ -v"; then
    ((PASSED_TESTS++))
fi

# 2. Integration tests
((TOTAL_TESTS++))
if run_test "integration_tests" "python -m pytest tests/integration/ -v"; then
    ((PASSED_TESTS++))
fi

# 3. Think AI Linter
((TOTAL_TESTS++))
if run_test "think_ai_linter" "python think_ai_linter_enhanced.py"; then
    ((PASSED_TESTS++))
fi

# 4. CLI comprehensive tests
((TOTAL_TESTS++))
if run_test "cli_comprehensive" "python test_think_ai_comprehensive.py"; then
    ((PASSED_TESTS++))
fi

# 5. Performance tests
((TOTAL_TESTS++))
if run_test "performance" "python think_ai_performance_test.py"; then
    ((PASSED_TESTS++))
fi

# 6. Dependency resolver test
((TOTAL_TESTS++))
if run_test "dependency_resolver" "python test_deps_installation_fixed.py"; then
    ((PASSED_TESTS++))
fi

# 7. Code generation test
((TOTAL_TESTS++))
if run_test "code_generation" "python demo_enhanced_code_gen.py"; then
    ((PASSED_TESTS++))
fi

# Generate summary report
SUMMARY_FILE="$TEST_DIR/test_summary.txt"
cat > "$SUMMARY_FILE" << EOF
Think AI Test Summary
====================
Date: $(date)
Total Tests: $TOTAL_TESTS
Passed: $PASSED_TESTS
Failed: $((TOTAL_TESTS - PASSED_TESTS))
Success Rate: $(echo "scale=2; $PASSED_TESTS * 100 / $TOTAL_TESTS" | bc)%

Test Results:
EOF

# Add individual test results
for log_file in "$TEST_DIR"/*.log; do
    test_name=$(basename "$log_file" .log)
    if grep -q "FAILED\|Error\|error" "$log_file"; then
        echo "❌ $test_name: FAILED" >> "$SUMMARY_FILE"
    else
        echo "✅ $test_name: PASSED" >> "$SUMMARY_FILE"
    fi
done

# Display summary
echo
echo "===================================="
cat "$SUMMARY_FILE"
echo "===================================="
echo "Full results saved to: $TEST_DIR"

# Copy test evidence if it exists
if [ -d "test_evidence" ]; then
    cp -r test_evidence/* "$TEST_DIR/" 2>/dev/null || true
fi

if [ -d "performance_results" ]; then
    cp -r performance_results "$TEST_DIR/" 2>/dev/null || true
fi

# Exit with appropriate code
if [ $PASSED_TESTS -eq $TOTAL_TESTS ]; then
    echo "🎉 All tests passed!"
    exit 0
else
    echo "⚠️  Some tests failed!"
    exit 1
fi