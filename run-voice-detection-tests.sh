#!/bin/bash

echo "========================================="
echo "Running Voice Detection Tests"
echo "========================================="

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to run a test and check result
run_test() {
    local test_name=$1
    local test_command=$2
    
    echo -e "\n${BLUE}Running: $test_name${NC}"
    echo "----------------------------------------"
    
    if eval $test_command; then
        echo -e "${GREEN}✓ $test_name passed${NC}"
        return 0
    else
        echo -e "${RED}✗ $test_name failed${NC}"
        return 1
    fi
}

# Track test results
TESTS_RUN=0
TESTS_PASSED=0

# 1. Run Frontend Unit Tests
if [ -f "frontend/src/components/AutoVoiceDetector.test.jsx" ]; then
    ((TESTS_RUN++))
    if run_test "Frontend Unit Tests" "cd frontend && npm test -- AutoVoiceDetector.test.jsx --run"; then
        ((TESTS_PASSED++))
    fi
else
    echo -e "${RED}Unit test file not found${NC}"
fi

# 2. Run Integration Tests
if [ -f "tests/integration/voice-detection.test.js" ]; then
    ((TESTS_RUN++))
    if run_test "Integration Tests" "npx playwright test tests/integration/voice-detection.test.js"; then
        ((TESTS_PASSED++))
    fi
else
    echo -e "${RED}Integration test file not found${NC}"
fi

# 3. Run E2E Tests on Local
echo -e "\n${BLUE}Testing Local Environment${NC}"
((TESTS_RUN++))
if run_test "E2E Local Tests" "PROD_URL=http://localhost:8080 node e2e-voice-detection-prod.js"; then
    ((TESTS_PASSED++))
fi

# 4. Run E2E Tests on Production (if URL provided)
if [ ! -z "$PROD_URL" ]; then
    echo -e "\n${BLUE}Testing Production Environment${NC}"
    ((TESTS_RUN++))
    if run_test "E2E Production Tests" "node e2e-voice-detection-prod.js"; then
        ((TESTS_PASSED++))
    fi
fi

# 5. Generate Combined Report
echo -e "\n${BLUE}Generating Combined Test Report...${NC}"

# Create summary report
cat > voice-detection-test-summary.md << EOF
# Voice Detection Test Summary

**Date:** $(date)
**Total Tests Run:** $TESTS_RUN
**Tests Passed:** $TESTS_PASSED
**Tests Failed:** $((TESTS_RUN - TESTS_PASSED))
**Success Rate:** $(awk "BEGIN {printf \"%.2f\", ($TESTS_PASSED/$TESTS_RUN)*100}")%

## Test Results

### Unit Tests
- AutoVoiceDetector Component: $([ -f "frontend/coverage/lcov-report/index.html" ] && echo "✓ See coverage report" || echo "⚠️ No coverage report")

### Integration Tests
- Voice Detection Flow: $([ -f "test-results/index.html" ] && echo "✓ See test report" || echo "⚠️ No test report")

### E2E Tests
- Local Environment: $([ -f "voice-detection-test-results/test-report.html" ] && echo "✓ See test report" || echo "⚠️ No test report")
$([ ! -z "$PROD_URL" ] && echo "- Production Environment: $([ -f "voice-detection-test-results/test-report.html" ] && echo "✓ See test report" || echo "⚠️ No test report")")

## Screenshots
$(ls voice-detection-test-results/*.png 2>/dev/null | wc -l) screenshots captured

## Recommendations
$(if [ $TESTS_PASSED -eq $TESTS_RUN ]; then
    echo "✅ All tests passed! Voice detection feature is working correctly."
else
    echo "⚠️ Some tests failed. Please review the test reports for details."
fi)
EOF

echo -e "\n${BLUE}Test Summary:${NC}"
cat voice-detection-test-summary.md

# Final result
echo -e "\n========================================="
if [ $TESTS_PASSED -eq $TESTS_RUN ]; then
    echo -e "${GREEN}✓ All tests passed! ($TESTS_PASSED/$TESTS_RUN)${NC}"
    exit 0
else
    echo -e "${RED}✗ Some tests failed! ($TESTS_PASSED/$TESTS_RUN passed)${NC}"
    exit 1
fi