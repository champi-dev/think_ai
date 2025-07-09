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