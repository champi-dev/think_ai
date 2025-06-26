#!/bin/bash

# Test the improved chat system

echo "Testing Think AI with improved direct answers..."
echo ""

# Test queries
./target/release/think-ai chat << EOF
hello
im daniel
what is the sun?
exit
EOF