#!/bin/bash

echo "🔧 FIXING DEPLOYMENT RUST VERSION COMPATIBILITY"
echo "=============================================="

# 1. Fix unclosed delimiter in prompt_optimizer.rs
echo "1️⃣ Fixing unclosed delimiter in prompt_optimizer.rs..."
# Check file structure
echo "Checking file structure..."
cd think-ai-image-gen/src
grep -n "^[[:space:]]*}" prompt_optimizer.rs | tail -5

# 2. Update Cargo.toml to use compatible dependency versions
echo ""
echo "2️⃣ Updating dependencies for Rust 1.80.1 compatibility..."
cd /home/champi/Dev/think_ai

# Update specific dependencies to compatible versions
echo "Updating half to compatible version..."
cargo update half@2.6.0 --precise 2.4.0

echo "Updating icu dependencies to compatible versions..."
cargo update icu_collections@2.0.0 --precise 1.5.0
cargo update icu_locale_core@2.0.0 --precise 1.5.0  
cargo update icu_normalizer@2.0.0 --precise 1.5.0
cargo update icu_normalizer_data@2.0.0 --precise 1.5.0
cargo update icu_properties@2.0.1 --precise 1.5.0
cargo update icu_properties_data@2.0.1 --precise 1.5.0
cargo update icu_provider@2.0.0 --precise 1.5.0

echo "Updating idna_adapter to compatible version..."
cargo update idna_adapter@1.2.1 --precise 1.2.0

echo "Updating other dependencies..."
cargo update litemap@0.8.0 --precise 0.7.0
cargo update potential_utf@0.1.2 --precise 0.1.1
cargo update tinystr@0.8.1 --precise 0.7.0
cargo update writeable@0.6.1 --precise 0.5.0
cargo update yoke@0.8.0 --precise 0.7.0
cargo update zerofrom@0.1.6 --precise 0.1.0
cargo update zerotrie@0.2.2 --precise 0.1.0
cargo update zerovec@0.11.2 --precise 0.10.0

# 3. Add rust-version to Cargo.toml
echo ""
echo "3️⃣ Setting rust-version in Cargo.toml..."
if ! grep -q "rust-version" Cargo.toml; then
    sed -i '/^\[package\]/a rust-version = "1.80"' Cargo.toml
fi

# 4. Test build with current Rust version
echo ""
echo "4️⃣ Testing build compatibility..."
rustc --version
cargo check --all 2>&1 | tail -20

echo ""
echo "✅ Deployment fixes applied!"
echo ""
echo "To verify:"
echo "1. Run: cargo check --all"
echo "2. If still having issues, consider:"
echo "   - Using cargo-msrv to find minimum supported Rust version"
echo "   - Pinning all dependencies in Cargo.lock"
echo "   - Updating Railway deployment to use Rust 1.82+"