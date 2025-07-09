// Self-Learning System - Autonomous knowledge expansion

use crate::{KnowledgeDomain, KnowledgeEngine};
use std::sync::{Arc, Mutex};

pub struct SelfLearningSystem {
    engine: Arc<KnowledgeEngine>,
    is_running: Arc<Mutex<bool>>,
}

impl SelfLearningSystem {
    pub fn new(engine: Arc<KnowledgeEngine>) -> Self {
        Self {
            engine,
            is_running: Arc::new(Mutex::new(false)),
        }
    }

    pub fn start_learning(&self) {
        let mut is_running = self.is_running.lock().unwrap();
        *is_running = true;
        println!("🧠 Self-learning system started");
    }

    pub fn stop_learning(&self) {
        let mut is_running = self.is_running.lock().unwrap();
        *is_running = false;
        println!("🛑 Self-learning system stopped");
    }

    pub fn learn_from_existing_knowledge(&self) {
        println!("📚 Learning from existing knowledge base...");
        // Simple learning placeholder
        self.engine.add_knowledge(
            KnowledgeDomain::General,
            "Self-Learning".to_string(),
            "System is learning autonomously".to_string(),
            vec!["learning".to_string(), "autonomous".to_string()],
        );
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_self_learning_creation() {
        let engine = Arc::new(KnowledgeEngine::new());
        let system = SelfLearningSystem::new(engine);
        system.start_learning();
        system.stop_learning();
    }
}
