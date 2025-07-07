# Think AI Pre-commit Workflow

## Overview

The Think AI project uses a comprehensive pre-commit hook to ensure code quality, test coverage, and deployment readiness before any code is committed. This workflow automates the entire quality assurance process.

## What the Pre-commit Hook Does

When you run `git commit`, the following checks are automatically performed:

### 1. **Rust Code Quality**
- **Formatting**: Ensures all Rust code follows standard formatting (`cargo fmt`)
- **Linting**: Checks for common mistakes and enforces best practices (`cargo clippy`)
- **Unit Tests**: Runs all unit tests across the codebase
- **Integration Tests**: Executes integration test suites

### 2. **Build Verification**
- **Release Build**: Compiles the full release binary to catch compilation errors
- **Docker Build**: Simulates Railway deployment by building the Docker image
- **Performance**: Quick benchmark to ensure O(1) performance guarantees

### 3. **Library Preparation**
- **JavaScript Build**: Compiles TypeScript and prepares npm package
- **Python Build**: Creates wheel and source distributions for PyPI
- **Local Testing**: Verifies both CLIs work correctly

### 4. **Security Checks**
- **Secret Scanning**: Searches for API keys, tokens, and passwords in staged files
- **Dependency Audit**: Checks for known vulnerabilities (when applicable)

## Usage

### Basic Workflow

```bash
# Make your changes
vim src/main.rs

# Stage changes
git add .

# Commit - this triggers all checks automatically
git commit -m "feat: Add O(1) hash-based search"

# If all checks pass, commit succeeds
# If any check fails, commit is blocked
```

### Testing Without Committing

```bash
# Run all pre-commit checks without making a commit
./pre-commit-test.sh
```

### Bypassing Checks (NOT Recommended)

```bash
# Only use in emergencies
git commit --no-verify -m "emergency fix"
```

## Automatic Deployment

Enable automatic library deployment after successful commits:

```bash
# Set environment variables
export THINK_AI_AUTO_DEPLOY=true
export PYPI_TOKEN="your-pypi-token"
export NPM_TOKEN="your-npm-token"

# Now commits will auto-deploy on success
git commit -m "feat: New O(1) algorithm"
```

## Manual Deployment After Checks

If you prefer to deploy manually after commits:

```bash
# Run deployment script
./deploy-after-checks.sh

# Or force deployment without checks
./deploy-after-checks.sh --force
```

## Configuration

### Environment Variables

- `THINK_AI_AUTO_DEPLOY`: Set to `true` to enable automatic deployment
- `PYPI_TOKEN`: Your PyPI API token for Python package deployment
- `NPM_TOKEN`: Your npm API token for JavaScript package deployment

### Customizing Checks

Edit `.git/hooks/pre-commit` to modify which checks run or add new ones.

## Performance Impact

The full pre-commit check suite typically takes:
- Rust formatting: ~2 seconds
- Rust linting: ~10 seconds
- Unit tests: ~5 seconds
- Integration tests: ~10 seconds
- Docker build: ~30 seconds
- Library builds: ~5 seconds
- **Total**: ~1 minute

## Troubleshooting

### Common Issues

1. **Rust formatting fails**
   ```bash
   cargo fmt
   git add -u
   git commit
   ```

2. **Clippy warnings**
   ```bash
   cargo clippy --fix
   git add -u
   git commit
   ```

3. **Tests failing**
   ```bash
   cargo test -- --nocapture
   # Fix the failing tests
   ```

4. **Docker build fails**
   ```bash
   # Check Docker daemon is running
   docker info
   
   # Review Dockerfile for issues
   docker build -t think-ai-test .
   ```

5. **Secret detected**
   ```bash
   # Remove the secret from your code
   # Use environment variables instead
   ```

### Logs

Check these log files for detailed error information:
- `/tmp/docker-build.log` - Docker build output
- `/tmp/python-build.log` - Python package build output
- `/tmp/pypi-deploy.log` - PyPI deployment logs
- `/tmp/npm-deploy.log` - npm deployment logs

## Best Practices

1. **Run checks early**: Use `./pre-commit-test.sh` before staging changes
2. **Fix incrementally**: Address one type of issue at a time
3. **Keep commits focused**: Smaller commits = faster checks
4. **Update versions**: The hook doesn't auto-increment versions
5. **Test locally first**: Ensure your changes work before committing

## Benefits

- **Consistent Code Quality**: Every commit meets the same high standards
- **Fewer Broken Builds**: Catch issues before they reach the repository
- **Automated Deployment**: Ship faster with confidence
- **Security**: Prevent accidental secret commits
- **Performance Guarantees**: Ensure O(1) complexity is maintained

## Integration with CI/CD

While the pre-commit hook runs locally, it complements our CI/CD pipeline:
- Local checks catch issues early
- CI/CD provides additional validation
- Railway deployment only receives tested code

---

Remember: The pre-commit hook is your friend! It saves time by catching issues early and ensures our codebase maintains its O(1) performance standards.