//! Think AI Vector - O(1) vector search using LSH
//!
//! This module implements constant-time similarity search through
//! hash-based indexing, achieving true O(1) performance.

pub mod types;
pub mod lsh;
pub mod math;
pub mod index;

pub use types::{VectorError, Result, LSHConfig, SearchResult};
pub use index::O1VectorIndex;
pub use math::{euclidean_distance, cosine_similarity};

#[cfg(test)]
mod tests;