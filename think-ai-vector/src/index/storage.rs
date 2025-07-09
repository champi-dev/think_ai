// Vector storage for the index

use ndarray::Array1;
use parking_lot::RwLock;
use std::sync::Arc;

pub struct VectorStorage {
    vectors: Arc<RwLock<Vec<Array1<f32>>>>,
    metadata: Arc<RwLock<Vec<serde_json::Value>>>,
}

impl Default for VectorStorage {
    fn default() -> Self {
        Self::new()
    }
}

impl VectorStorage {
    pub fn new() -> Self {
        Self {
            vectors: Arc::new(RwLock::new(Vec::new())),
            metadata: Arc::new(RwLock::new(Vec::new())),
        }
    }

    pub fn add(&self, vector: Array1<f32>, metadata: serde_json::Value) -> usize {
        let mut vectors = self.vectors.write();
        let mut meta = self.metadata.write();

        let idx = vectors.len();
        vectors.push(vector);
        meta.push(metadata);

        idx
    }

    pub fn get(&self, idx: usize) -> Option<(Array1<f32>, serde_json::Value)> {
        let vectors = self.vectors.read();
        let metadata = self.metadata.read();

        vectors.get(idx).cloned().zip(metadata.get(idx).cloned())
    }

    pub fn len(&self) -> usize {
        self.vectors.read().len()
    }
}
