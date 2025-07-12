#!/bin/bash

echo "🧪 Running Think AI E2E Tests..."

# Create a temporary Cargo project for the test
mkdir -p /tmp/think-ai-e2e-test
cd /tmp/think-ai-e2e-test

# Create Cargo.toml
cat > Cargo.toml << EOF
[package]
name = "think-ai-e2e-test"
version = "0.1.0"
edition = "2021"

[dependencies]
tokio = { version = "1", features = ["full"] }
reqwest = { version = "0.11", features = ["json"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
anyhow = "1.0"
colored = "2.0"
uuid = { version = "1.4", features = ["v4"] }
EOF

# Create src directory first
mkdir -p src

# Copy the test file
cp /home/administrator/think_ai/e2e-test-full-system.rs src/main.rs

# Remove the rust-script header
sed -i '1,11d' src/main.rs

# Build and run
cargo run --release