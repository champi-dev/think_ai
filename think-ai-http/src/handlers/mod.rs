// HTTP handlers

pub mod chat;
pub mod compute;
pub mod health;
// pub mod image; // Removed - no image-gen dependency
pub mod knowledge;
pub mod parallel_chat;
pub mod search;
pub mod stats;
pub use chat::chat;
pub use compute::compute;
pub use health::health;
// Image handlers removed
pub use knowledge::knowledge_stats;
pub use parallel_chat::{parallel_chat, initialize_parallel_consciousness};
pub use search::search;
pub use stats::stats;
