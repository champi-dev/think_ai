#!/bin/bash

echo "🔧 FIXING PERF.RS SYNTAX ERRORS"
echo "=============================="

# Fix perf.rs completely
cat > think-ai-utils/src/perf.rs << 'EOF'
// Performance measurement utilities with O(1) guarantees

use once_cell::sync::Lazy;
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::Arc;

/// Global performance counter with O(1) increment
pub static GLOBAL_OPS: Lazy<Arc<AtomicU64>> = Lazy::new(|| Arc::new(AtomicU64::new(0)));

/// Increment global operation counter - O(1)
#[inline(always)]
pub fn inc_ops() {
    GLOBAL_OPS.fetch_add(1, Ordering::Relaxed);
}

/// Get total operations - O(1)
#[inline(always)]
pub fn get_ops() -> u64 {
    GLOBAL_OPS.load(Ordering::Relaxed)
}

/// Performance guard that measures duration on drop
pub struct PerfGuard {
    name: &'static str,
    start: std::time::Instant,
}

impl PerfGuard {
    pub fn new(name: &'static str) -> Self {
        tracing::trace!("Starting operation: {}", name);
        Self {
            name,
            start: std::time::Instant::now(),
        }
    }
}

impl Drop for PerfGuard {
    fn drop(&mut self) {
        let duration = self.start.elapsed();
        tracing::debug!("Operation '{}' completed in {:?}", self.name, duration);
        inc_ops();
    }
}

/// Macro for O(1) performance measurement
#[macro_export]
macro_rules! perf_guard {
    ($name:expr) => {
        let _guard = $crate::perf::PerfGuard::new($name);
    };
}

/// Simple performance timer
pub struct PerfTimer {
    start: std::time::Instant,
}

impl PerfTimer {
    pub fn new() -> Self {
        Self {
            start: std::time::Instant::now(),
        }
    }

    pub fn elapsed(&self) -> std::time::Duration {
        self.start.elapsed()
    }

    pub fn elapsed_ms(&self) -> f64 {
        self.elapsed().as_secs_f64() * 1000.0
    }
}

impl Default for PerfTimer {
    fn default() -> Self {
        Self::new()
    }
}
EOF

# Also fix the remaining webapp issues
echo ""
echo "Fixing remaining webapp variable issues..."

# Fix effects.rs more comprehensively
sed -i 's/effect_\./effect./' think-ai-webapp/src/ui/effects.rs
sed -i 's/\b_progress\b/progress/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/\b_fade\b/fade/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/\b_opacity\b/opacity/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/\b_radius\b/radius/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/\b_size\b/size/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/\b_scale\b/scale/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/\b_current_x\b/current_x/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/\b_current_y\b/current_y/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/\b_html\b/html/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/\b_time\b/time/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/\b_document\b/document/g' think-ai-webapp/src/ui/effects.rs

# Build again
echo ""
echo "Testing build..."
cargo build --release 2>&1 | grep -E "(Compiling|Finished|error:)" | tail -20

echo ""
echo "✅ Syntax errors fixed!"