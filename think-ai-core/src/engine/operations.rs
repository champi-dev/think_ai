impl O1Engine {
    pub fn store(&self, key: &str, result: ComputeResult) -> Result<()> {
        let hash = hash_key(key, self.config.hash_seed);
        self.cache.insert(hash, result);
        self.state.increment_ops();
        Ok(())
    }
    
    pub fn stats(&self) -> EngineStats {
        let (initialized, operation_count) = self.state.get_stats();
        EngineStats {
            initialized,
            operation_count,
            cache_size: self.cache.len(),
        }
    }
}