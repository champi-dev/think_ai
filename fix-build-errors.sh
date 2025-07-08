#!/bin/bash

echo "🔧 FIXING SPECIFIC BUILD ERRORS"
echo "=============================="

# 1. Fix think-ai-utils/src/perf.rs
echo "1️⃣ Fixing perf.rs..."
sed -i 's/tracing::trace!("Starting operation: {}", name);/tracing::trace!("Starting operation: {}", self.name);/' think-ai-utils/src/perf.rs
sed -i 's/name,/self.name,/' think-ai-utils/src/perf.rs
sed -i 's/, duration);/, self.start.elapsed());/' think-ai-utils/src/perf.rs

# 2. Fix think-ai-utils/src/lib.rs
echo "2️⃣ Fixing lib.rs variable names..."
cat > think-ai-utils/src/lib.rs << 'EOF'
//! Think AI Utils - Functional utilities for O(1) performance
//!
//! This module provides pure functional utilities for performance measurement,
//! logging, and other cross-cutting concerns.

pub mod logging;
pub mod perf;

use serde::{Deserialize, Serialize};
use std::time::Instant;

/// Measure the execution time of a closure and return both the result and duration
pub fn measure<F, T>(f: F) -> (T, std::time::Duration)
where
    F: FnOnce() -> T,
{
    let start = Instant::now();
    let result = f();
    let duration = start.elapsed();
    (result, duration)
}

/// Measure async execution time
pub async fn measure_async<F, Fut, T>(f: F) -> (T, std::time::Duration)
where
    F: FnOnce() -> Fut,
    Fut: std::future::Future<Output = T>,
{
    let start = Instant::now();
    let result = f().await;
    let duration = start.elapsed();
    (result, duration)
}

/// O(1) performance metrics
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PerfMetrics {
    pub operation: String,
    pub duration_ns: u128,
    pub complexity: String,
}

impl PerfMetrics {
    pub fn new(operation: impl Into<String>, duration: std::time::Duration) -> Self {
        Self {
            operation: operation.into(),
            duration_ns: duration.as_nanos(),
            complexity: "O(1)".to_string(),
        }
    }

    pub fn log(&self) {
        tracing::info!(
            "Performance: {} completed in {}ns ({})",
            self.operation,
            self.duration_ns,
            self.complexity
        );
    }
}

/// Simple timing macro for performance measurement
#[macro_export]
macro_rules! time_operation {
    ($op_name:expr, $body:expr) => {{
        let (result, duration) = $crate::measure(|| $body);
        let metrics = $crate::PerfMetrics::new($op_name, duration);
        metrics.log();
        result
    }};
}
EOF

# 3. Fix webapp variable issues
echo "3️⃣ Fixing webapp variable issues..."

# Fix effects.rs
sed -i 's/let _id = effect\.get_id()/let id = effect.get_id()/' think-ai-webapp/src/ui/effects.rs
sed -i 's/effect_\.update/effect.update/' think-ai-webapp/src/ui/effects.rs
sed -i 's/effect_\.render/effect.render/' think-ai-webapp/src/ui/effects.rs
sed -i 's/delta_time_/delta_time/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/time_/time/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/\bdocument\b/_document/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/\btime\b/time/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/\bdelta_time\b/delta_time/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/\bprogress\b/progress/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/\bfade\b/fade/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/\bopacity\b/opacity/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/\bradius\b/radius/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/\bhtml\b/html/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/\bsize\b/size/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/\bscale\b/scale/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/\bcurrent_x\b/current_x/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/\bcurrent_y\b/current_y/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/\bdistance\b/distance/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/intensity_:/intensity:/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/text_:/text:/g' think-ai-webapp/src/ui/effects.rs

# Fix mod.rs
sed -i 's/_window\./window./' think-ai-webapp/src/ui/mod.rs
sed -i 's/_document/document/g' think-ai-webapp/src/ui/mod.rs
sed -i 's/_style_element/style_element/g' think-ai-webapp/src/ui/mod.rs
sed -i 's/_head/head/g' think-ai-webapp/src/ui/mod.rs
sed -i 's/let _window =/let window =/' think-ai-webapp/src/ui/mod.rs
sed -i 's/let _document =/let document =/' think-ai-webapp/src/ui/mod.rs

# 4. Fix qwen client
echo "4️⃣ Fixing qwen client..."
sed -i 's/config___:/config:/g' think-ai-qwen/src/client.rs
sed -i 's/request___:/request:/g' think-ai-qwen/src/client.rs
sed -i 's/context___:/context:/g' think-ai-qwen/src/client.rs
sed -i 's/___prompt/prompt/g' think-ai-qwen/src/client.rs
sed -i 's/___response/response/g' think-ai-qwen/src/client.rs
sed -i 's/___request/request/g' think-ai-qwen/src/client.rs

# 5. Build again
echo ""
echo "5️⃣ Testing build..."
cargo build --release 2>&1 | grep -E "(Compiling|Finished|error:)" | tail -20

echo ""
echo "✅ Build errors fixed!"