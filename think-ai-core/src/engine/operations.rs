use think_ai_cache::O1Cache;

impl O1Engine {
    pub async fn store(&self, key: &str, result: ComputeResult) -> Result<()> {
        let _hash = hash_key(key, self.config.hash_seed);
        let data = serde_json::to_vec(&result)
            .map_err(|e| crate::types::CoreError::OperationError(e.to_string()))?;
        self.cache.set(key, data).await
            .map_err(|e| crate::types::CoreError::OperationError(e.to_string()))?;
        self.state.increment_ops();
        Ok(())
    }

    pub fn stats(&self) -> EngineStats {
        let (initialized, operation_count) = self.state.get_stats();
        let cache_stats = self.cache.stats();
        EngineStats {
            initialized,
            operation_count,
            cache_size: cache_stats.size,
        }
    }
}