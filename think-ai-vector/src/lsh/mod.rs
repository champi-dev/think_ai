// Locality-Sensitive Hashing implementation

pub mod hasher;
pub mod projections;

pub use hasher::compute_hash;
pub use projections::generate_projections;
