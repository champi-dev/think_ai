#!/bin/bash
set -e

echo "Fixing Rust version compatibility issues..."
echo "Current rustc version: $(rustc --version)"
echo ""

# Downgrade dependencies to versions compatible with rustc 1.80.1
echo "Downgrading dependencies to compatible versions..."

# These commands will update specific dependencies to older versions
# that are compatible with rustc 1.80.1

cargo update half@2.6.0 --precise 2.3.1
cargo update icu_collections@2.0.0 --precise 1.5.0
cargo update icu_locale_core@2.0.0 --precise 1.5.0
cargo update icu_normalizer@2.0.0 --precise 1.5.0
cargo update icu_normalizer_data@2.0.0 --precise 1.5.0
cargo update icu_properties@2.0.1 --precise 1.5.0
cargo update icu_properties_data@2.0.1 --precise 1.5.0
cargo update icu_provider@2.0.0 --precise 1.5.0
cargo update idna_adapter@1.2.1 --precise 1.2.0
cargo update litemap@0.8.0 --precise 0.7.3
cargo update potential_utf@0.1.2 --precise 0.1.1
cargo update tinystr@0.8.1 --precise 0.7.6
cargo update writeable@0.6.1 --precise 0.5.5
cargo update yoke@0.8.0 --precise 0.7.4
cargo update zerofrom@0.1.6 --precise 0.1.4
cargo update zerotrie@0.2.2 --precise 0.1.3
cargo update zerovec@0.11.2 --precise 0.10.4

echo ""
echo "Attempting to build after dependency downgrades..."
cargo build --release

echo ""
echo "Build completed successfully!"
echo ""
echo "If you still encounter issues, you may need to:"
echo "1. Update your Rust toolchain: rustup update"
echo "2. Or use a specific older version: rustup default 1.81.0"
echo "3. Or manually edit Cargo.toml to specify exact versions"