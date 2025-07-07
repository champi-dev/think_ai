//! HTTP handlers

pub mod health;
pub mod compute;
pub mod search;
pub mod stats;
pub mod chat;
pub mod knowledge;

pub use health::health;
pub use compute::compute;
pub use search::search;
pub use stats::stats;
pub use chat::chat;
pub use knowledge::knowledge_stats;