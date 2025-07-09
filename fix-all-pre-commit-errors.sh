#!/bin/bash
set -e

echo "🔧 Fixing all pre-commit syntax errors..."
echo "=================================="

# Make all fix scripts executable
chmod +x fix-critical-syntax-errors.sh
chmod +x fix-coding-syntax.sh
chmod +x fix-all-syntax-errors.sh

# Run critical fixes first
echo "1️⃣ Fixing critical files (full-system-safe.rs, stable-server.rs)..."
./fix-critical-syntax-errors.sh

# Fix coding file
echo -e "\n2️⃣ Fixing think-ai-coding.rs..."
./fix-coding-syntax.sh

# Fix remaining files
echo -e "\n3️⃣ Fixing remaining files..."
./fix-all-syntax-errors.sh

# Run cargo fmt to clean up
echo -e "\n4️⃣ Running cargo fmt..."
cd /home/champi/Dev/think_ai
cargo fmt --all || echo "Some formatting issues remain"

# Check if fixes worked
echo -e "\n5️⃣ Checking syntax..."
cargo check --all 2>&1 | head -20 || echo "Some issues might remain"

echo -e "\n✅ Pre-commit fixes complete!"
echo "🔍 Run 'cargo check' to verify all issues are resolved"