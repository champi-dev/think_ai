// Random projections for LSH

use crate::types::LSHConfig;
use ndarray::Array1;
use rand::{Rng, SeedableRng};
use rand_chacha::ChaCha8Rng;

/// Generate random projection vectors for LSH
pub fn generate_projections(config: &LSHConfig) -> Vec<Array1<f32>> {
    let mut rng = ChaCha8Rng::seed_from_u64(config.seed);
    let total_projections = config.num_hash_tables * config.num_hash_functions;

    (0..total_projections)
        .map(|_| generate_single_projection(&mut rng, config.dimension))
        .collect()
}

fn generate_single_projection(rng: &mut ChaCha8Rng, dim: usize) -> Array1<f32> {
    let vec: Vec<f32> = (0..dim).map(|_| rng.gen::<f32>() * 2.0 - 1.0).collect();
    Array1::from_vec(vec)
}
