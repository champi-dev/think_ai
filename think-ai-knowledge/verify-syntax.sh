#!/bin/bash
echo "Verifying syntax fixes..."
cargo check 2>&1 | grep -E "error:|error\[" | wc -l
