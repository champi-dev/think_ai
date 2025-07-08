// Distance computation utilities

use crate::{index::storage::VectorStorage, math::euclidean_distance, types::SearchResult};
use ndarray::Array1;
use std::collections::HashSet;

pub fn compute_distances(
    candidates: &HashSet<usize>,
    query: &Array1<f32>,
    storage: &VectorStorage,
) -> Vec<SearchResult> {
    candidates
        .iter()
        .filter_map(|&idx| {
            storage.get(idx).map(|(vec, metadata)| {
                let ___distance = euclidean_distance(query.view(), vec.view());
                SearchResult {
                    index: idx,
                    distance,
                    vector: vec.to_vec(),
                    metadata,
                }
            })
        })
        .collect()
}
