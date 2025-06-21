#!/bin/bash
# Lightweight cache builder for Railway (without Git LFS)
# Creates a minimal cache with just the essential heavy dependencies

set -euo pipefail

PURPLE='\033[0;35m'
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${PURPLE}🚀 Railway Quick Cache Builder${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Create lightweight cache
CACHE_DIR=".railway-wheels"
mkdir -p "${CACHE_DIR}"

# Only cache the largest/slowest dependencies
echo -e "${YELLOW}📦 Building essential wheels only...${NC}"

# List of heavy dependencies to pre-build
HEAVY_DEPS=(
    "torch==2.1.2"
    "transformers==4.36.2"
    "sentence-transformers==2.2.2"
    "numpy==1.24.3"
    "pandas==2.0.3"
    "scikit-learn==1.3.2"
    "faiss-cpu==1.7.4"
)

# Build wheels for heavy dependencies
for dep in "${HEAVY_DEPS[@]}"; do
    echo -e "  Building ${dep}..."
    if [[ "$dep" == "torch==2.1.2" ]]; then
        pip wheel "$dep" --index-url https://download.pytorch.org/whl/cpu \
            --wheel-dir="${CACHE_DIR}" --no-deps --quiet || true
    else
        pip wheel "$dep" --wheel-dir="${CACHE_DIR}" --no-deps --quiet || true
    fi
done

# Create simple installer
cat > "${CACHE_DIR}/quick-install.sh" << 'EOF'
#!/bin/bash
# Quick install from partial cache

# Install heavy deps from cache
pip install --find-links .railway-wheels \
    torch==2.1.2 \
    transformers==4.36.2 \
    sentence-transformers==2.2.2 \
    numpy==1.24.3 \
    pandas==2.0.3 \
    scikit-learn==1.3.2 \
    faiss-cpu==1.7.4 \
    --no-index 2>/dev/null || echo "Some cached installs failed"

# Install remaining deps normally
pip install -r requirements-full.txt
EOF

chmod +x "${CACHE_DIR}/quick-install.sh"

# Update nixpacks to use quick cache
cat > "nixpacks-quick-cache.toml" << 'EOF'
[phases.setup]
nixPkgs = ["python311", "gcc", "python311Packages.pip", "python311Packages.virtualenv", "git"]

[phases.install]
cmds = [
    "python3 -m venv /opt/venv",
    ". /opt/venv/bin/activate && pip install --upgrade pip setuptools wheel",
    '''
    if [ -f ".railway-wheels/quick-install.sh" ]; then
        echo "⚡ Using quick cache for heavy dependencies"
        . /opt/venv/bin/activate && ./.railway-wheels/quick-install.sh
    else
        echo "📦 Standard installation"
        . /opt/venv/bin/activate && pip install -r requirements-full.txt
    fi
    '''
]

[phases.build]
cmds = [
    "echo 'Setting up Think AI directories...'",
    "mkdir -p /tmp/think_ai/models",
    "mkdir -p /tmp/think_ai/cache",
    "mkdir -p /tmp/think_ai/data"
]

[start]
cmd = "/opt/venv/bin/python -u think_ai_full.py"
EOF

# Report
CACHE_SIZE=$(du -sh ${CACHE_DIR} | cut -f1)
WHEEL_COUNT=$(ls -1 ${CACHE_DIR}/*.whl 2>/dev/null | wc -l || echo 0)

echo -e "\n${GREEN}✅ Quick cache built!${NC}"
echo -e "  📦 Wheels: ${WHEEL_COUNT}"
echo -e "  💾 Size: ${CACHE_SIZE}"
echo -e "\n${YELLOW}To use:${NC}"
echo -e "  1. ${CYAN}cp nixpacks-quick-cache.toml nixpacks.toml${NC}"
echo -e "  2. ${CYAN}git add .railway-wheels nixpacks.toml${NC}"
echo -e "  3. ${CYAN}git commit -m 'Add quick cache for heavy deps'${NC}"
echo -e "  4. ${CYAN}git push${NC}"
