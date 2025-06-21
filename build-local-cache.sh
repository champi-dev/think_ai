#!/bin/bash
# Elite Local Cache Builder for Railway Deployment
# Builds all dependencies locally and prepares them for Railway

set -euo pipefail

# Colors
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${PURPLE}🚀 Think AI Local Cache Builder${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Configuration
CACHE_DIR="railway-cache"
WHEELS_DIR="${CACHE_DIR}/wheels"
MODELS_DIR="${CACHE_DIR}/models"
MANIFESTS_DIR="${CACHE_DIR}/manifests"

# Clean previous cache
if [ -d "${CACHE_DIR}" ]; then
    echo -e "${YELLOW}⚠️  Removing existing cache...${NC}"
    rm -rf "${CACHE_DIR}"
fi

# Create cache structure
echo -e "${BLUE}📁 Creating cache directories...${NC}"
mkdir -p "${WHEELS_DIR}" "${MODELS_DIR}" "${MANIFESTS_DIR}"

# Build Python wheels with perfect compatibility
echo -e "\n${BLUE}🏗️  Building Python wheels...${NC}"

# Create a requirements hash for validation
REQUIREMENTS_HASH=$(sha256sum requirements-full.txt | cut -d' ' -f1)
echo "${REQUIREMENTS_HASH}" > "${MANIFESTS_DIR}/requirements.hash"

# Build wheels with platform compatibility
# Using manylinux for maximum compatibility
pip wheel -r requirements-full.txt \
    --wheel-dir="${WHEELS_DIR}" \
    --prefer-binary \
    --platform manylinux2014_x86_64 \
    --platform manylinux_2_17_x86_64 \
    --platform linux_x86_64 \
    --only-binary :all: 2>/dev/null || \
pip wheel -r requirements-full.txt \
    --wheel-dir="${WHEELS_DIR}" \
    --prefer-binary

# Special handling for PyTorch CPU
echo -e "${YELLOW}⚡ Building PyTorch CPU wheel...${NC}"
pip download torch==2.1.2 \
    --index-url https://download.pytorch.org/whl/cpu \
    --dest="${WHEELS_DIR}" \
    --platform manylinux2014_x86_64 \
    --only-binary :all: \
    --no-deps

# Download and cache AI models
echo -e "\n${BLUE}🧠 Pre-downloading AI models...${NC}"

# Create model download script
cat > "${CACHE_DIR}/download_models.py" << 'EOF'
import os
import sys
from pathlib import Path

# Set cache directory
cache_dir = Path("railway-cache/models")
os.environ["TRANSFORMERS_CACHE"] = str(cache_dir / "transformers")
os.environ["HF_HOME"] = str(cache_dir / "huggingface")
os.environ["SENTENCE_TRANSFORMERS_HOME"] = str(cache_dir / "sentence-transformers")

# Create directories
for dir in [cache_dir / "transformers", cache_dir / "huggingface", cache_dir / "sentence-transformers"]:
    dir.mkdir(parents=True, exist_ok=True)

try:
    from sentence_transformers import SentenceTransformer
    print("📥 Downloading all-MiniLM-L6-v2...")
    model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder=str(cache_dir / "sentence-transformers"))
    print("✅ Model downloaded successfully!")

    # Save model info
    with open(cache_dir / "models.manifest", "w") as f:
        f.write("all-MiniLM-L6-v2\n")

except Exception as e:
    print(f"⚠️  Model download skipped: {e}")
    sys.exit(0)  # Don't fail the build
EOF

python "${CACHE_DIR}/download_models.py" || echo "Model caching skipped"

# Create efficient installer script
echo -e "\n${BLUE}📝 Creating optimized installer...${NC}"

cat > "${CACHE_DIR}/install_from_cache.sh" << 'EOF'
#!/bin/bash
# O(1) Installation from pre-built cache

set -euo pipefail

CACHE_DIR="railway-cache"
WHEELS_DIR="${CACHE_DIR}/wheels"

# Verify cache integrity
if [ ! -f "${CACHE_DIR}/manifests/requirements.hash" ]; then
    echo "❌ Cache not found! Run build-local-cache.sh first"
    exit 1
fi

CURRENT_HASH=$(sha256sum requirements-full.txt | cut -d' ' -f1)
CACHED_HASH=$(cat "${CACHE_DIR}/manifests/requirements.hash")

if [ "${CURRENT_HASH}" != "${CACHED_HASH}" ]; then
    echo "⚠️  Requirements changed! Rebuilding cache..."
    exit 1
fi

# Install from wheels - O(1) performance
echo "⚡ Installing from pre-built wheels..."
pip install --find-links "${WHEELS_DIR}" \
    --no-index \
    --no-deps \
    -r requirements-full.txt || \
pip install --find-links "${WHEELS_DIR}" \
    --prefer-binary \
    -r requirements-full.txt

# Copy models to expected locations
if [ -d "${CACHE_DIR}/models" ]; then
    echo "📦 Restoring AI models..."
    mkdir -p ~/.cache
    cp -r "${CACHE_DIR}/models/huggingface" ~/.cache/ 2>/dev/null || true
    cp -r "${CACHE_DIR}/models/transformers" ~/.cache/ 2>/dev/null || true
    cp -r "${CACHE_DIR}/models/sentence-transformers" ~/.cache/ 2>/dev/null || true
fi

echo "✅ Installation complete!"
EOF

chmod +x "${CACHE_DIR}/install_from_cache.sh"

# Generate cache statistics
echo -e "\n${BLUE}📊 Generating cache report...${NC}"

WHEEL_COUNT=$(ls -1 ${WHEELS_DIR}/*.whl 2>/dev/null | wc -l || echo 0)
CACHE_SIZE=$(du -sh ${CACHE_DIR} | cut -f1)

cat > "${CACHE_DIR}/cache-report.md" << EOF
# Railway Cache Report

Generated: $(date)

## Cache Statistics
- **Wheels built**: ${WHEEL_COUNT}
- **Total size**: ${CACHE_SIZE}
- **Requirements hash**: ${REQUIREMENTS_HASH}

## Contents
### Python Wheels
$(ls -1 ${WHEELS_DIR}/*.whl 2>/dev/null | sed 's/.*\//- /' || echo "None")

### AI Models
$(ls -1 ${MODELS_DIR}/ 2>/dev/null | sed 's/^/- /' || echo "None")

## Usage
1. Commit this cache to your repository
2. In Railway, use: \`./railway-cache/install_from_cache.sh\`
EOF

# Create .gitattributes for Git LFS (large files)
echo -e "\n${BLUE}📝 Configuring Git LFS...${NC}"
cat > "${CACHE_DIR}/.gitattributes" << 'EOF'
# Git LFS for large wheels and models
*.whl filter=lfs diff=lfs merge=lfs -text
*.bin filter=lfs diff=lfs merge=lfs -text
*.safetensors filter=lfs diff=lfs merge=lfs -text
*.h5 filter=lfs diff=lfs merge=lfs -text
*.pt filter=lfs diff=lfs merge=lfs -text
*.pth filter=lfs diff=lfs merge=lfs -text
EOF

# Final report
echo -e "\n${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✨ Cache build complete!${NC}"
echo -e "${CYAN}📊 Summary:${NC}"
echo -e "  📦 Wheels built: ${WHEEL_COUNT}"
echo -e "  💾 Cache size: ${CACHE_SIZE}"
echo -e "  📁 Location: ${CACHE_DIR}/"
echo -e "\n${YELLOW}🚀 Next steps:${NC}"
echo -e "  1. Initialize Git LFS: ${CYAN}git lfs install${NC}"
echo -e "  2. Track cache: ${CYAN}git lfs track 'railway-cache/**/*.whl'${NC}"
echo -e "  3. Add to git: ${CYAN}git add railway-cache${NC}"
echo -e "  4. Commit: ${CYAN}git commit -m 'Add pre-built dependency cache'${NC}"
echo -e "  5. Push: ${CYAN}git push${NC}"
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
