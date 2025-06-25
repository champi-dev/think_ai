//! HTTP handlers

pub mod health;
pub mod compute;
pub mod search;
pub mod stats;

pub use health::health;
pub use compute::compute;
pub use search::search;
pub use stats::stats;