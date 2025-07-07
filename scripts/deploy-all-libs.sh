#!/bin/bash
# Deploy All Libraries Script
# Deploys npm and PyPI packages with version bumps and full testing

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Load environment variables if .env exists
if [ -f "$PROJECT_ROOT/.env" ]; then
    echo "Loading environment variables from .env..."
    export $(grep -v '^#' "$PROJECT_ROOT/.env" | xargs)
fi

echo "📦 Think AI Library Deployment Pipeline"
echo "======================================="

# Function to bump version
bump_version() {
    local version_file=$1
    local current_version=$(grep -E '"version":|version = ' "$version_file" | sed -E 's/.*"([0-9]+\.[0-9]+\.[0-9]+)".*/\1/')
    
    if [ -z "$current_version" ]; then
        echo "Error: Could not find version in $version_file"
        return 1
    fi
    
    # Bump patch version
    IFS='.' read -r major minor patch <<< "$current_version"
    new_patch=$((patch + 1))
    new_version="$major.$minor.$new_patch"
    
    echo "$new_version"
}

# Deploy npm package
deploy_npm() {
    echo "🔷 Deploying npm package (thinkai-quantum)..."
    cd "$PROJECT_ROOT/think-ai-js"
    
    # Bump version
    current_version=$(node -p "require('./package.json').version")
    new_version=$(bump_version package.json)
    
    echo "  Current version: $current_version"
    echo "  New version: $new_version"
    
    # Update package.json version
    sed -i "s/\"version\": \"$current_version\"/\"version\": \"$new_version\"/" package.json
    
    # Build the package
    echo "  Building package..."
    npm run build
    
    # Run tests
    echo "  Running tests..."
    npm test
    
    # Publish to npm
    echo "  Publishing to npm..."
    if [ -z "$NPM_TOKEN" ]; then
        echo "Error: NPM_TOKEN environment variable not set"
        exit 1
    fi
    echo "//registry.npmjs.org/:_authToken=$NPM_TOKEN" > ~/.npmrc
    npm publish --access public
    rm -f ~/.npmrc
    
    echo "✅ npm package deployed successfully!"
}

# Deploy PyPI package
deploy_pypi() {
    echo "🐍 Deploying PyPI package (thinkai-quantum)..."
    cd "$PROJECT_ROOT/think-ai-py"
    
    # Bump version
    current_version=$(grep "version = " pyproject.toml | sed 's/version = "\(.*\)"/\1/')
    new_version=$(bump_version pyproject.toml)
    
    echo "  Current version: $current_version"
    echo "  New version: $new_version"
    
    # Update pyproject.toml version
    sed -i "s/version = \"$current_version\"/version = \"$new_version\"/" pyproject.toml
    
    # Clean previous builds
    rm -rf dist/ build/ *.egg-info/
    
    # Build the package
    echo "  Building package..."
    python3 -m build
    
    # Run tests
    echo "  Running tests..."
    python3 -m pytest tests/ -v
    
    # Upload to PyPI
    echo "  Publishing to PyPI..."
    if [ -z "$PYPI_TOKEN" ]; then
        echo "Error: PYPI_TOKEN environment variable not set"
        exit 1
    fi
    python3 -m twine upload dist/* -u __token__ -p "$PYPI_TOKEN"
    
    echo "✅ PyPI package deployed successfully!"
}

# Test npm package
test_npm_package() {
    echo "🧪 Testing npm package installation..."
    
    # Create temporary directory
    temp_dir=$(mktemp -d)
    cd "$temp_dir"
    
    # Install and test
    echo "  Installing thinkai-quantum from npm..."
    npm install thinkai-quantum@latest
    
    # Test CLI
    echo "  Testing CLI..."
    npx thinkai-quantum --version
    
    # Cleanup
    cd -
    rm -rf "$temp_dir"
    
    echo "✅ npm package test passed!"
}

# Test PyPI package
test_pypi_package() {
    echo "🧪 Testing PyPI package installation..."
    
    # Create virtual environment
    temp_dir=$(mktemp -d)
    cd "$temp_dir"
    python3 -m venv test_env
    source test_env/bin/activate
    
    # Install and test
    echo "  Installing thinkai-quantum from PyPI..."
    pip install thinkai-quantum --upgrade
    
    # Test CLI
    echo "  Testing CLI..."
    think-ai --version
    
    # Cleanup
    deactivate
    cd -
    rm -rf "$temp_dir"
    
    echo "✅ PyPI package test passed!"
}

# Test full system
test_full_system() {
    echo "🔍 Testing full system capabilities..."
    cd "$PROJECT_ROOT"
    
    # Build release binaries
    echo "  Building Rust binaries..."
    cargo build --release
    
    # Test CLI
    echo "  Testing Think AI CLI..."
    ./target/release/think-ai --version
    
    # Test that server can start (but kill it immediately)
    echo "  Testing server startup..."
    timeout 5s ./target/release/think-ai server || true
    
    # Run integration tests
    echo "  Running integration tests..."
    cargo test --all
    
    echo "✅ Full system test passed!"
}

# Main deployment flow
main() {
    # Check for required tools
    command -v npm >/dev/null 2>&1 || { echo "npm is required but not installed."; exit 1; }
    command -v python3 >/dev/null 2>&1 || { echo "python3 is required but not installed."; exit 1; }
    command -v cargo >/dev/null 2>&1 || { echo "cargo is required but not installed."; exit 1; }
    
    # Deploy libraries
    deploy_npm
    deploy_pypi
    
    # Wait a bit for packages to be available
    echo "⏳ Waiting for packages to be available..."
    sleep 30
    
    # Test deployments
    test_npm_package
    test_pypi_package
    
    # Test full system
    test_full_system
    
    echo "🎉 All deployments completed successfully!"
    echo "   npm: thinkai-quantum v$(cd "$PROJECT_ROOT/think-ai-js" && node -p "require('./package.json').version")"
    echo "   PyPI: thinkai-quantum v$(cd "$PROJECT_ROOT/think-ai-py" && grep "version = " pyproject.toml | sed 's/version = "\(.*\)"/\1/')"
}

# Run main function
main "$@"