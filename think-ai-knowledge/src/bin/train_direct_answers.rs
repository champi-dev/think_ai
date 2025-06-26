//! Direct Answer Training for Think AI
//! Trains the system to provide direct, comprehensive answers

use std::sync::Arc;
use think_ai_knowledge::{KnowledgeEngine, real_knowledge::RealKnowledgeGenerator};
use think_ai_knowledge::training_system::TrainingOrchestrator;

fn main() {
    println!("🧠 Think AI - Direct Answer Training System");
    println!("=========================================\n");
    
    // Create knowledge engine
    let engine = Arc::new(KnowledgeEngine::new());
    
    // Load initial knowledge base
    println!("📚 Loading initial knowledge base...");
    RealKnowledgeGenerator::populate_comprehensive_knowledge(&engine);
    
    let initial_stats = engine.get_stats();
    println!("✅ Initial knowledge loaded: {} items\n", initial_stats.total_nodes);
    
    // Run comprehensive training
    let iterations = std::env::args()
        .nth(1)
        .and_then(|s| s.parse::<usize>().ok())
        .unwrap_or(10_000);  // Default to 10k for faster demo
    
    println!("🚀 Starting training with {} iterations", iterations);
    println!("This will train Think AI to provide direct, relevant answers.\n");
    
    TrainingOrchestrator::run_comprehensive_training(engine.clone(), iterations);
    
    // Save trained knowledge
    println!("\n💾 Saving trained knowledge base...");
    if let Ok(persistence) = think_ai_knowledge::persistence::KnowledgePersistence::new("./trained_knowledge") {
        if let Err(e) = persistence.save_checkpoint(&engine.get_all_nodes(), iterations as u64) {
            eprintln!("Failed to save checkpoint: {}", e);
        } else {
            println!("✅ Trained knowledge saved successfully!");
        }
    }
    
    // Final statistics
    let final_stats = engine.get_stats();
    println!("\n📊 Training Complete!");
    println!("====================");
    println!("Total knowledge items: {}", final_stats.total_nodes);
    println!("Training iterations: {}", iterations);
    println!("Domains covered: {}", final_stats.domain_distribution.len());
    
    println!("\n🎉 Think AI is now trained to provide direct, comprehensive answers!");
    println!("Run the chat to see improved responses.");
}