#!/bin/bash
set -e

echo "Fixing all remaining delimiter issues..."

# Fix think-ai-consciousness/src/consciousness_field.rs
echo "Fixing think-ai-consciousness/src/consciousness_field.rs"
sed -i '34s/Self::default()/Self::default()\n    }/' think-ai-consciousness/src/consciousness_field.rs
sed -i '36s/$/\n    }/' think-ai-consciousness/src/consciousness_field.rs
# Add closing braces at the end of the file
echo -e "    }\n}" >> think-ai-consciousness/src/consciousness_field.rs

# Fix think-ai-vector/src/lsh/projections.rs
echo "Fixing think-ai-vector/src/lsh/projections.rs"
sed -i 's/dim___/dim/g' think-ai-vector/src/lsh/projections.rs
echo "}" >> think-ai-vector/src/lsh/projections.rs

# Fix think-ai-qwen/src/client.rs
echo "Fixing think-ai-qwen/src/client.rs"
# Add closing brace for the new() method
sed -i '47s/$/\n    }/' think-ai-qwen/src/client.rs

# Fix think-ai-core/src/config/mod.rs
echo "Fixing think-ai-core/src/config/mod.rs"
cat >> think-ai-core/src/config/mod.rs << 'EOF'
}
EOF

# Fix think-ai-image-gen/src/lib.rs
echo "Fixing think-ai-image-gen/src/lib.rs - checking for missing braces in get_stats"
# First check line 194 to see if it needs fixing
if ! grep -q "GenerationStats {" think-ai-image-gen/src/lib.rs; then
    echo "GenerationStats already fixed"
else
    # Fix the get_stats method - it's missing the 'Ok(' wrapper
    sed -i '/pub fn get_stats(&self) -> GenerationStats {/,/average_generation_time_ms: self.calculate_avg_generation_time(),/{
        s/GenerationStats {/GenerationStats {/
        /average_generation_time_ms: self.calculate_avg_generation_time(),/a\
        }
    }' think-ai-image-gen/src/lib.rs
fi

echo "All delimiter fixes applied."