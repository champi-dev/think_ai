#!/bin/bash

echo "=== Think AI System Health Check ==="
echo "Date: $(date)"
echo

# Check compilation status
echo "1. COMPILATION STATUS"
echo "===================="
TOTAL_ERRORS=$(cargo check 2>&1 | grep -E "error:|error\[E" | wc -l)
echo "Total compilation errors: $TOTAL_ERRORS"

# Break down errors by type
echo
echo "Error breakdown:"
cargo check 2>&1 | grep -E "error:" | head -10

# Check which packages have errors
echo
echo "2. AFFECTED PACKAGES"
echo "===================="
cargo check 2>&1 | grep "could not compile" | cut -d'`' -f2 | sort | uniq

# Check for delimiter errors specifically
echo
echo "3. DELIMITER ERRORS"
echo "===================="
DELIMITER_ERRORS=$(cargo check 2>&1 | grep -E "unclosed delimiter|mismatched closing delimiter" | wc -l)
echo "Delimiter-related errors: $DELIMITER_ERRORS"

echo
echo "Files with delimiter issues:"
cargo check 2>&1 | grep -B2 -E "unclosed delimiter|mismatched closing delimiter" | grep "^ -->" | cut -d' ' -f3 | cut -d':' -f1 | sort | uniq

# Check for unresolved imports
echo
echo "4. IMPORT ERRORS"
echo "================"
IMPORT_ERRORS=$(cargo check 2>&1 | grep -E "unresolved import" | wc -l)
echo "Unresolved import errors: $IMPORT_ERRORS"

# Check for method errors
echo
echo "5. METHOD/TYPE ERRORS"
echo "===================="
METHOD_ERRORS=$(cargo check 2>&1 | grep -E "no method named|no function named" | wc -l)
echo "Method/function errors: $METHOD_ERRORS"

# Check git status summary
echo
echo "6. GIT STATUS SUMMARY"
echo "===================="
MODIFIED_FILES=$(git status --porcelain | grep "^ M" | wc -l)
UNTRACKED_FILES=$(git status --porcelain | grep "^??" | wc -l)
echo "Modified files: $MODIFIED_FILES"
echo "Untracked files: $UNTRACKED_FILES"
echo "Untracked shell scripts (potential fix attempts): $(git status --porcelain | grep "^??" | grep "\.sh$" | wc -l)"

# Check if core packages compile
echo
echo "7. CORE PACKAGE STATUS"
echo "====================="
echo -n "think-ai-core: "
cargo check -p think-ai-core 2>&1 | grep -q "error:" && echo "❌ ERRORS" || echo "✅ OK"

echo -n "think-ai-knowledge: "
cargo check -p think-ai-knowledge 2>&1 | grep -q "error:" && echo "❌ ERRORS" || echo "✅ OK"

echo -n "think-ai-http: "
cargo check -p think-ai-http 2>&1 | grep -q "error:" && echo "❌ ERRORS" || echo "✅ OK"

echo -n "think-ai-cli: "
cargo check -p think-ai-cli 2>&1 | grep -q "error:" && echo "❌ ERRORS" || echo "✅ OK"

# Summary and recommendations
echo
echo "8. HEALTH SUMMARY"
echo "================"
if [ "$TOTAL_ERRORS" -eq 0 ]; then
    echo "✅ System is healthy - no compilation errors"
else
    echo "❌ System has compilation errors"
    echo
    echo "MAIN ISSUES IDENTIFIED:"
    echo "1. Delimiter errors (unclosed/mismatched brackets) in $DELIMITER_ERRORS files"
    echo "2. Unresolved imports: $IMPORT_ERRORS"
    echo "3. Method/type errors: $METHOD_ERRORS"
    echo
    echo "AFFECTED BINARIES:"
    cargo check 2>&1 | grep "could not compile" | grep "bin" | cut -d'"' -f2 | sort | uniq | head -10
    echo
    echo "RECOMMENDATIONS:"
    echo "1. Fix delimiter errors in the identified files (syntax issues)"
    echo "2. Review and fix import statements"
    echo "3. Update method calls to match current API"
    echo "4. Many shell scripts created suggest ongoing debugging efforts"
fi

echo
echo "=== Health Check Complete ==="