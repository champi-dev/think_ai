#!/bin/bash
# Comprehensive test runner for Think AI
# This script runs all tests and ensures the system works as promised

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test results
TESTS_PASSED=0
TESTS_FAILED=0

# Function to print colored output
print_status() {
    local status=$1
    local message=$2
    
    if [ "$status" = "pass" ]; then
        echo -e "${GREEN}✅ $message${NC}"
        ((TESTS_PASSED++))
    elif [ "$status" = "fail" ]; then
        echo -e "${RED}❌ $message${NC}"
        ((TESTS_FAILED++))
    elif [ "$status" = "info" ]; then
        echo -e "${BLUE}ℹ️  $message${NC}"
    elif [ "$status" = "warn" ]; then
        echo -e "${YELLOW}⚠️  $message${NC}"
    fi
}

# Function to check prerequisites
check_prerequisites() {
    print_status "info" "Checking prerequisites..."
    
    # Check Rust
    if ! command -v cargo &> /dev/null; then
        print_status "fail" "Cargo not found. Please install Rust."
        exit 1
    fi
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_status "fail" "Python3 not found. Please install Python 3.8+."
        exit 1
    fi
    
    # Check Node.js (for frontend tests)
    if ! command -v node &> /dev/null; then
        print_status "warn" "Node.js not found. Frontend tests will be skipped."
    fi
    
    print_status "pass" "Prerequisites check completed"
}

# Function to setup test environment
setup_test_env() {
    print_status "info" "Setting up test environment..."
    
    # Create test directories
    mkdir -p test_data
    mkdir -p test_results
    
    # Install Python dependencies
    pip3 install -q pytest pytest-asyncio aiohttp toml playwright
    
    # Install Playwright browsers
    playwright install chromium --with-deps
    
    print_status "pass" "Test environment setup completed"
}

# Function to run Rust unit tests
run_rust_unit_tests() {
    print_status "info" "Running Rust unit tests..."
    
    if cargo test --lib --quiet; then
        print_status "pass" "Rust unit tests passed"
    else
        print_status "fail" "Rust unit tests failed"
    fi
}

# Function to run Rust integration tests
run_rust_integration_tests() {
    print_status "info" "Running Rust integration tests..."
    
    if cargo test --test '*' --quiet; then
        print_status "pass" "Rust integration tests passed"
    else
        print_status "fail" "Rust integration tests failed"
    fi
}

# Function to run Python tests
run_python_tests() {
    print_status "info" "Running Python tests..."
    
    # Run unit tests
    if python3 -m pytest tests/unit/ -q; then
        print_status "pass" "Python unit tests passed"
    else
        print_status "fail" "Python unit tests failed"
    fi
    
    # Run integration tests
    if python3 -m pytest tests/integration/ -q; then
        print_status "pass" "Python integration tests passed"
    else
        print_status "fail" "Python integration tests failed"
    fi
}

# Function to run E2E tests
run_e2e_tests() {
    print_status "info" "Running E2E tests..."
    
    # Start the server in background
    print_status "info" "Building and starting Think AI server..."
    cargo build --release --bin think-ai-full-production
    
    # Check if server is already running
    if ! curl -s http://localhost:3000/health > /dev/null 2>&1; then
        ./target/release/think-ai-full-production &
        SERVER_PID=$!
        
        # Wait for server to start
        for i in {1..30}; do
            if curl -s http://localhost:3000/health > /dev/null 2>&1; then
                break
            fi
            sleep 1
        done
    fi
    
    # Run E2E tests
    if python3 tests/e2e/test_full_system_e2e.py; then
        print_status "pass" "E2E tests passed"
    else
        print_status "fail" "E2E tests failed"
    fi
    
    # Stop server if we started it
    if [ ! -z "$SERVER_PID" ]; then
        kill $SERVER_PID 2>/dev/null || true
    fi
}

# Function to run performance tests
run_performance_tests() {
    print_status "info" "Running performance tests..."
    
    # Create a simple performance test
    cat > test_performance.py << 'EOF'
import asyncio
import aiohttp
import time
import statistics

async def measure_response_time():
    times = []
    async with aiohttp.ClientSession() as session:
        for i in range(10):
            start = time.time()
            async with session.post(
                "http://localhost:3000/api/chat",
                json={"message": f"Test message {i}"}
            ) as resp:
                await resp.json()
            times.append(time.time() - start)
    return times

async def main():
    times = await measure_response_time()
    avg_time = statistics.mean(times) * 1000
    p95_time = statistics.quantiles(times, n=20)[18] * 1000
    
    print(f"Average response time: {avg_time:.2f}ms")
    print(f"P95 response time: {p95_time:.2f}ms")
    
    # Check thresholds
    if avg_time < 1000 and p95_time < 2000:
        return 0
    return 1

if __name__ == "__main__":
    exit(asyncio.run(main()))
EOF
    
    if python3 test_performance.py; then
        print_status "pass" "Performance tests passed"
    else
        print_status "fail" "Performance tests failed"
    fi
    
    rm -f test_performance.py
}

# Function to run security tests
run_security_tests() {
    print_status "info" "Running security tests..."
    
    # Test for common vulnerabilities
    SECURITY_PASS=true
    
    # Test XSS protection
    if curl -s -X POST http://localhost:3000/api/chat \
        -H "Content-Type: application/json" \
        -d '{"message": "<script>alert(\"xss\")</script>"}' \
        | grep -q "400"; then
        print_status "pass" "XSS protection working"
    else
        print_status "fail" "XSS protection not working"
        SECURITY_PASS=false
    fi
    
    # Test SQL injection protection
    if curl -s -X POST http://localhost:3000/api/chat \
        -H "Content-Type: application/json" \
        -d '{"message": "\"; DROP TABLE users; --"}' \
        | grep -q "400"; then
        print_status "pass" "SQL injection protection working"
    else
        print_status "fail" "SQL injection protection not working"
        SECURITY_PASS=false
    fi
    
    if [ "$SECURITY_PASS" = true ]; then
        print_status "pass" "Security tests passed"
    else
        print_status "fail" "Security tests failed"
    fi
}

# Function to generate test report
generate_report() {
    print_status "info" "Generating test report..."
    
    REPORT_FILE="test_results/test_report_$(date +%Y%m%d_%H%M%S).txt"
    
    cat > "$REPORT_FILE" << EOF
Think AI Comprehensive Test Report
==================================
Date: $(date)
Total Tests Passed: $TESTS_PASSED
Total Tests Failed: $TESTS_FAILED

Test Categories:
- Rust Unit Tests: $([ $TESTS_FAILED -eq 0 ] && echo "PASSED" || echo "FAILED")
- Rust Integration Tests: $([ $TESTS_FAILED -eq 0 ] && echo "PASSED" || echo "FAILED")
- Python Tests: $([ $TESTS_FAILED -eq 0 ] && echo "PASSED" || echo "FAILED")
- E2E Tests: $([ $TESTS_FAILED -eq 0 ] && echo "PASSED" || echo "FAILED")
- Performance Tests: $([ $TESTS_FAILED -eq 0 ] && echo "PASSED" || echo "FAILED")
- Security Tests: $([ $TESTS_FAILED -eq 0 ] && echo "PASSED" || echo "FAILED")

Overall Status: $([ $TESTS_FAILED -eq 0 ] && echo "✅ ALL TESTS PASSED" || echo "❌ SOME TESTS FAILED")
EOF
    
    print_status "info" "Report saved to: $REPORT_FILE"
}

# Main execution
main() {
    echo "🚀 Think AI Comprehensive Test Suite"
    echo "===================================="
    
    # Change to project directory
    cd "$(dirname "$0")"
    
    # Run all test phases
    check_prerequisites
    setup_test_env
    run_rust_unit_tests
    run_rust_integration_tests
    run_python_tests
    run_e2e_tests
    run_performance_tests
    run_security_tests
    
    # Generate report
    generate_report
    
    # Print summary
    echo
    echo "===================================="
    echo "Test Summary"
    echo "===================================="
    echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
    echo -e "${RED}Failed: $TESTS_FAILED${NC}"
    echo
    
    if [ $TESTS_FAILED -eq 0 ]; then
        echo -e "${GREEN}✅ All tests passed! The system works as promised.${NC}"
        exit 0
    else
        echo -e "${RED}❌ Some tests failed. Please check the report for details.${NC}"
        exit 1
    fi
}

# Run main function
main