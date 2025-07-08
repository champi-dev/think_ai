// Think AI Vector - O(1) vector search using LSH
//!
// This module implements constant-time similarity search through
// hash-based indexing, achieving true O(1) performance.

pub mod index;
pub mod lsh;
pub mod math;
pub mod types;

pub use index::O1VectorIndex;
pub use math::{cosine_similarity, euclidean_distance};
pub use types::{LSHConfig, Result, SearchResult, VectorError};

#[cfg(test)]
mod tests;
