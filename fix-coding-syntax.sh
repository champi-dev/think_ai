#!/bin/bash
set -e

echo "🔧 Fixing think-ai-coding.rs syntax errors..."

# Fix the prefix errors and raw string
cd /home/champi/Dev/think_ai

# Fix "here" prefix errors (add space)
sed -i 's/here"/here "/g' think-ai-cli/src/bin/think-ai-coding.rs

# Find and fix the unterminated raw string at line 1044
# Look for the pattern and ensure it's properly terminated
perl -i -pe '
    if (/^\s*r#"use axum:\{/ && !/#"/) {
        $_ .= "\n\"#\n";
    }
' think-ai-cli/src/bin/think-ai-coding.rs

# Alternative approach if the above doesn't work
# Find lines with r#" that don't have corresponding "#
awk '
    /r#"/ {
        # Count occurrences of r#" and "#
        open_count = gsub(/r#"/, "&")
        close_count = gsub(/"#/, "&")
        
        # If unmatched, add closing
        if (open_count > close_count) {
            print $0
            for (i = 0; i < (open_count - close_count); i++) {
                print "\"#"
            }
            next
        }
    }
    { print }
' think-ai-cli/src/bin/think-ai-coding.rs > /tmp/coding-fixed.rs

# Only replace if the fix worked
if [ -s /tmp/coding-fixed.rs ]; then
    mv /tmp/coding-fixed.rs think-ai-cli/src/bin/think-ai-coding.rs
fi

echo "✅ Coding syntax fixes applied!"