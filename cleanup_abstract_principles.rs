#!/usr/bin/env cargo script

// Cleanup utility to remove problematic abstract principles from knowledge storage
// Run with: cargo script cleanup_abstract_principles.rs
use std::sync::Arc;
use think_ai_knowledge::{
    KnowledgeEngine,
    persistence::KnowledgePersistence,
};
fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🧹 Think AI Knowledge Cleanup Utility");
    println!("=====================================");
    println!();
    // Load existing knowledge from all possible locations
    let engine = Arc::new(KnowledgeEngine::new());
    let mut total_loaded = 0;
    let mut cleaned_count = 0;
    // Try trained_knowledge
    if let Ok(persistence) = KnowledgePersistence::new("trained_knowledge") {
        if let Ok(Some(checkpoint)) = persistence.load_latest_checkpoint() {
            let count = checkpoint.nodes.len();
            println!("📚 Loading {} items from trained_knowledge...", count);
            engine.load_nodes(checkpoint.nodes);
            total_loaded += count;
        }
    }
    // Try knowledge_storage
    if let Ok(persistence) = KnowledgePersistence::new("knowledge_storage") {
            println!("📚 Loading {} items from knowledge_storage...", count);
    println!("✅ Total items loaded: {}", total_loaded);
    // Clean up problematic abstract principles
    println!("🔍 Scanning for problematic abstract principles...");
    let all_nodes = engine.get_all_nodes();
    let mut nodes_to_keep = Vec::new();
    for (_, node) in all_nodes.iter() {
        let _should_remove =
            // Remove nodes with "Abstract principle derived from" in content
            node.content.contains("Abstract principle derived from") ||
            // Remove nodes with "Abstract Principle from" in topic
            node.topic.contains("Abstract Principle from") ||
            // Remove nodes that are just generic philosophical abstractions
            (node.content.contains("Symmetry breaking leads to differentiation") ||
             node.content.contains("Systems tend toward increasing complexity") ||
             node.content.contains("Information flows create feedback loops") ||
             node.content.contains("Emergence occurs when simple rules") ||
             node.content.contains("Balance between order and chaos") ||
             node.content.contains("Hierarchical organization enables") ||
             node.content.contains("Networks exhibit power law") ||
             node.content.contains("Optimization involves tradeoffs"));
        if should_remove {
            cleaned_count += 1;
            println!("❌ Removing: {}", node.topic);
        } else {
            nodes_to_keep.push(node.clone());
    println!("📊 Cleanup Results:");
    println!("   Original items: {}", total_loaded);
    println!("   Items removed: {}", cleaned_count);
    println!("   Items kept: {}", nodes_to_keep.len());
    if cleaned_count > 0 {
        // Create new engine with cleaned nodes
        let clean_engine = Arc::new(KnowledgeEngine::new());
        clean_engine.load_nodes(nodes_to_keep);
        // Save cleaned knowledge back
        println!("💾 Saving cleaned knowledge...");
        if let Ok(persistence) = KnowledgePersistence::new("trained_knowledge") {
            let clean_nodes = clean_engine.get_all_nodes();
            if let Err(e) = persistence.save_checkpoint(&clean_nodes, 0) {
                eprintln!("⚠️  Failed to save to trained_knowledge: {}", e);
            } else {
                println!("✅ Saved cleaned knowledge to trained_knowledge");
            }
        if let Ok(persistence) = KnowledgePersistence::new("knowledge_storage") {
                eprintln!("⚠️  Failed to save to knowledge_storage: {}", e);
                println!("✅ Saved cleaned knowledge to knowledge_storage");
        println!();
        println!("🎉 Cleanup complete! Abstract principles have been removed.");
        println!("   Think AI should now provide proper specific answers instead of generic abstractions.");
    } else {
        println!("✅ No problematic abstract principles found. Knowledge base is clean!");
    Ok(())
}
