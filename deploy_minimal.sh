#!/bin/bash

echo "🚀 Creating minimal Railway deployment..."

# Create minimal deployment directory
DEPLOY_DIR="/tmp/think_ai_minimal"
rm -rf "$DEPLOY_DIR"
mkdir -p "$DEPLOY_DIR"

# Copy only essential files
echo "Copying essential files..."
cp Cargo.toml Cargo.lock "$DEPLOY_DIR/"
cp nixpacks.toml "$DEPLOY_DIR/"
cp Dockerfile "$DEPLOY_DIR/"
cp minimal_3d.html "$DEPLOY_DIR/"

# Copy all think-ai source directories (without target/)
echo "Copying source code..."
for dir in think-ai-*; do
    if [ -d "$dir" ]; then
        cp -r "$dir" "$DEPLOY_DIR/"
        # Remove any target directories in subdirs
        find "$DEPLOY_DIR/$dir" -name "target" -type d -exec rm -rf {} + 2>/dev/null || true
    fi
done

# Create .railwayignore for the deployment
cat > "$DEPLOY_DIR/.railwayignore" << 'EOF'
# Ignore build artifacts
target/
.cargo/

# Ignore large files
*.log
*.tmp

# Keep only source code and configs
EOF

echo "Deployment directory created at: $DEPLOY_DIR"
echo "Size: $(du -sh "$DEPLOY_DIR" | cut -f1)"
echo ""
echo "To deploy:"
echo "1. cd $DEPLOY_DIR"
echo "2. railway login"
echo "3. railway up"
echo ""
echo "Or run: cd $DEPLOY_DIR && railway up"