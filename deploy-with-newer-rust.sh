#!/bin/bash

echo "🚀 DEPLOYMENT HELPER"
echo "==================="
echo ""
echo "For Railway deployment:"
echo "1. railway.toml is configured to use Rust 1.82"
echo "2. Push your changes: git push"
echo "3. Railway will automatically use the correct Rust version"
echo ""
echo "For local development:"
echo "1. Install Rust 1.82+: rustup update stable"
echo "2. Or use: rustup override set 1.82"
echo ""
echo "Current Rust version:"
rustc --version
