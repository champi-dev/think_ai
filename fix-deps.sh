#!/bin/bash
# Fix dependency versions for older Rust compatibility

echo "🔧 Fixing dependency versions for Rust 1.80.1 compatibility..."

# Clean and update dependencies
cargo clean

# Update to compatible versions
cargo update -p icu_collections --precise 1.5.0
cargo update -p icu_locale_core --precise 1.5.0
cargo update -p icu_normalizer --precise 1.5.0
cargo update -p icu_properties --precise 1.5.0
cargo update -p icu_provider --precise 1.5.0
cargo update -p idna --precise 0.5.0
cargo update -p idna_adapter --precise 1.0.0
cargo update -p litemap --precise 0.7.3
cargo update -p tinystr --precise 0.7.6
cargo update -p writeable --precise 0.5.5
cargo update -p yoke --precise 0.7.4
cargo update -p zerofrom --precise 0.1.4
cargo update -p zerovec --precise 0.10.4

echo "✅ Dependencies updated to compatible versions"
echo "🚀 Now try building again with: cargo build --release"