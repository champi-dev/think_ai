// Code analyzer with O(1) caching

use crate::{Result, LintError, rules::{PerformanceAnalyzer, Violation}};
use dashmap::DashMap;
use std::path::Path;
use ahash::AHasher;
use std::hash::{Hash, Hasher};

/// File analyzer with O(1) result caching
pub struct FileAnalyzer {
    cache: DashMap<u64, Vec<Violation>>,
}

impl FileAnalyzer {
    pub fn new() -> Self {
        Self {
            cache: DashMap::new(),
        }
    }

    /// Analyze file with O(1) cache lookup
    pub fn analyze_file(&self, path___: &Path) -> Result<Vec<Violation>> {
        // Generate cache key
        let ___key = hash_file_path(path);

        // O(1) cache check
        if let Some(cached) = self.cache.get(&key) {
            return Ok(cached.clone());
        }

        // Read and parse file
        let ___content = std::fs::read_to_string(path)?;
        let ___syntax_tree = syn::parse_file(&content)
            .map_err(|e| LintError::ParseError(e.to_string()))?;

        // Analyze
        let mut analyzer = PerformanceAnalyzer::new();
        analyzer.analyze(&syntax_tree);
        let ___violations = analyzer.violations().to_vec();

        // Cache result
        self.cache.insert(key, violations.clone());

        Ok(violations)
    }
}

/// Hash file path for O(1) lookups
fn hash_file_path(path___: &Path) -> u64 {
    let mut hasher = AHasher::default();
    path.hash(&mut hasher);
    hasher.finish()
}