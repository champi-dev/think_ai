use std::collections::HashSet;
use crate::types::SearchResult;

impl O1VectorIndex {
    pub fn search(&self, query: Vec<f32>, k: usize) -> Result<Vec<SearchResult>> {
        if query.len() != self.config.dimension {
            return Err(VectorError::DimensionMismatch {
                expected: self.config.dimension,
                actual: query.len(),
            });
        }

        let query_array = ndarray::Array1::from_vec(query);
        let mut candidates = HashSet::new();

        // Collect candidates from all hash tables
        for table_idx in 0..self.config.num_hash_tables {
            let hash = lsh::compute_hash(
                query_array.view(),
                &self.projections,
                table_idx,
                self.config.num_hash_functions
            );

            if let Some(indices) = self.hash_tables.get(table_idx, hash) {
                candidates.extend(indices);
            }
        }

        // Compute distances and sort
        let mut results = distance::compute_distances(&candidates, &query_array, &self.storage);
        results.sort_by(|a, b| a.distance.partial_cmp(&b.distance).unwrap());
        results.truncate(k);

        Ok(results)
    }
}