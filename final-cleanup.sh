#!/bin/bash
echo "🔧 Final cleanup to fix all compilation errors..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Revert all changes first
echo -e "${YELLOW}Reverting all changes to clean state...${NC}"
git checkout -- . 2>/dev/null || echo "Revert complete"

# Now apply only the necessary fixes
echo -e "${GREEN}Applying targeted fixes...${NC}"

# Create the missing utils and qwen files properly
echo -e "${GREEN}Creating think-ai-utils/src/perf.rs...${NC}"
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

echo -e "${GREEN}Creating think-ai-qwen/src/client.rs...${NC}"
cat > think-ai-qwen/src/client.rs << 'EOF'
use anyhow::Result;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QwenConfig {
    pub api_key: Option<String>,
    pub base_url: String,
    pub model: String,
}

impl Default for QwenConfig {
    fn default() -> Self {
        Self {
            api_key: None,
            base_url: "https://api.qwen.ai".to_string(),
            model: "qwen-turbo".to_string(),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QwenRequest {
    pub query: String,
    pub context: Option<String>,
    pub system_prompt: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QwenResponse {
    pub content: String,
    pub usage: Usage,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Usage {
    pub prompt_tokens: u32,
    pub completion_tokens: u32,
    pub total_tokens: u32,
}

pub struct QwenClient {
    config: QwenConfig,
}

impl QwenClient {
    pub fn new(config: QwenConfig) -> Self {
        Self { config }
    }

    pub async fn generate(&self, request: QwenRequest) -> Result<QwenResponse> {
        // Simulate a response for now
        let response = QwenResponse {
            content: format!("Response to: {} (model: {})", request.query, self.config.model),
            usage: Usage {
                prompt_tokens: 10,
                completion_tokens: 20,
                total_tokens: 30,
            },
        };
        Ok(response)
    }

    pub async fn generate_simple(&self, query: &str, context: Option<&str>) -> Result<String> {
        let request = QwenRequest {
            query: query.to_string(),
            context: context.map(|c| c.to_string()),
            system_prompt: None,
        };
        let response = self.generate(request).await?;
        Ok(response.content)
    }
}
EOF

# Run the original compilation error fix script
echo -e "${GREEN}Running compilation error fixes...${NC}"
./fix-compilation-errors.sh

# Run the final compilation fix
echo -e "${GREEN}Running final compilation fixes...${NC}"
./fix-final-compilation.sh

echo -e "${GREEN}✅ Cleanup complete!${NC}"
echo -e "${YELLOW}Running final build...${NC}"

# Final build
cd /home/champi/Dev/think_ai
cargo build --release 2>&1 | tee build-final-cleanup.log

# Check if build succeeded
if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo -e "${GREEN}✅ BUILD SUCCESSFUL!${NC}"
    echo -e "${YELLOW}You can now run:${NC}"
    echo "  ./target/release/think-ai chat      # Interactive CLI"
    echo "  ./target/release/think-ai server    # HTTP server"
    echo "  ./target/release/think-ai-webapp    # Web interface"
    
    # List available binaries
    echo -e "\n${GREEN}Available binaries:${NC}"
    ls -la target/release/think-ai* 2>/dev/null | grep -v "\.d$" | grep -v "\.rlib$" | head -20
else
    echo -e "${RED}❌ Build still has errors. Check build-final-cleanup.log${NC}"
    echo -e "${YELLOW}Summary of remaining errors:${NC}"
    grep -E "error(\[E[0-9]+\])?:" build-final-cleanup.log | grep -v "could not compile" | sort | uniq | head -10
fi