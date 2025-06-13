#!/bin/bash
# Run all tests with coverage

echo "🧪 Running Think AI Test Suite..."
echo "================================"

# Check if pytest is installed
if ! python -m pytest --version &> /dev/null; then
    echo "⚠️  pytest not found. Installing test dependencies..."
    pip install -e ".[dev]"
fi

# Run unit tests
echo ""
echo "🔬 Running Unit Tests..."
python -m pytest tests/unit/ -v --cov=. --cov-report=term-missing --cov-report=html

# Run integration tests
echo ""
echo "🔗 Running Integration Tests..."
python -m pytest tests/integration/ -v --cov=. --cov-report=term-missing --cov-append

# Generate coverage report
echo ""
echo "📊 Test Coverage Report:"
python -m pytest --cov=. --cov-report=term

# Check coverage threshold
coverage_percent=$(python -m pytest --cov=. --cov-report=term | grep TOTAL | awk '{print $4}' | sed 's/%//')

if [ ! -z "$coverage_percent" ]; then
    if (( $(echo "$coverage_percent < 80" | bc -l) )); then
        echo ""
        echo "⚠️  Warning: Test coverage is below 80% ($coverage_percent%)"
        echo "Please add more tests to improve coverage."
    else
        echo ""
        echo "✅ Excellent! Test coverage is $coverage_percent%"
    fi
fi

echo ""
echo "📝 HTML coverage report generated in htmlcov/index.html"