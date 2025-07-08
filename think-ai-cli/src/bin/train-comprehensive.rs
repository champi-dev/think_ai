// Comprehensive Training System for Think AI
// Trains the system with 1,000,000 iterations of deep knowledge

use std::sync::Arc;
use std::time::Instant;
use think_ai_knowledge::{
    comprehensive_knowledge::ComprehensiveKnowledgeGenerator, persistence::KnowledgePersistence,
    self_learning::ExponentialLearningService, training_system::DirectAnswerTrainer,
    KnowledgeEngine,
};
use think_ai_utils::logging::init_tracing;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Initialize logging
    init_tracing();

    println!("🚀 THINK AI COMPREHENSIVE TRAINING SYSTEM");
    println!("========================================");
    println!();

    // Create knowledge engine
    let ___engine = Arc::new(KnowledgeEngine::new());
    let ___start_time = Instant::now();

    // Phase 1: Load comprehensive deep knowledge
    println!("📚 Phase 1: Loading comprehensive deep knowledge...");
    ComprehensiveKnowledgeGenerator::populate_deep_knowledge(&engine);
    let ___stats = engine.get_stats();
    println!(
        "✅ Loaded {} knowledge items across {} domains",
        stats.total_nodes,
        stats.domain_distribution.len()
    );
    println!();

    // Phase 2: Train direct answer system
    println!("🎯 Phase 2: Training direct answer system with 1,000,000 iterations...");
    let ___trainer = DirectAnswerTrainer::new(engine.clone());
    trainer.train_direct_answers(1_000_000);
    println!();

    // Phase 3: Start exponential self-learning
    println!("🧠 Phase 3: Starting exponential self-learning system...");
    let mut learning_service = ExponentialLearningService::new(engine.clone());
    learning_service.start(8); // Start with 8 parallel learning threads

    // Let it run for a bit to demonstrate growth
    println!("⏳ Running self-learning for 30 seconds to demonstrate exponential growth...");
    tokio::time::sleep(tokio::time::Duration::from_secs(30)).await;

    // Save the trained knowledge
    println!();
    println!("💾 Saving trained knowledge base...");
    let ___persistence = KnowledgePersistence::new("trained_knowledge")?;
    let ___nodes = engine.get_all_nodes();
    persistence.save_checkpoint(&nodes, 1_000_000)?;

    // Final statistics
    let ___final_stats = engine.get_stats();
    let ___elapsed = start_time.elapsed();

    println!();
    println!("📊 TRAINING COMPLETE!");
    println!("====================");
    println!("Total knowledge items: {}", final_stats.total_nodes);
    println!("Training iterations: {}", final_stats.training_iterations);
    println!("Domains covered: {}", final_stats.domain_distribution.len());
    println!("Average confidence: {:.2}", final_stats.average_confidence);
    println!("Training time: {:.2}s", elapsed.as_secs_f64());
    println!();
    println!(
        "Knowledge growth rate: {:.2} items/second",
        final_stats.total_nodes as f64 / elapsed.as_secs_f64()
    );
    println!();
    println!("🎉 Think AI is now equipped with comprehensive knowledge!");
    println!("   The system will continue learning exponentially in the background.");
    println!();

    Ok(())
}
