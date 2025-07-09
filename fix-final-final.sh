#!/bin/bash
echo "🔧 Final comprehensive fixes for all remaining errors..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Fix think-ai-utils/src/perf.rs
echo -e "${GREEN}Fixing think-ai-utils/src/perf.rs completely...${NC}"
cat > think-ai-utils/src/perf.rs << 'EOF'
use once_cell::sync::Lazy;
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::Arc;
use std::time::Instant;

/// Global operation counter for O(1) performance tracking
pub static GLOBAL_OPS: Lazy<Arc<AtomicU64>> = Lazy::new(|| Arc::new(AtomicU64::new(0)));

/// Increment global operation counter - O(1)
#[inline(always)]
pub fn inc_ops() {
    GLOBAL_OPS.fetch_add(1, Ordering::Relaxed);
}

/// Get total operations - O(1)
pub fn get_ops() -> u64 {
    GLOBAL_OPS.load(Ordering::Relaxed)
}

/// Performance guard that measures duration on drop
pub struct PerfGuard {
    name: &'static str,
    start: Instant,
}

impl PerfGuard {
    pub fn new(name: &'static str) -> Self {
        tracing::trace!("Starting operation: {}", name);
        Self {
            name,
            start: Instant::now(),
        }
    }
}

impl Drop for PerfGuard {
    fn drop(&mut self) {
        let duration = self.start.elapsed();
        tracing::trace!("{} completed in {:?}", self.name, duration);
        inc_ops();
    }
}

/// Macro for performance tracking
#[macro_export]
macro_rules! perf_guard {
    ($name:expr) => {
        let _guard = $crate::perf::PerfGuard::new($name);
    };
}
EOF

# Fix think-ai-image-gen/src/lib.rs completely
echo -e "${GREEN}Fixing think-ai-image-gen/src/lib.rs test function...${NC}"
# First, let's check how many lines we have
total_lines=$(wc -l < think-ai-image-gen/src/lib.rs)
echo "Total lines in file: $total_lines"

# Find where the test module starts
test_start=$(grep -n "#\[cfg(test)\]" think-ai-image-gen/src/lib.rs | head -1 | cut -d: -f1)
echo "Test module starts at line: $test_start"

# Keep everything before the test module
head -n $((test_start - 1)) think-ai-image-gen/src/lib.rs > think-ai-image-gen/src/lib.rs.tmp

# Add a proper test module
cat >> think-ai-image-gen/src/lib.rs.tmp << 'EOF'
#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_cache_key_generation() {
        let config = ImageGenConfig {
            api_key: "test".to_string(),
            api_url: "http://test".to_string(),
            cache_dir: "/tmp/test".into(),
            max_cache_size_bytes: 1024 * 1024,
            enable_learning: false,
        };
        let generator = ImageGenerator::new(config).await.unwrap();
        let request1 = ImageGenerationRequest {
            prompt: "A beautiful sunset".to_string(),
            negative_prompt: None,
            width: Some(512),
            height: Some(512),
            num_images: Some(1),
            guidance_scale: None,
            model_id: None,
        };
        let request2 = request1.clone();
        let key1 = generator.generate_cache_key(&request1);
        let key2 = generator.generate_cache_key(&request2);
        assert_eq!(key1, key2, "Same requests should generate same cache keys");
    }
}
EOF

mv think-ai-image-gen/src/lib.rs.tmp think-ai-image-gen/src/lib.rs

# Fix the QwenClient warning by using the config field
echo -e "${GREEN}Fixing QwenClient warning...${NC}"
sed -i 's/format!("Response to: {}", request.query)/format!("Response to: {} (model: {})", request.query, self.config.model)/' think-ai-qwen/src/client.rs

echo -e "${GREEN}✅ All fixes complete!${NC}"
echo -e "${YELLOW}Running final build to verify...${NC}"

# Try to build again
cd /home/champi/Dev/think_ai
cargo build --release 2>&1 | tee build-complete.log

# Check if build succeeded
if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo -e "${GREEN}✅ BUILD SUCCESSFUL!${NC}"
    echo -e "${YELLOW}You can now run:${NC}"
    echo "  ./target/release/think-ai chat      # Interactive CLI"
    echo "  ./target/release/think-ai server    # HTTP server"
    echo "  ./target/release/think-ai-webapp    # Web interface"
    
    # List all built binaries
    echo -e "\n${GREEN}Available binaries:${NC}"
    ls -la target/release/think-ai* | grep -v "\.d$" | grep -v "\.rlib$"
else
    echo -e "${RED}❌ Build still has errors. Check build-complete.log${NC}"
    echo -e "${YELLOW}Remaining errors:${NC}"
    grep -E "error\[E[0-9]+\]:|error:" build-complete.log | head -20
fi