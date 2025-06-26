use std::sync::Arc;
use think_ai_knowledge::{
    comprehensive_trainer::{ComprehensiveTrainer, ComprehensiveTrainingConfig},
    persistence::KnowledgePersistence,
    KnowledgeEngine,
};

fn main() {
    println!("🚀 Think AI Comprehensive Training System");
    println!("=========================================\n");

    // Initialize knowledge engine
    let engine = Arc::new(KnowledgeEngine::new());
    
    // Try to load existing knowledge
    match KnowledgePersistence::new("comprehensive_knowledge") {
        Ok(persistence) => {
            match persistence.load_latest_checkpoint() {
                Ok(Some(checkpoint)) => {
                    println!("📚 Loaded {} existing knowledge nodes", checkpoint.nodes.len());
                    engine.load_nodes(checkpoint.nodes);
                }
                Ok(None) => {
                    println!("📝 Starting with fresh knowledge base");
                }
                Err(e) => {
                    println!("⚠️  Could not load knowledge: {}", e);
                }
            }
        }
        Err(e) => {
            println!("⚠️  Could not create persistence: {}", e);
        }
    }

    // Configure comprehensive training
    let config = ComprehensiveTrainingConfig {
        tool_iterations: 1000,
        conversation_iterations: 1000,
        batch_size: 50,
        domains: think_ai_knowledge::KnowledgeDomain::all_domains(),
        enable_self_improvement: true,
    };

    println!("⚙️  Training Configuration:");
    println!("   - Tool Training: {} iterations", config.tool_iterations);
    println!("   - Conversation Training: {} iterations", config.conversation_iterations);
    println!("   - Batch Size: {}", config.batch_size);
    println!("   - Self-Improvement: {}", if config.enable_self_improvement { "Enabled" } else { "Disabled" });
    println!("   - Domains: {} domains\n", config.domains.len());

    // Create and run trainer
    let mut trainer = ComprehensiveTrainer::new(engine.clone(), config);
    
    println!("🏋️  Starting comprehensive training...\n");
    let result = trainer.train_comprehensive();

    // Display results
    println!("\n📊 Training Results");
    println!("==================");
    
    println!("\n🔧 Tool Training:");
    println!("   - Iterations: {}", result.tool_training.iterations);
    println!("   - Successful Patterns: {}", result.tool_training.successful_patterns);
    println!("   - Average Quality: {:.2}%", result.tool_training.average_quality * 100.0);
    println!("   - Duration: {:.2}s", result.tool_training.duration.as_secs_f64());
    
    println!("\n💬 Conversation Training:");
    println!("   - Iterations: {}", result.conversation_training.iterations);
    println!("   - Successful Conversations: {}", result.conversation_training.successful_conversations);
    println!("   - Average Quality: {:.2}%", result.conversation_training.average_quality * 100.0);
    println!("   - Duration: {:.2}s", result.conversation_training.duration.as_secs_f64());
    
    println!("\n📈 Overall Metrics:");
    println!("   - Total Training Time: {:.2}s", result.total_duration.as_secs_f64());
    println!("   - Tool Response Quality: {:.2}%", result.quality_metrics.average_tool_quality * 100.0);
    println!("   - Conversation Quality: {:.2}%", result.quality_metrics.average_conversation_quality * 100.0);
    println!("   - Overall Success Rate: {:.2}%", result.quality_metrics.success_rate * 100.0);

    // Pattern distribution
    println!("\n🎯 Tool Pattern Distribution:");
    for (pattern, count) in &result.tool_training.pattern_distribution {
        println!("   - {}: {} successful patterns", pattern, count);
    }
    
    println!("\n🗣️  Conversation Tone Distribution:");
    for (tone, count) in &result.conversation_training.tone_distribution {
        println!("   - {}: {} conversations", tone, count);
    }

    // Save enhanced knowledge base
    let all_nodes = engine.get_all_nodes();
    println!("\n💾 Saving enhanced knowledge base...");
    match KnowledgePersistence::new("comprehensive_knowledge") {
        Ok(persistence) => {
            match persistence.save_checkpoint(&all_nodes, 2000) {
                Ok(_) => println!("✅ Successfully saved {} knowledge nodes", all_nodes.len()),
                Err(e) => println!("❌ Failed to save knowledge: {}", e),
            }
        }
        Err(e) => {
            println!("❌ Failed to create persistence: {}", e);
        }
    }

    // Display final statistics
    let stats = engine.get_stats();
    println!("\n📊 Final Knowledge Base Statistics:");
    println!("   - Total Nodes: {}", stats.total_nodes);
    println!("   - Training Iterations: {}", stats.training_iterations);
    println!("   - Total Knowledge Items: {}", stats.total_knowledge_items);
    println!("   - Average Confidence: {:.2}", stats.average_confidence);
    
    println!("\n🏆 Domain Distribution:");
    for (domain, count) in stats.domain_distribution {
        println!("   - {:?}: {} entries", domain, count);
    }

    println!("\n✨ Comprehensive training complete!");
    println!("🤖 Think AI is now equipped with:");
    println!("   ✓ Powerful tool capabilities for helping with tasks");
    println!("   ✓ Natural conversational abilities");
    println!("   ✓ Context-aware responses");
    println!("   ✓ Self-improvement mechanisms");
    println!("\n🎉 Ready to provide intelligent, helpful, and natural assistance!");
}