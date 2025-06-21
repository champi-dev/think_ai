#!/bin/bash
# Elite Library Deployment Script
# Publishes all Think AI packages to npm and PyPI

set -euo pipefail

# Colors
PURPLE='\033[0;35m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${PURPLE}🚀 Think AI Library Deployment System${NC}"
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Check for required tools
check_requirements() {
    echo -e "\n${BLUE}🔍 Checking requirements...${NC}"
    
    local missing=0
    
    # Python tools
    if ! command -v twine &> /dev/null; then
        echo -e "${RED}❌ twine not found. Install with: pip install twine${NC}"
        missing=1
    fi
    
    # Node tools
    if ! command -v npm &> /dev/null; then
        echo -e "${RED}❌ npm not found${NC}"
        missing=1
    fi
    
    # Check authentication
    if [ -z "${PYPI_TOKEN:-}" ] && [ ! -f ~/.pypirc ]; then
        echo -e "${YELLOW}⚠️  PyPI credentials not found. Set PYPI_TOKEN or configure ~/.pypirc${NC}"
    fi
    
    if ! npm whoami &> /dev/null; then
        echo -e "${YELLOW}⚠️  Not logged in to npm. Run: npm login${NC}"
    fi
    
    if [ $missing -eq 1 ]; then
        exit 1
    fi
    
    echo -e "${GREEN}✅ All requirements met${NC}"
}

# Deploy Python packages
deploy_python() {
    echo -e "\n${BLUE}🐍 Deploying Python packages...${NC}"
    
    # 1. think-ai main package
    if [ -f "setup.py" ]; then
        echo -e "${YELLOW}📦 Building think-ai...${NC}"
        python setup.py sdist bdist_wheel
        
        if [ "${DRY_RUN:-false}" = "true" ]; then
            echo -e "${YELLOW}[DRY RUN] Would upload to PyPI${NC}"
        else
            echo -e "${YELLOW}📤 Uploading to PyPI...${NC}"
            twine upload dist/* --skip-existing
        fi
        echo -e "${GREEN}✅ think-ai deployed${NC}"
    fi
    
    # 2. think-ai-cli
    if [ -d "think-ai-cli/python" ]; then
        cd think-ai-cli/python
        echo -e "${YELLOW}📦 Building think-ai-cli...${NC}"
        python setup.py sdist bdist_wheel
        
        if [ "${DRY_RUN:-false}" = "true" ]; then
            echo -e "${YELLOW}[DRY RUN] Would upload to PyPI${NC}"
        else
            twine upload dist/* --skip-existing
        fi
        cd ../..
        echo -e "${GREEN}✅ think-ai-cli deployed${NC}"
    fi
    
    # 3. o1-vector-search
    if [ -d "o1-python" ]; then
        cd o1-python
        echo -e "${YELLOW}📦 Building o1-vector-search...${NC}"
        python setup.py sdist bdist_wheel
        
        if [ "${DRY_RUN:-false}" = "true" ]; then
            echo -e "${YELLOW}[DRY RUN] Would upload to PyPI${NC}"
        else
            twine upload dist/* --skip-existing
        fi
        cd ..
        echo -e "${GREEN}✅ o1-vector-search deployed${NC}"
    fi
}

# Deploy JavaScript packages
deploy_javascript() {
    echo -e "\n${BLUE}📦 Deploying JavaScript packages...${NC}"
    
    # 1. think-ai npm package
    if [ -d "npm" ] && [ -f "npm/package.json" ]; then
        cd npm
        echo -e "${YELLOW}📦 Building think-ai npm package...${NC}"
        npm run build
        
        # Update version if needed
        CURRENT_VERSION=$(node -p "require('./package.json').version")
        echo -e "${BLUE}Current version: ${CURRENT_VERSION}${NC}"
        
        if [ "${DRY_RUN:-false}" = "true" ]; then
            echo -e "${YELLOW}[DRY RUN] Would publish to npm${NC}"
            npm pack
        else
            echo -e "${YELLOW}📤 Publishing to npm...${NC}"
            npm publish --access public
        fi
        cd ..
        echo -e "${GREEN}✅ think-ai npm package deployed${NC}"
    fi
    
    # 2. think-ai-cli npm
    if [ -d "think-ai-cli/nodejs" ] && [ -f "think-ai-cli/nodejs/package.json" ]; then
        cd think-ai-cli/nodejs
        echo -e "${YELLOW}📦 Building think-ai-cli...${NC}"
        npm run build
        
        if [ "${DRY_RUN:-false}" = "true" ]; then
            echo -e "${YELLOW}[DRY RUN] Would publish to npm${NC}"
            npm pack
        else
            npm publish --access public
        fi
        cd ../..
        echo -e "${GREEN}✅ think-ai-cli npm deployed${NC}"
    fi
    
    # 3. o1-js package
    if [ -d "o1-js" ] && [ -f "o1-js/package.json" ]; then
        cd o1-js
        echo -e "${YELLOW}📦 Building o1-js...${NC}"
        npm run build
        
        if [ "${DRY_RUN:-false}" = "true" ]; then
            echo -e "${YELLOW}[DRY RUN] Would publish to npm${NC}"
            npm pack
        else
            npm publish --access public
        fi
        cd ..
        echo -e "${GREEN}✅ o1-js deployed${NC}"
    fi
}

# Version management
bump_version() {
    local package=$1
    local bump_type=${2:-patch}  # patch, minor, major
    
    echo -e "${YELLOW}📝 Bumping ${package} version (${bump_type})...${NC}"
    
    case $package in
        "all")
            # Bump all packages
            npm version $bump_type --no-git-tag-version 2>/dev/null || true
            ;;
        "python")
            # Update setup.py version
            echo "Manual version update needed in setup.py"
            ;;
        "npm")
            cd npm && npm version $bump_type --no-git-tag-version && cd ..
            ;;
    esac
}

# Main deployment flow
main() {
    # Parse arguments
    DRY_RUN=false
    DEPLOY_PYTHON=true
    DEPLOY_JS=true
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                DRY_RUN=true
                echo -e "${YELLOW}🔍 DRY RUN MODE${NC}"
                shift
                ;;
            --python-only)
                DEPLOY_JS=false
                shift
                ;;
            --js-only)
                DEPLOY_PYTHON=false
                shift
                ;;
            --bump)
                bump_version "${2:-all}" "${3:-patch}"
                shift 3
                ;;
            *)
                echo "Unknown option: $1"
                echo "Usage: $0 [--dry-run] [--python-only|--js-only] [--bump package version]"
                exit 1
                ;;
        esac
    done
    
    # Check requirements
    check_requirements
    
    # Clean previous builds
    echo -e "\n${BLUE}🧹 Cleaning previous builds...${NC}"
    rm -rf dist build *.egg-info
    find . -type d -name "dist" -not -path "./node_modules/*" -exec rm -rf {} + 2>/dev/null || true
    
    # Deploy packages
    if [ "$DEPLOY_PYTHON" = true ]; then
        deploy_python
    fi
    
    if [ "$DEPLOY_JS" = true ]; then
        deploy_javascript
    fi
    
    # Summary
    echo -e "\n${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}✨ Deployment complete!${NC}"
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    if [ "$DRY_RUN" = true ]; then
        echo -e "${YELLOW}This was a dry run. No packages were actually published.${NC}"
        echo -e "${BLUE}Remove --dry-run flag to deploy for real.${NC}"
    else
        echo -e "\n${BLUE}📦 Published packages:${NC}"
        echo -e "  Python: ${GREEN}think-ai, think-ai-cli, o1-vector-search${NC}"
        echo -e "  NPM: ${GREEN}think-ai, think-ai-cli, o1-js${NC}"
        echo -e "\n${YELLOW}🔗 View at:${NC}"
        echo -e "  https://pypi.org/project/think-ai/"
        echo -e "  https://www.npmjs.com/package/think-ai"
    fi
}

# Run main function
main "$@"