//! Distance computation utilities

use crate::{
    types::SearchResult,
    math::euclidean_distance,
    index::storage::VectorStorage,
};
use ndarray::Array1;
use std::collections::HashSet;

pub fn compute_distances(
    candidates: &HashSet<usize>,
    query: &Array1<f32>,
    storage: &VectorStorage,
) -> Vec<SearchResult> {
    candidates.iter()
        .filter_map(|&idx| {
            storage.get(idx).map(|(vec, metadata)| {
                let distance = euclidean_distance(query.view(), vec.view());
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