use std::time::Duration;
use think_ai_knowledge::{
    persistence::KnowledgePersistence, self_learning::SelfLearningSystem,
    trainer::KnowledgeTrainer, KnowledgeEngine,
};
use tokio::time::sleep;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🧠 Think AI Self-Learning Service Starting...");

    // Initialize components
    let knowledge_engine = std::sync::Arc::new(KnowledgeEngine::new());
    let mut self_learning = SelfLearningSystem::new(knowledge_engine.clone());
    let trainer = KnowledgeTrainer::new();

    // Load existing knowledge if available
    if let Ok(persistence) = KnowledgePersistence::new("knowledge_base") {
        if let Ok(nodes) = persistence.load() {
            let loaded_count = nodes.len();
            knowledge_engine.load_nodes(nodes);
            println!("📚 Loaded {} existing knowledge nodes", loaded_count);
        }
    }

    // Initial training if knowledge base is empty
    let stats = knowledge_engine.get_stats();
    if stats.total_nodes == 0 {
        println!("🎓 Performing initial training...");
        trainer.train_comprehensive(&knowledge_engine, 100);
        println!("✅ Initial training complete");
    }

    // Start self-learning loop
    println!("🔄 Starting continuous self-learning...");
    let mut iteration = 0;
    let mut checkpoint_counter = 0;

    loop {
        iteration += 1;
        println!("\n📊 Self-learning iteration #{}", iteration);

        // Perform self-learning
        self_learning.learn_iteration(&knowledge_engine).await;

        // Save checkpoint every 10 iterations
        checkpoint_counter += 1;
        if checkpoint_counter % 10 == 0 {
            if let Ok(persistence) = KnowledgePersistence::new("knowledge_base") {
                let nodes = knowledge_engine.get_all_nodes();
                if let Ok(_) = persistence.save(&nodes) {
                    println!("💾 Checkpoint saved ({} nodes)", nodes.len());
                }
            }
        }

        // Display stats every 12 iterations (hourly if 5 min intervals)
        if checkpoint_counter % 12 == 0 {
            let stats = knowledge_engine.get_stats();
            println!("\n📈 Knowledge Base Statistics:");
            println!("   Total Nodes: {}", stats.total_nodes);
            println!("   Domains: {:?}", stats.domains);
            println!("   Avg Confidence: {:.2}", stats.average_confidence);
        }

        // Sleep for 5 minutes before next iteration
        sleep(Duration::from_secs(300)).await;
    }
}
