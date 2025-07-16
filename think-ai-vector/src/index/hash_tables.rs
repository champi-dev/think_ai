// Hash table management for O(1) lookups

use ahash::RandomState;
use dashmap::DashMap;

pub struct HashTables {
    tables: Vec<DashMap<u64, Vec<usize>, RandomState>>,
}

impl HashTables {
    pub fn new(num_tables: usize, seed: u64) -> Self {
        let tables = (0..num_tables)
            .map(|i| {
                let hasher = RandomState::with_seeds(seed + i as u64, 0, 0, 0);
                DashMap::with_capacity_and_hasher(1024, hasher)
            })
            .collect();

        Self { tables }
    }

    pub fn insert(&self, table_idx: usize, hash: u64, idx: usize) {
        self.tables[table_idx].entry(hash).or_default().push(idx);
    }

    pub fn get(&self, table_idx: usize, hash: u64) -> Option<Vec<usize>> {
        self.tables[table_idx].get(&hash).map(|entry| entry.clone())
    }

    pub fn clear(&self) {
        for table in &self.tables {
            table.clear();
        }
    }
}
