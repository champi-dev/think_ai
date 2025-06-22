# Think AI v3.1.0 Git Hooks

Automated quality assurance and deployment preparation hooks.

## Installation

```bash
./install_hooks.sh
```

## Pre-Commit Hook

Runs before every commit to ensure code quality:

1. **Code Formatting** (if tools available)
   - `black` - Python code formatter
   - `isort` - Import sorting
   - `ruff` - Fast Python linter

2. **Syntax Validation**
   - Checks all Python files compile correctly
   - No syntax errors allowed

3. **Test Suite**
   - Runs comprehensive test suite
   - Tests core functionality:
     - Imports and dependencies
     - Configuration system
     - Consciousness framework
     - Ethics/Constitutional AI
     - O(1) storage operations
     - Language model integration
     - API endpoints
     - Performance requirements
     - Colombian mode features

### Skip Pre-Commit

```bash
git commit --no-verify -m "Emergency fix"
```

## Pre-Push Hook

Prepares complete deployment bundle before pushing:

1. **Requirements Management**
   - Updates all requirements files
   - Creates minimal requirements for Railway
   - Generates complete dependency list

2. **Python Package**
   - Creates wheel distribution
   - Packages as installable library

3. **Webapp Bundle**
   - Builds Next.js production bundle
   - Creates compressed archive

4. **Docker Preparation**
   - Lists all Docker configurations
   - Creates build instructions

5. **Deployment Scripts**
   - Railway deployment script
   - Docker deployment script
   - Manual deployment instructions

6. **Deployment Manifest**
   - Version information
   - Git commit/branch
   - Component listing
   - Endpoint documentation

7. **Final Bundle**
   - Complete deployment package
   - All necessary files included
   - Timestamped archive

### Skip Pre-Push

```bash
git push --no-verify
```

## Files Created

### By Pre-Commit
- Formatted Python files
- Test results

### By Pre-Push
- `think_ai_v3/requirements-all.txt` - Complete requirements
- `think_ai_v3/requirements-minimal.txt` - Minimal deployment
- `think_ai_v3/requirements-railway.txt` - Railway optimized
- `dist/think_ai-3.1.0-py3-none-any.whl` - Python wheel
- `webapp_bundle.tar.gz` - Webapp bundle
- `DOCKER_IMAGES.md` - Docker documentation
- `deploy_railway.sh` - Railway deploy script
- `deploy_docker.sh` - Docker deploy script
- `DEPLOYMENT_MANIFEST.json` - Deployment metadata
- `think_ai_v3.1.0_deployment_*.tar.gz` - Complete bundle

## Testing Hooks

### Test Pre-Commit
```bash
# Make a small change
echo "# test" >> README.md
git add README.md
git commit -m "Test commit"
```

### Test Pre-Push
```bash
# Create test branch
git checkout -b test-hooks
git push origin test-hooks
```

## Troubleshooting

### Missing Tools
Install development dependencies:
```bash
pip install black isort ruff pytest
```

### Slow Tests
The test suite should complete in < 10 seconds. If slower:
- Check network connectivity (model downloads)
- Ensure no heavy models are loading
- Run with mock models for testing

### Hook Failures
1. Check error messages for specific failures
2. Run tests manually: `python think_ai_v3/tests/test_full_suite.py`
3. Fix issues and retry
4. Use `--no-verify` only for emergencies

## Configuration

### Custom Test Suite
Edit `think_ai_v3/tests/test_full_suite.py` to add/modify tests.

### Formatting Rules
- Line length: 100 characters
- Import sorting: black-compatible
- See `pyproject.toml` for detailed configuration

## Performance

- Pre-commit: ~5-10 seconds
- Pre-push: ~30-60 seconds (includes builds)

Both hooks are optimized for speed while maintaining quality.