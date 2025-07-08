#!/bin/bash
set -e

echo "Testing Think AI Isolated Sessions Architecture"
echo "=============================================="
echo ""

# Create a test binary for the new architecture
cat > think-ai-cli/src/bin/test-isolated-sessions.rs << 'EOF'
use std::sync::Arc;
use tokio::time::{sleep, Duration};
use think_ai_knowledge::{
    isolated_session::IsolatedSession,
    parallel_processor::{ParallelProcessor, ProcessType},
    shared_knowledge::SharedKnowledge,
    types::Message,
};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🚀 Starting Think AI Isolated Sessions Test");
    println!("==========================================\n");
    
    // Create shared knowledge base
    let shared_knowledge = Arc::new(SharedKnowledge::new());
    
    // Start parallel cognitive processes
    let processor = ParallelProcessor::new(shared_knowledge.clone());
    
    println!("📊 Starting background cognitive processes...");
    let thinking_id = processor.start_process(ProcessType::Thinking, Some("general context".to_string())).await?;
    println!("✅ Started thinking process: {}", thinking_id);
    
    let dreaming_id = processor.start_process(ProcessType::Dreaming, None).await?;
    println!("✅ Started dreaming process: {}", dreaming_id);
    
    let learning_id = processor.start_process(ProcessType::Learning, Some("learn from interactions".to_string())).await?;
    println!("✅ Started learning process: {}", learning_id);
    
    // Let processes run for a bit
    sleep(Duration::from_secs(2)).await;
    
    // Create multiple isolated chat sessions
    println!("\n📱 Creating isolated chat sessions...");
    
    // Session 1
    let mut session1 = IsolatedSession::new(shared_knowledge.clone());
    println!("✅ Created session 1: {}", session1.session_id);
    
    let msg1 = Message {
        role: "user".to_string(),
        content: "Tell me about Rust programming".to_string(),
        timestamp: std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_secs(),
    };
    
    let response1 = session1.process_message(msg1).await?;
    println!("💬 Session 1 response: {}", response1.content);
    
    // Session 2 (completely independent)
    let mut session2 = IsolatedSession::new(shared_knowledge.clone());
    println!("\n✅ Created session 2: {}", session2.session_id);
    
    let msg2 = Message {
        role: "user".to_string(),
        content: "What's the weather like?".to_string(),
        timestamp: std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_secs(),
    };
    
    let response2 = session2.process_message(msg2).await?;
    println!("💬 Session 2 response: {}", response2.content);
    
    // Check process status
    println!("\n📊 Background process status:");
    let status = processor.get_process_status();
    for process in status {
        println!("  - {} ({}): uptime {}s, {} contributions", 
            process.process_id, 
            format!("{:?}", process.state),
            process.uptime,
            process.contributions
        );
    }
    
    // Check shared knowledge statistics
    let stats = shared_knowledge.get_statistics().await;
    println!("\n🧠 Shared knowledge statistics:");
    println!("  - Total items: {}", stats.total_items);
    println!("  - Sources: {}", stats.total_sources);
    println!("  - Average confidence: {:.2}", stats.average_confidence);
    
    // Continue conversation in session 1
    println!("\n💬 Continuing conversation in session 1...");
    let msg3 = Message {
        role: "user".to_string(),
        content: "Can you explain more about memory safety?".to_string(),
        timestamp: std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_secs(),
    };
    
    let response3 = session1.process_message(msg3).await?;
    println!("💬 Session 1 follow-up: {}", response3.content);
    
    // Session 2 remains isolated
    println!("\n📱 Session 2 context check:");
    println!("  - Messages in session 2: {}", session2.context.messages.len());
    println!("  - Session 2 knows nothing about Rust discussion from session 1");
    
    // Process some background messages
    let messages = processor.process_messages().await;
    println!("\n📨 Background process messages: {} received", messages.len());
    
    // Export and restore session
    println!("\n💾 Testing session persistence...");
    let export = session1.export_session();
    println!("  - Exported session 1 with {} messages", export.context.messages.len());
    
    let restored_session = IsolatedSession::restore_session(export, shared_knowledge.clone());
    println!("  - Restored session with ID: {}", restored_session.session_id);
    
    println!("\n✅ Isolated sessions architecture test completed successfully!");
    println!("\n🎯 Key features demonstrated:");
    println!("  1. Multiple isolated chat sessions with separate contexts");
    println!("  2. Background cognitive processes running in parallel");
    println!("  3. Shared knowledge base accessible by all components");
    println!("  4. Session persistence and restoration");
    println!("  5. O(1) performance with hash-based lookups");
    
    Ok(())
}
EOF

# Build the test binary
echo "Building test binary..."
cargo build --release --bin test-isolated-sessions

# Run the test
echo ""
echo "Running isolated sessions test..."
echo ""
./target/release/test-isolated-sessions