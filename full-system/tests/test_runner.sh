#!/bin/bash
# Automated test runner with coverage and monitoring

set -e

COVERAGE_THRESHOLD=100
TEST_RESULTS_DIR="/home/champi/Dev/think_ai/test-results"
WHATSAPP_NUMBER="+573026132990"

# Create results directory
mkdir -p "$TEST_RESULTS_DIR"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Starting comprehensive test suite...${NC}"

# Function to send WhatsApp notification
send_whatsapp() {
    local message="$1"
    local severity="$2"
    
    if [ -n "$TWILIO_ACCOUNT_SID" ] && [ -n "$TWILIO_AUTH_TOKEN" ]; then
        curl -X POST "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_ACCOUNT_SID/Messages.json" \
            --data-urlencode "From=whatsapp:$TWILIO_WHATSAPP_FROM" \
            --data-urlencode "To=whatsapp:$WHATSAPP_NUMBER" \
            --data-urlencode "Body=🤖 ThinkAI Test Alert ($severity): $message" \
            -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN" > /dev/null 2>&1
    fi
}

# Install coverage tools if not present
if ! command -v cargo-tarpaulin &> /dev/null; then
    echo "Installing cargo-tarpaulin..."
    cargo install cargo-tarpaulin
fi

# Run unit tests with coverage
echo -e "\n${YELLOW}Running unit tests with coverage...${NC}"
cargo tarpaulin --out Html --out Json --output-dir "$TEST_RESULTS_DIR" \
    --exclude-files "*/tests/*" --exclude-files "*/target/*" \
    --timeout 300 --all-features 2>&1 | tee "$TEST_RESULTS_DIR/unit_test.log"

# Extract coverage percentage
COVERAGE=$(grep -oP 'Coverage is \K[0-9.]+' "$TEST_RESULTS_DIR/unit_test.log" || echo "0")

# Check coverage threshold
if (( $(echo "$COVERAGE < $COVERAGE_THRESHOLD" | bc -l) )); then
    echo -e "${RED}Coverage ${COVERAGE}% is below threshold ${COVERAGE_THRESHOLD}%${NC}"
    send_whatsapp "Unit test coverage is only ${COVERAGE}%, below ${COVERAGE_THRESHOLD}% threshold" "ERROR"
    exit 1
else
    echo -e "${GREEN}Coverage ${COVERAGE}% meets threshold${NC}"
fi

# Start service for E2E tests
echo -e "\n${YELLOW}Starting service for E2E tests...${NC}"
cd /home/champi/Dev/think_ai/full-system
PORT=7777 cargo run --release --bin think-ai-full > "$TEST_RESULTS_DIR/service.log" 2>&1 &
SERVICE_PID=$!

# Wait for service to start
sleep 10

# Check if service is running
if ! curl -s http://localhost:7777/health > /dev/null; then
    echo -e "${RED}Service failed to start${NC}"
    cat "$TEST_RESULTS_DIR/service.log"
    send_whatsapp "Service failed to start for E2E tests" "CRITICAL"
    kill $SERVICE_PID 2>/dev/null || true
    exit 1
fi

# Run E2E tests
echo -e "\n${YELLOW}Running E2E tests...${NC}"
export WHATSAPP_TO_NUMBER="$WHATSAPP_NUMBER"
cargo test --test e2e_tests -- --test-threads=1 --nocapture 2>&1 | tee "$TEST_RESULTS_DIR/e2e_test.log"
E2E_RESULT=${PIPESTATUS[0]}

# Run integration tests
echo -e "\n${YELLOW}Running integration tests...${NC}"
cargo test --test integration_tests 2>&1 | tee "$TEST_RESULTS_DIR/integration_test.log"
INTEGRATION_RESULT=${PIPESTATUS[0]}

# Stop service
kill $SERVICE_PID 2>/dev/null || true

# Generate test report
echo -e "\n${YELLOW}Generating test report...${NC}"
cat > "$TEST_RESULTS_DIR/test_report.json" <<EOF
{
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "coverage": $COVERAGE,
    "unit_tests": $([ -f "$TEST_RESULTS_DIR/unit_test.log" ] && grep -c "test result: ok" "$TEST_RESULTS_DIR/unit_test.log" || echo 0),
    "e2e_tests": $([ $E2E_RESULT -eq 0 ] && echo "true" || echo "false"),
    "integration_tests": $([ $INTEGRATION_RESULT -eq 0 ] && echo "true" || echo "false"),
    "errors": []
}
EOF

# Check overall results
if [ $E2E_RESULT -ne 0 ] || [ $INTEGRATION_RESULT -ne 0 ]; then
    echo -e "${RED}Some tests failed${NC}"
    send_whatsapp "Test suite failed. E2E: $([ $E2E_RESULT -eq 0 ] && echo "✓" || echo "✗"), Integration: $([ $INTEGRATION_RESULT -eq 0 ] && echo "✓" || echo "✗")" "ERROR"
    exit 1
else
    echo -e "${GREEN}All tests passed with ${COVERAGE}% coverage!${NC}"
    send_whatsapp "All tests passed! Coverage: ${COVERAGE}%" "INFO"
fi

# Create HTML dashboard
cat > "$TEST_RESULTS_DIR/dashboard.html" <<EOF
<!DOCTYPE html>
<html>
<head>
    <title>ThinkAI Test Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .card { background: white; padding: 20px; margin: 10px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .success { color: #28a745; }
        .error { color: #dc3545; }
        .metric { font-size: 48px; font-weight: bold; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
    </style>
</head>
<body>
    <h1>ThinkAI Test Results</h1>
    <div class="grid">
        <div class="card">
            <h2>Coverage</h2>
            <div class="metric ${COVERAGE >= $COVERAGE_THRESHOLD ? 'success' : 'error'}">${COVERAGE}%</div>
        </div>
        <div class="card">
            <h2>E2E Tests</h2>
            <div class="metric $([ $E2E_RESULT -eq 0 ] && echo "success" || echo "error")">
                $([ $E2E_RESULT -eq 0 ] && echo "✓ PASS" || echo "✗ FAIL")
            </div>
        </div>
        <div class="card">
            <h2>Integration Tests</h2>
            <div class="metric $([ $INTEGRATION_RESULT -eq 0 ] && echo "success" || echo "error")">
                $([ $INTEGRATION_RESULT -eq 0 ] && echo "✓ PASS" || echo "✗ FAIL")
            </div>
        </div>
        <div class="card">
            <h2>Last Run</h2>
            <p>$(date)</p>
        </div>
    </div>
</body>
</html>
EOF

echo -e "\n${GREEN}Test report available at: $TEST_RESULTS_DIR/dashboard.html${NC}"