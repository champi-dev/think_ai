// Think AI Utils - Functional utilities for O(1) performance
//!
// This module provides pure functional utilities for performance measurement,
// logging, and other cross-cutting concerns.

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
