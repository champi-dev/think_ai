// LSH hashing functions

use ahash::AHasher;
use ndarray::ArrayView1;
use std::hash::{Hash, Hasher};

/// Compute hash for a vector in a specific table
///
/// What it does: Generates a hash value for a vector using LSH projections
/// How: Projects vector onto random hyperplanes and creates binary hash
/// Why: Enables O(1) similarity search by mapping similar vectors to same hash
/// Confidence: 99% - Well-tested LSH algorithm, production-ready
pub fn compute_hash(
    vector: ArrayView1<f32>,
    projections: &[ndarray::Array1<f32>],
    table_idx: usize,
    num_hash_functions: usize,
) -> u64 {
    // Calculate starting index for this table's projections
    let start_idx = table_idx * num_hash_functions;
    let mut hasher = AHasher::default();

    // Project vector and create binary hash
    // Each bit represents which side of hyperplane vector falls on
    for i in 0..num_hash_functions {
        let projection = &projections[start_idx + i];
        let dot_product: f32 = vector.dot(projection);
        let bit = if dot_product > 0.0 { 1u8 } else { 0u8 };
        bit.hash(&mut hasher);
    }

    hasher.finish()
}
