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
    println!("║              THINK AI COMPREHENSIVE KNOWLEDGE TRAINING            ║");
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
        iterations: 1_000_000,
        meta_iterations: 1_000_000,
        batch_size: 1000,
        ..Default::default()
    };

    println!("Configuration:");
    println!("- Iterations: {}", config.iterations);
    println!("- Meta-iterations: {}", config.meta_iterations);
    println!("- Batch size: {}", config.batch_size);
    println!(
        "- Total expected items: {}\n",
        config.iterations * config.meta_iterations * config.batch_size as u64
    );

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
        "the origin of the universe",
        "human cognition and neuroscience",
    ];

    for query in demo_queries {
        println!("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
        println!("Query: {}", query);
        println!("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
        let response = responder.generate_comprehensive_response(query);
        println!("{}", response);
    }

    persistence.save_knowledge(&engine.get_all_nodes())?;
    persistence.save_checkpoint(
        &engine.get_all_nodes(),
        training_result.total_iterations * meta_result.total_sets,
    )?;

    println!("\n\n✅ TRAINING COMPLETE - KNOWLEDGE PERMANENTLY STORED");
    println!(
        "Total knowledge items: {}",
        engine.get_stats().total_knowledge_items
    );
    println!("Knowledge will persist forever in: ./knowledge_storage\n");

    Ok(())
}
