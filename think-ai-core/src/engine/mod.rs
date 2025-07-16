// O(1) Engine implementation
//!
// # What is O(1)?
// Imagine you have a huge library with millions of books. O(1) means you can find
// any book instantly - not by searching through shelves, but by knowing exactly
// where it is. Like having a magic map that tells you "Harry Potter is at shelf 42,
// position 7" without looking at any other books.
//!
// # How This Engine Works
// This engine is like that magic library. When you ask for something, it uses a
// special trick called "hashing" to instantly know where to find it. No searching,
// no waiting - just instant answers.

pub mod hasher;
pub mod state;

use self::{hasher::hash_key, state::StateManager};
use crate::{
    config::EngineConfig,
    types::{ComputeResult, EngineStats, Result},
};
use std::sync::Arc;
use think_ai_cache::MemoryCache;

/// Core O(1) Engine with functional design
///
/// # The Three Magic Components
///
/// 1. **Config** - The rules of our magic library
///    Like saying "our library has 1 million slots and uses spell #42 for finding books"
///
/// 2. **State** - Is the library open or closed?
///    We need to know if we're ready to serve customers
///
/// 3. **Cache** - The actual magic shelves
///    This is where we store everything with instant access
pub struct O1Engine {
    pub(crate) config: Arc<EngineConfig>,
    pub(crate) state: StateManager,
    pub(crate) cache: MemoryCache,
}

impl O1Engine {
    /// Creates a new O(1) Engine
    ///
    /// # What happens here?
    /// Think of this like opening a new library:
    /// 1. We decide how many shelves we need (cache_size)
    /// 2. We create a special spell for finding books (hash_seed)
    /// 3. We build the shelves (cache)
    /// 4. We put up an "Opening Soon" sign (state)
    pub fn new(config: EngineConfig) -> Self {
        let cache = MemoryCache::new(config.cache_size);
        Self {
            config: Arc::new(config),
            state: StateManager::new(),
            cache,
        }
    }

    /// Initialize the engine - like turning on the lights in our library
    ///
    /// # Why async?
    /// Even though this is fast, we might need to do things like:
    /// - Check if all shelves are ready
    /// - Warm up the magic spells
    /// - Make sure everything is connected
    /// Using async lets other things happen while we prepare
    pub async fn initialize(&self) -> Result<()> {
        tracing::info!("Initializing O(1) engine");
        self.state.set_initialized();
        Ok(())
    }

    /// The Magic Happens Here! Find any value in O(1) time
    ///
    /// # How it works (like finding a book instantly):
    /// 1. Take the key (like "Harry Potter")
    /// 2. Use our magic spell (hash function) to get a shelf number
    /// 3. Go directly to that shelf - no searching!
    /// 4. Return what we find (or None if empty)
    ///
    /// # Example
    /// ```
    /// let result = engine.compute("What is the meaning of life?");
    /// // Instantly returns the answer if we've seen this question before
    /// ```
    pub async fn compute(&self, key: &str) -> Option<ComputeResult> {
        // Step 1: Turn the key into a magic number (hash) for internal use
        // This ALWAYS takes the same time, whether key is 1 char or 1 million chars
        let _hash = hash_key(key, self.config.hash_seed);

        // Step 2: Use the key directly with the cache (it handles hashing internally)
        // Like teleporting to the exact shelf in our library
        match self.cache.get(key).await {
            Ok(data) => {
                // Deserialize the cached data
                serde_json::from_slice(&data).ok()
            }
            Err(_) => None,
        }
    }
}

// Include operations implementation
include!("operations.rs");
