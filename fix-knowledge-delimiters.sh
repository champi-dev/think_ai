#!/bin/bash
set -e

echo "Fixing knowledge lib.rs delimiter issues..."

# Fix the first issue around line 241-243
sed -i '241s/$/\n                        } else {/' think-ai-knowledge/src/lib.rs
sed -i '242d' think-ai-knowledge/src/lib.rs  # Remove duplicate line
sed -i '243s/^/                    } else { /' think-ai-knowledge/src/lib.rs

# Fix missing closing braces around line 256
sed -i '255a\                        }\n                    }\n                }' think-ai-knowledge/src/lib.rs

# Fix the if-else structure around line 263
sed -i '263s/^/        } else /' think-ai-knowledge/src/lib.rs
sed -i '265a\        }' think-ai-knowledge/src/lib.rs

echo "Delimiter issues fixed!"