//! Self-Learning Service - Runs exponential learning in background

use std::sync::Arc;
use think_ai_knowledge::{
    KnowledgeEngine,
    self_learning::ExponentialLearningService,
    persistence::KnowledgePersistence,
    comprehensive_knowledge::ComprehensiveKnowledgeGenerator,
};
use think_ai_utils::logging::init_tracing;
use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Initialize logging
    init_tracing();
    
    println!("🧪 Think AI Self-Learning Service");
    println!("================================");
    
    // Create knowledge engine
    let engine = Arc::new(KnowledgeEngine::new());
    
    // Load existing knowledge if available
    let mut loaded_count = 0;
    if let Ok(persistence) = KnowledgePersistence::new("trained_knowledge") {
        if let Ok(loaded) = persistence.load_latest() {
            engine.load_nodes(loaded.nodes);
            loaded_count = engine.get_stats().total_nodes;
            println!("📚 Loaded {} existing knowledge items", loaded_count);
        }
    }
    
    // If no knowledge loaded, populate comprehensive knowledge
    if loaded_count == 0 {
        println!("🌍 No existing knowledge found. Loading comprehensive knowledge base...");
        ComprehensiveKnowledgeGenerator::populate_deep_knowledge(&engine);
        println!("✅ Loaded {} knowledge items", engine.get_stats().total_nodes);
    }
    
    // Start exponential learning service
    let mut service = ExponentialLearningService::new(engine.clone());
    service.start(4); // 4 parallel learning threads
    
    println!("🚀 Self-learning service started with 4 parallel threads");
    println!("📊 Knowledge will grow exponentially in the background");
    println!();
    
    // Keep running and save checkpoints periodically
    let mut checkpoint_counter = 0;
    loop {
        sleep(Duration::from_secs(300)).await; // 5 minutes
        
        checkpoint_counter += 1;
        
        // Save checkpoint
        let nodes = engine.get_all_nodes();
        let stats = engine.get_stats();
        
        println!("💾 Saving checkpoint #{} - {} knowledge items", checkpoint_counter, stats.total_nodes);
        
        if let Ok(persistence) = KnowledgePersistence::new("trained_knowledge") {
            if let Err(e) = persistence.save_checkpoint(&nodes, checkpoint_counter as u64 * 300) {
                eprintln!("⚠️  Failed to save checkpoint: {}", e);
            } else {
                println!("✅ Checkpoint saved successfully");
            }
        }
        
        // Print growth statistics
        if checkpoint_counter % 12 == 0 { // Every hour
            println!();
            println!("📊 Hourly Statistics:");
            println!("   Total Knowledge Items: {}", stats.total_nodes);
            println!("   Domains Covered: {}", stats.domain_distribution.len());
            println!("   Average Confidence: {:.2}", stats.average_confidence);
            
            // Calculate growth rate
            let growth_rate = if loaded_count > 0 {
                ((stats.total_nodes as f64 / loaded_count as f64) - 1.0) * 100.0
            } else {
                0.0
            };
            println!("   Growth Rate: {:.2}%", growth_rate);
            println!();
        }
    }
}