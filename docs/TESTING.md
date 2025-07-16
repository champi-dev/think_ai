# 🧪 Think AI Testing Infrastructure

This document describes the comprehensive testing infrastructure for Think AI, ensuring 100% code coverage and reliability.

## 📋 Overview

Our testing infrastructure includes:
- **Unit Tests**: Testing individual components in isolation
- **Integration Tests**: Testing component interactions
- **E2E Tests**: Testing complete user workflows
- **Coverage Reports**: Tracking test coverage metrics
- **Periodic Testing**: Automated background test runs
- **Pre-commit Hooks**: Ensuring code quality before commits

## 🚀 Quick Start

### Running All Tests
```bash
npm test
```

### Running Specific Test Suites
```bash
# Backend tests only
npm run test:backend

# Frontend tests only
npm run test:frontend

# E2E tests only
npm run test:e2e

# Watch mode for development
npm run test:watch
```

## 🔍 Test Structure

### Backend Tests (Rust)
Located in `full-system/tests/`:
- `unit_tests.rs`: Unit tests for individual functions and modules
- `integration_tests.rs`: Integration tests for API endpoints
- `mod.rs`: Test module organization

### Frontend Tests (React)
Located in `frontend/src/`:
- `App.test.jsx`: Component unit tests (642 lines, 100% coverage)
- `App.integration.test.jsx`: Integration tests with MSW
- `test-setup.js`: Test environment configuration

### E2E Tests (Playwright)
Located in `tests/`:
- `e2e-full-flow.spec.js`: Complete user journey tests
- `e2e-edge-cases.spec.js`: Edge case and error handling tests
- `e2e-responsiveness.spec.js`: Responsive design tests

## 📊 Coverage Reports

### Generating Coverage Reports
```bash
# Generate all coverage reports
npm run coverage

# Backend coverage only
npm run test:backend:coverage

# Frontend coverage only
npm run test:frontend:coverage
```

### Viewing Coverage Reports
Coverage reports are generated in the `coverage/` directory:
- `coverage/combined/index.html`: Combined coverage report
- `coverage/backend/tarpaulin-report.html`: Rust backend coverage
- `coverage/frontend/index.html`: React frontend coverage

### Coverage Requirements
- **Target**: 100% coverage for all metrics
- **Minimum**: 90% for CI/CD to pass
- **Metrics**: Statements, Branches, Functions, Lines

## 🔄 Periodic Test Runner

The periodic test runner automatically executes all test suites at regular intervals.

### Starting the Test Runner
```bash
# Run in foreground
npm run test:periodic

# Run as daemon
node scripts/periodic-test-runner.js --daemon
```

### Installing as System Service
```bash
# Copy service file
sudo cp scripts/periodic-test-runner.service /etc/systemd/system/think-ai-tests.service

# Enable and start service
sudo systemctl enable think-ai-tests
sudo systemctl start think-ai-tests

# Check status
sudo systemctl status think-ai-tests
```

### Configuration
Environment variables:
- `TEST_INTERVAL`: Test run interval in milliseconds (default: 30 minutes)
- `NOTIFY_ON_FAILURE`: Enable failure notifications (default: false)

## 🪝 Pre-commit Hooks

Pre-commit hooks ensure code quality before commits.

### Setup
```bash
# Install husky
npx husky install

# The pre-commit hook is already configured in .husky/pre-commit
```

### Checks Performed
1. Rust formatting (cargo fmt)
2. Rust linting (cargo clippy)
3. Frontend linting (ESLint)
4. Frontend type checking (TypeScript)
5. Backend unit tests
6. Frontend unit tests

### Bypassing Hooks (Emergency Only)
```bash
git commit --no-verify -m "Emergency fix"
```

## 🧪 Writing Tests

### Backend Test Example
```rust
#[tokio::test]
async fn test_chat_endpoint() {
    let app = create_test_app().await;
    
    let response = app
        .oneshot(
            Request::builder()
                .method("POST")
                .uri("/api/chat")
                .header("content-type", "application/json")
                .body(Body::from(json!({"message": "Hello"}).to_string()))
                .unwrap(),
        )
        .await
        .unwrap();
        
    assert_eq!(response.status(), StatusCode::OK);
}
```

### Frontend Test Example
```jsx
test('sends message on button click', async () => {
  const user = userEvent.setup();
  render(<App />);
  
  const input = screen.getByPlaceholderText('Type your message here...');
  const sendButton = screen.getByText('Send');
  
  await user.type(input, 'Hello AI');
  await user.click(sendButton);
  
  await waitFor(() => {
    expect(screen.getByText('Hello AI')).toBeInTheDocument();
  });
});
```

### E2E Test Example
```javascript
test('complete user journey', async ({ page }) => {
  await page.goto('http://localhost:8080');
  
  await page.fill('input[placeholder="Type your message here..."]', 'Hello');
  await page.click('button:has-text("Send")');
  
  await expect(page.locator('.message.user')).toContainText('Hello');
  await expect(page.locator('.message.assistant')).toBeVisible();
});
```

## 🎯 Best Practices

1. **Test Isolation**: Each test should be independent
2. **Clear Names**: Use descriptive test names
3. **Arrange-Act-Assert**: Follow AAA pattern
4. **Mock External Dependencies**: Use MSW for API mocking
5. **Test User Behavior**: Focus on user interactions, not implementation
6. **Accessibility**: Include accessibility tests
7. **Performance**: Test performance-critical paths

## 🐛 Debugging Tests

### Backend Tests
```bash
# Run with verbose output
RUST_LOG=debug cargo test -- --nocapture

# Run specific test
cargo test test_chat_endpoint -- --exact
```

### Frontend Tests
```bash
# Run in watch mode with UI
npm run test:watch

# Debug specific test
npm test -- App.test.jsx -t "sends message"
```

### E2E Tests
```bash
# Run with UI mode
npm run test:e2e:ui

# Debug mode
npm run test:e2e:debug

# Generate trace on failure
PWDEBUG=1 npm run test:e2e
```

## 📈 CI/CD Integration

Tests run automatically on:
- Every push to main/develop branches
- Every pull request
- Scheduled nightly runs

GitHub Actions workflow: `.github/workflows/ci.yml`

## 🚨 Troubleshooting

### Common Issues

1. **Tests timing out**
   - Increase timeout in test configuration
   - Check for unresolved promises

2. **Coverage not reaching 100%**
   - Check for unreachable code
   - Add tests for error cases
   - Verify all branches are covered

3. **Flaky tests**
   - Add proper waitFor conditions
   - Avoid hardcoded timeouts
   - Use data-testid for reliable selectors

4. **Port conflicts**
   - Ensure ports 8080 and others are free
   - Use dynamic port allocation in tests

## 📞 Support

For test-related issues:
1. Check test output for specific errors
2. Review this documentation
3. Check CI logs if tests pass locally but fail in CI
4. Open an issue with test logs and reproduction steps