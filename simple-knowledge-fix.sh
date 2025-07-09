#!/bin/bash
set -e

echo "Simple fix for knowledge lib.rs..."

# Fix line 129 - missing closing brace
sed -i '129a\}' think-ai-knowledge/src/lib.rs

# Fix line 152 - missing closing brace
sed -i '153a\    }' think-ai-knowledge/src/lib.rs

# Fix line 182 - missing closing brace
sed -i '182a\    }' think-ai-knowledge/src/lib.rs

# Fix line 193 - missing semicolon
sed -i '193s/$/;/' think-ai-knowledge/src/lib.rs

# Fix lines 208-210 - add matched = true
sed -i '210a\                    matched = true;' think-ai-knowledge/src/lib.rs

# Fix line 216 - add matched = true and closing brace
sed -i '216a\                    matched = true;\n                }' think-ai-knowledge/src/lib.rs

# Fix line 231 - add matched = true and closing brace
sed -i '231a\                    matched = true;\n                }' think-ai-knowledge/src/lib.rs

# Fix line 233 - add if statement
sed -i '233s/^/                else if Self::word_boundary_match(\&content_lower, \&query_lower) {\n                    if is_definition_query {/' think-ai-knowledge/src/lib.rs

# Fix lines around 241-243
sed -i '241a\                        } else {' think-ai-knowledge/src/lib.rs
sed -i '243s/.*$/                    } else {/' think-ai-knowledge/src/lib.rs

# Fix lines 261-263
sed -i '261a\                    if is_definition_query {' think-ai-knowledge/src/lib.rs
sed -i '262a\                    }' think-ai-knowledge/src/lib.rs
sed -i '263s/} else//' think-ai-knowledge/src/lib.rs

# Fix line 267 - add else
sed -i '268s/^/        } else {/' think-ai-knowledge/src/lib.rs

# Fix end of query function
sed -i '279a\        }\n    }' think-ai-knowledge/src/lib.rs

# Many more fixes needed...
echo "This approach is too complex. Need a different strategy."