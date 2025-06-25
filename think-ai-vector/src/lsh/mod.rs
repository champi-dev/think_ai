//! Locality-Sensitive Hashing implementation

pub mod projections;
pub mod hasher;

pub use projections::generate_projections;
pub use hasher::compute_hash;