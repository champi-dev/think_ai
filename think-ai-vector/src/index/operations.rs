impl O1VectorIndex {
    pub fn add(&self, vector: Vec<f32>, metadata: serde_json::Value) -> Result<usize> {
        if vector.len() != self.config.dimension {
            return Err(VectorError::DimensionMismatch {
                expected: self.config.dimension,
                actual: vector.len(),
            });
        }
        
        let vector_array = ndarray::Array1::from_vec(vector);
        let idx = self.storage.add(vector_array.clone(), metadata);
        
        // Add to hash tables
        for table_idx in 0..self.config.num_hash_tables {
            let hash = lsh::compute_hash(
                vector_array.view(),
                &self.projections,
                table_idx,
                self.config.num_hash_functions
            );
            self.hash_tables.insert(table_idx, hash, idx);
        }
        
        Ok(idx)
    }
    
    pub fn len(&self) -> usize {
        self.storage.len()
    }
    
    pub fn is_empty(&self) -> bool {
        self.len() == 0
    }
    
    pub fn clear(&self) {
        self.hash_tables.clear();
    }
}