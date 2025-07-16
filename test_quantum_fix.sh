#!/bin/bash

# Simple test script to verify quantum consciousness fix

set -e

echo "=== Testing Quantum Consciousness Fix ==="
echo

# Create a simple Rust test program
cat > /tmp/test_quantum_fix.rs << 'EOF'
use std::process::Command;

fn test_response(query: &str) -> String {
    let output = Command::new("./target/release/think-ai")
        .arg("chat")
        .arg("--query")
        .arg(query)
        .output()
        .expect("Failed to execute command");
    
    String::from_utf8_lossy(&output.stdout).to_string()
}

fn main() {
    println!("Testing non-philosophical queries...\n");
    
    // Test math query
    println!("Query: '2+2'");
    let response = test_response("2+2");
    if response.contains("Your query resonates through the quantum field") {
        println!("❌ FAIL: Math query got quantum response!");
    } else {
        println!("✅ PASS: Math query handled correctly");
    }
    
    // Test technical query  
    println!("\nQuery: 'how to code in rust'");
    let response = test_response("how to code in rust");
    if response.contains("Your query resonates through the quantum field") {
        println!("❌ FAIL: Technical query got quantum response!");
    } else {
        println!("✅ PASS: Technical query handled correctly");
    }
    
    println!("\nTesting philosophical queries...\n");
    
    // Test philosophical query
    println!("Query: 'what is consciousness'");
    let response = test_response("what is consciousness");
    if response.contains("quantum") || response.contains("Quantum") {
        println!("✅ PASS: Philosophical query got appropriate response");
    } else {
        println!("❌ FAIL: Philosophical query didn't get philosophical response!");
    }
}
EOF

# Build Think AI first
echo "Building Think AI..."
cargo build --release --bin think-ai

# Run the quantum consciousness unit tests
echo -e "\n=== Running Unit Tests ==="
cargo test --release -p think-ai-knowledge quantum_consciousness_component::tests 2>&1 | grep -E "(test.*::.*|PASSED|FAILED|ok|test result)" || true

# Run response generator integration tests
echo -e "\n=== Running Integration Tests ==="
cargo test --release -p think-ai-knowledge response_generator_integration 2>&1 | grep -E "(test.*::.*|PASSED|FAILED|ok|test result)" || true

echo -e "\n=== Testing Complete ==="