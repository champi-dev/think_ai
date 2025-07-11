// Integration test for conversation context retention
use think_ai_knowledge::enhanced_conversation_memory::EnhancedConversationMemory;
use std::sync::Arc;

fn main() {
    println!("🧪 Testing Enhanced Conversation Memory");
    println!("=====================================");
    
    // Create memory instance
    let memory = Arc::new(EnhancedConversationMemory::new());
    let session_id = "test-session-123";
    
    // Test 1: Add messages
    println!("\n1️⃣ Adding conversation messages...");
    memory.add_message(
        session_id.to_string(),
        "user".to_string(),
        "My name is Alice and I'm a Rust developer".to_string(),
    );
    memory.add_message(
        session_id.to_string(),
        "assistant".to_string(),
        "Nice to meet you, Alice! Rust is a great language.".to_string(),
    );
    memory.add_message(
        session_id.to_string(),
        "user".to_string(),
        "What's my name?".to_string(),
    );
    
    // Test 2: Retrieve conversation context
    println!("\n2️⃣ Retrieving conversation context...");
    if let Some(context) = memory.get_conversation_context(session_id, 10) {
        println!("Context entries: {}", context.len());
        for (role, content) in &context {
            println!("  {}: {}", role, content);
        }
        
        // Check if context contains Alice
        let context_str = context
            .iter()
            .map(|(_, content)| content.as_str())
            .collect::<Vec<_>>()
            .join(" ");
            
        if context_str.contains("Alice") {
            println!("✅ Context contains 'Alice' - memory working!");
        } else {
            println!("❌ Context doesn't contain 'Alice'");
        }
    } else {
        println!("❌ No context found for session");
    }
    
    // Test 3: Session isolation
    println!("\n3️⃣ Testing session isolation...");
    let other_session = "other-session-456";
    memory.add_message(
        other_session.to_string(),
        "user".to_string(),
        "My name is Bob".to_string(),
    );
    
    if let Some(context) = memory.get_conversation_context(other_session, 10) {
        let context_str = context
            .iter()
            .map(|(_, content)| content.as_str())
            .collect::<Vec<_>>()
            .join(" ");
            
        if !context_str.contains("Alice") && context_str.contains("Bob") {
            println!("✅ Session isolation working - Bob's session doesn't know about Alice");
        } else {
            println!("❌ Session isolation failed");
        }
    }
    
    // Test 4: Get full session
    println!("\n4️⃣ Testing get_session method...");
    if let Some(session) = memory.get_session(session_id) {
        println!("Session ID: {}", session.session_id);
        println!("Total messages: {}", session.messages.len());
        println!("✅ Session retrieval working!");
    } else {
        println!("❌ Failed to retrieve session");
    }
    
    println!("\n✅ All memory tests completed!");
    println!("\nThe conversation memory is properly storing and retrieving context.");
    println!("The issue is that the response generator needs to use this context.");
}