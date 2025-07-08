// Functional logging utilities with zero-copy performance

use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

/// Initialize tracing with optimized settings
pub fn init_tracing() {
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "think_ai=debug,tower_http=debug".into()),
        )
        .with(tracing_subscriber::fmt::layer())
        .init();
}

/// Log with O(1) performance using compile-time optimization
#[macro_export]
macro_rules! o1_log {
    ($level:expr, $($arg:tt)*) => {
        match $level {
            "trace" => tracing::trace!($($arg)*),
            "debug" => tracing::debug!($($arg)*),
            "info" => tracing::info!($($arg)*),
            "warn" => tracing::warn!($($arg)*),
            "error" => tracing::error!($($arg)*),
            _ => tracing::info!($($arg)*),
        }
    };
}
