#!/bin/bash
echo "🔧 Fixing specific compilation errors..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Fix think-ai-utils/src/lib.rs - missing closing brace
echo -e "${GREEN}Fixing think-ai-utils/src/lib.rs...${NC}"
echo "}" >> think-ai-utils/src/lib.rs

# Fix think-ai-utils/src/perf.rs - missing closing braces
echo -e "${GREEN}Fixing think-ai-utils/src/perf.rs...${NC}"
# Add missing closing braces
cat >> think-ai-utils/src/perf.rs << 'EOF'
    }
}
}
EOF

# Fix think-ai-cache/src/lib.rs variable names
echo -e "${GREEN}Fixing think-ai-cache/src/lib.rs variable names...${NC}"
# Remove underscores from parameter names that are used
sed -i 's/key___:/key:/g' think-ai-cache/src/lib.rs
sed -i 's/value___:/value:/g' think-ai-cache/src/lib.rs
sed -i 's/max_size___:/max_size:/g' think-ai-cache/src/lib.rs
sed -i 's/cache___:/cache:/g' think-ai-cache/src/lib.rs
sed -i 's/config___:/config:/g' think-ai-cache/src/lib.rs

# Fix variable references in the same file
sed -i 's/___(hasher|cache|bytes|config|value|retrieved|data)/\1/g' think-ai-cache/src/lib.rs

# Fix think-ai-webapp files
echo -e "${GREEN}Fixing webapp issues...${NC}"
# Fix variable names in webapp files
sed -i 's/ctx___:/ctx:/g' think-ai-webapp/src/ui/dashboard.rs
sed -i 's/msg__:/msg:/g' think-ai-webapp/src/ui/dashboard.rs
sed -i 's/document__:/document:/g' think-ai-webapp/src/ui/dashboard.rs
sed -i 's/s___:/s:/g' think-ai-webapp/src/lib.rs
sed -i 's/time___:/time:/g' think-ai-webapp/src/lib.rs
sed -i 's/height___:/height:/g' think-ai-webapp/src/lib.rs
sed -i 's/query___:/query:/g' think-ai-webapp/src/lib.rs
sed -i 's/f__:/f:/g' think-ai-knowledge/src/types.rs

# Fix think-ai-webapp missing braces
echo -e "${GREEN}Adding missing braces to webapp files...${NC}"
# Add missing closing braces
echo "}" >> think-ai-webapp/src/ui/effects.rs
echo "}" >> think-ai-webapp/src/ui/dashboard.rs
echo "}" >> think-ai-webapp/src/lib.rs
echo "}" >> think-ai-knowledge/src/types.rs

# Fix think-ai-qwen/src/client.rs missing braces
echo -e "${GREEN}Fixing think-ai-qwen/src/client.rs...${NC}"
cat >> think-ai-qwen/src/client.rs << 'EOF'
    }
}
}
}
}
}
EOF

# Fix think-ai-consciousness missing brace
echo -e "${GREEN}Fixing think-ai-consciousness/src/lib.rs...${NC}"
echo "    }" >> think-ai-consciousness/src/lib.rs
echo "}" >> think-ai-consciousness/src/lib.rs

# Fix think-ai-vector missing brace
echo -e "${GREEN}Fixing think-ai-vector/src/index/mod.rs...${NC}"
echo "}" >> think-ai-vector/src/index/mod.rs

# Fix think-ai-cache missing braces
echo -e "${GREEN}Fixing think-ai-cache/src/lib.rs missing braces...${NC}"
cat >> think-ai-cache/src/lib.rs << 'EOF'
    }
}
}
}
}
}
}
}
EOF

# Fix think-ai-storage missing braces
echo -e "${GREEN}Fixing think-ai-storage/src/backends/memory.rs...${NC}"
cat >> think-ai-storage/src/backends/memory.rs << 'EOF'
        Ok(())
    }
}
}
EOF

# Fix think-ai-image-gen issues
echo -e "${GREEN}Fixing think-ai-image-gen/src/lib.rs...${NC}"
# Fix variable names
sed -i 's/config___:/config:/g' think-ai-image-gen/src/lib.rs
sed -i 's/request___:/request:/g' think-ai-image-gen/src/lib.rs
# Remove underscores from variable references
sed -i 's/___(api_key|api_url|cache_dir|max_cache_gb|client|cache|optimizer|learner|cache_key|enhanced_prompt|start_time|generation_time_ms|metadata|total_generations|cache_stats|config|generator)/\1/g' think-ai-image-gen/src/lib.rs
# Add missing closing braces
cat >> think-ai-image-gen/src/lib.rs << 'EOF'
        };
    }
}
}
}
EOF

echo -e "${GREEN}✅ Specific fixes complete!${NC}"
echo -e "${YELLOW}Running build to verify...${NC}"

# Try to build again
cd /home/champi/Dev/think_ai
cargo build --release 2>&1 | tee build-specific-fixes.log

# Check if build succeeded
if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo -e "${GREEN}✅ BUILD SUCCESSFUL!${NC}"
    echo -e "${YELLOW}You can now run:${NC}"
    echo "  ./target/release/think-ai chat      # Interactive CLI"
    echo "  ./target/release/think-ai server    # HTTP server"
    echo "  ./target/release/think-ai-webapp    # Web interface"
else
    echo -e "${RED}❌ Build still has errors. Check build-specific-fixes.log${NC}"
    echo -e "${YELLOW}Remaining errors:${NC}"
    grep -E "error\[E[0-9]+\]:|error:" build-specific-fixes.log | head -10
fi