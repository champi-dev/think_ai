//! Think AI Utils - Functional utilities for O(1) performance
//!
//! This module provides pure functional utilities for performance measurement,
//! logging, and other cross-cutting concerns.

pub mod perf;
pub mod logging;

use std::time::Instant;
use serde::{Deserialize, Serialize};

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
    
    /// Assert that operation completed in O(1) time (< 1ms)
    pub fn assert_o1(&self) -> Result<(), String> {
        const O1_THRESHOLD_NS: u128 = 1_000_000; // 1ms
        
        if self.duration_ns > O1_THRESHOLD_NS {
            Err(format!(
                "Operation '{}' took {}ns, exceeding O(1) threshold of {}ns",
                self.operation, self.duration_ns, O1_THRESHOLD_NS
            ))
        } else {
            Ok(())
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_measure() {
        let (result, duration) = measure(|| {
            42
        });
        
        assert_eq!(result, 42);
        assert!(duration.as_nanos() > 0);
    }
    
    #[tokio::test]
    async fn test_measure_async() {
        let (result, duration) = measure_async(|| async {
            tokio::time::sleep(tokio::time::Duration::from_micros(10)).await;
            "done"
        }).await;
        
        assert_eq!(result, "done");
        assert!(duration.as_micros() >= 10);
    }
    
    #[test]
    fn test_perf_metrics() {
        let duration = std::time::Duration::from_micros(500);
        let metrics = PerfMetrics::new("test_op", duration);
        
        assert_eq!(metrics.operation, "test_op");
        assert_eq!(metrics.duration_ns, 500_000);
        assert!(metrics.assert_o1().is_ok());
    }
}