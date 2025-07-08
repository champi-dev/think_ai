#!/bin/bash

# Setup script for Think AI Image Generation

echo "🎨 Think AI Image Generation Setup"
echo "================================="
echo ""

# Check if .env already exists
if [ -f .env ]; then
    echo "⚠️  .env file already exists. Backing up to .env.backup"
    cp .env .env.backup
fi

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    touch .env
fi

# Function to update or add environment variable
update_env() {
    local key=$1
    local value=$2
    
    if grep -q "^${key}=" .env; then
        # Update existing key
        sed -i.bak "s|^${key}=.*|${key}=${value}|" .env
    else
        # Add new key
        echo "${key}=${value}" >> .env
    fi
}

# Ask for Leonardo AI API key
echo "Please enter your Leonardo AI API key:"
echo "(You can get one from https://leonardo.ai/)"
read -s LEONARDO_API_KEY
echo ""

if [ -z "$LEONARDO_API_KEY" ]; then
    echo "❌ API key cannot be empty"
    exit 1
fi

# Update .env file
update_env "LEONARDO_API_KEY" "$LEONARDO_API_KEY"
update_env "LEONARDO_API_URL" "https://cloud.leonardo.ai/api/rest/v1"
update_env "IMAGE_CACHE_DIR" "./image_cache"
update_env "IMAGE_CACHE_MAX_SIZE_GB" "10"

# Create cache directory
mkdir -p ./image_cache

echo "✅ Configuration saved to .env"
echo "✅ Cache directory created at ./image_cache"
echo ""
echo "⚠️  IMPORTANT: Never commit the .env file to git!"
echo ""
echo "📦 Building the image generation module..."

# Build the module
cargo build --release --bin think-ai-image

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo ""
    echo "🎯 You can now use Think AI Image Generation:"
    echo "  ./target/release/think-ai-image generate \"a beautiful sunset over mountains\""
    echo "  ./target/release/think-ai-image stats"
    echo "  ./target/release/think-ai-image --help"
else
    echo "❌ Build failed. Please check the error messages above."
fi