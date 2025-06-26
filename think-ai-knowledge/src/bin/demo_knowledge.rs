use std::sync::Arc;
use think_ai_knowledge::{
    evidence::EvidenceCollector,
    persistence::KnowledgePersistence,
    responder::ComprehensiveResponder,
    trainer::{KnowledgeTrainer, TrainingConfig},
    KnowledgeEngine,
};

fn main() -> std::io::Result<()> {
    println!("\n╔══════════════════════════════════════════════════════════════════╗");
    println!("║          THINK AI KNOWLEDGE TRAINING DEMONSTRATION                ║");
    println!("╚══════════════════════════════════════════════════════════════════╝\n");

    let engine = Arc::new(KnowledgeEngine::new());

    let persistence = KnowledgePersistence::new("./knowledge_storage")?;
    if let Some(checkpoint) = persistence.load_latest_checkpoint()? {
        println!(
            "Loading checkpoint from iteration {}...",
            checkpoint.iteration
        );
        engine.load_nodes(checkpoint.nodes);
        println!(
            "Loaded {} knowledge items from checkpoint\n",
            engine.get_stats().total_nodes
        );
    }

    let config = TrainingConfig {
        iterations: 100,
        meta_iterations: 10,
        batch_size: 100,
        ..Default::default()
    };

    println!("Demo Configuration (scaled down for demonstration):");
    println!("- Iterations: {}", config.iterations);
    println!("- Meta-iterations: {}", config.meta_iterations);
    println!("- Batch size: {}", config.batch_size);
    println!(
        "- Total items: {}\n",
        config.iterations * config.meta_iterations * config.batch_size as u64
    );

    println!("NOTE: Full training would use 1,000,000 iterations × 1,000,000 meta-iterations");
    println!("      This demo uses 100 × 10 to provide evidence of functionality\n");

    let trainer = KnowledgeTrainer::new(engine.clone(), config);

    println!(
        "Phase 1: Training with {} iterations...",
        trainer.config.iterations
    );
    let training_result = trainer.train();

    println!(
        "\nPhase 2: Meta-training with {} sets...",
        trainer.config.meta_iterations
    );
    let meta_result = trainer.meta_train();

    let evidence_collector = EvidenceCollector::new(engine.clone(), "./knowledge_storage")?;
    let evidence =
        evidence_collector.collect_comprehensive_evidence(&training_result, Some(&meta_result))?;

    println!("{}", evidence);

    println!("\n\n=== DEMONSTRATING COMPREHENSIVE RESPONSES ===\n");

    let responder = ComprehensiveResponder::new(engine.clone());
    let demo_queries = vec![
        "consciousness and quantum mechanics",
        "the nature of mathematical truth",
        "artificial intelligence ethics",
    ];

    for query in demo_queries {
        println!("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
        println!("Query: {}", query);
        println!("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
        let response = responder.generate_comprehensive_response(query);
        if response.len() > 500 {
            println!(
                "{}...\n[Response truncated for demo - full response is {} characters]",
                &response[..500],
                response.len()
            );
        } else {
            println!("{}", response);
        }
    }

    persistence.save_knowledge(&engine.get_all_nodes())?;
    persistence.save_checkpoint(
        &engine.get_all_nodes(),
        training_result.total_iterations * meta_result.total_sets,
    )?;

    let persistence_report = persistence.verify_persistence()?;
    println!("\n\n{}", persistence_report);

    println!("\n✅ DEMONSTRATION COMPLETE");
    println!(
        "Total knowledge items created: {}",
        engine.get_stats().total_knowledge_items
    );
    println!("Knowledge persisted in: ./knowledge_storage");
    println!(
        "\nFull training would create {} items and provide comprehensive coverage",
        1_000_000u64 * 1_000_000u64 * 1000u64
    );

    Ok(())
}
