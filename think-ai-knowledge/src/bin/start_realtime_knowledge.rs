//! Start real-time knowledge gathering service

#[cfg(feature = "web-scraping")]
use think_ai_knowledge::{KnowledgeEngine, realtime_knowledge_gatherer::{RealtimeKnowledgeGatherer, run_knowledge_gatherer}};
use std::sync::Arc;

#[tokio::main]
async fn main() {
    #[cfg(not(feature = "web-scraping"))]
    {
        println!("🌐 Think AI Real-Time Knowledge Gathering Service");
        println!("==============================================");
        println!("⚠️  Web scraping features are disabled to maintain compatibility with Rust 1.80.1");
        println!("To enable, build with: cargo build --features web-scraping");
        return;
    }
    
    #[cfg(feature = "web-scraping")]
    {
        println!("🌐 Think AI Real-Time Knowledge Gathering Service");
        println!("==============================================");
        println!("Monitoring public web sources for latest knowledge...\n");
    
    // Initialize knowledge engine
    let knowledge_engine = Arc::new(KnowledgeEngine::new());
    
    // Create real-time gatherer
    let gatherer = Arc::new(RealtimeKnowledgeGatherer::new(knowledge_engine.clone()));
    
    println!("📡 Starting background knowledge gathering...");
    println!("📰 Sources: Hacker News, Medium, Dev.to, TechCrunch, Reddit");
    println!("🔄 Update interval: 5 minutes\n");
    
    // Run the gatherer in background
    let gatherer_clone = gatherer.clone();
    let gather_task = tokio::spawn(async move {
        run_knowledge_gatherer(gatherer_clone).await;
    });
    
    // Test immediate gathering
    println!("🚀 Running initial knowledge gathering...");
    let initial_content = gatherer.gather_all().await;
    println!("✅ Gathered {} items in initial run", initial_content.len());
    
    if !initial_content.is_empty() {
        println!("\n📋 Sample gathered content:");
        for (i, content) in initial_content.iter().take(3).enumerate() {
            println!("\n{}. {}", i + 1, content.title);
            println!("   Source: {}", content.source_id);
            println!("   URL: {}", content.url);
            if let Some(date) = &content.published_date {
                println!("   Published: {}", date.format("%Y-%m-%d %H:%M"));
            }
        }
    }
    
    println!("\n💡 Knowledge gathering service is running in the background");
    println!("Press Ctrl+C to stop the service\n");
    
    // Wait for the background task
    gather_task.await.unwrap();
    }
}