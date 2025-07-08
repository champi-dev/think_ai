// HTTP handlers

pub mod chat;
pub mod compute;
pub mod health;
pub mod image;
pub mod knowledge;
pub mod search;
pub mod stats;

pub use chat::chat;
pub use compute::compute;
pub use health::health;
pub use image::{
    generate_image, get_image_stats, provide_feedback, serve_image, ImageGenerationState,
};
pub use knowledge::knowledge_stats;
pub use search::search;
pub use stats::stats;
