# Publishing Think AI to PyPI

## Prerequisites

1. Create accounts on:
   - PyPI: https://pypi.org/account/register/
   - TestPyPI: https://test.pypi.org/account/register/

2. Generate API tokens:
   - PyPI: https://pypi.org/manage/account/token/
   - TestPyPI: https://test.pypi.org/manage/account/token/

## Publishing Steps

### 1. Test on TestPyPI First (Recommended)

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ think-ai
```

### 2. Publish to PyPI

```bash
# Upload to PyPI
twine upload dist/*

# Or with API token (recommended)
twine upload dist/* -u __token__ -p pypi-YOUR-API-TOKEN-HERE
```

### 3. Install from PyPI

```bash
pip install think-ai
```

## Package Details

- **Package Name**: think-ai
- **Version**: 0.1.0
- **Description**: A self-improving AI system with distributed consciousness
- **Author**: Think AI Team
- **License**: MIT
- **Python**: >=3.8

## Command Line Tools

After installation, users will have access to:
- `think-ai` - Main CLI interface
- `think-ai-chat` - Interactive chat mode
- `think-ai-server` - Run as server
- `think-ai-tui` - Terminal UI

## Updating the Package

1. Update version in `pyproject.toml` and `think_ai/__init__.py`
2. Update CHANGELOG.md
3. Clean old builds: `rm -rf dist/ build/ *.egg-info`
4. Build new version: `python3 -m build`
5. Upload: `twine upload dist/*`

## Troubleshooting

- If package name is taken, update the name in `pyproject.toml`
- Check package at: https://pypi.org/project/think-ai/
- For issues with dependencies, consider using version ranges instead of pinned versions