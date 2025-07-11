// Integration test for conversation context retention
use think_ai_knowledge::enhanced_conversation_memory::EnhancedConversationMemory;
use std::sync::Arc;

#[test]
fn test_conversation_memory_retention() {
    // Create memory instance
    let memory = Arc::new(EnhancedConversationMemory::new());
    let session_id = "test-session-123";
    
    // Add messages
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
    
    // Retrieve conversation context
    let context = memory.get_conversation_context(session_id, 10);
    assert!(context.is_some(), "Context should exist");
    
    let context = context.unwrap();
    assert_eq!(context.len(), 3, "Should have 3 messages");
    
    // Check if context contains Alice
    let context_str = context
        .iter()
        .map(|(_, content)| content.as_str())
        .collect::<Vec<_>>()
        .join(" ");
        
    assert!(context_str.contains("Alice"), "Context should contain 'Alice'");
    assert!(context_str.contains("Rust"), "Context should contain 'Rust'");
}

#[test]
fn test_session_isolation() {
    let memory = Arc::new(EnhancedConversationMemory::new());
    
    // Session 1
    memory.add_message(
        "session-1".to_string(),
        "user".to_string(),
        "I am Alice".to_string(),
    );
    
    // Session 2
    memory.add_message(
        "session-2".to_string(),
        "user".to_string(),
        "I am Bob".to_string(),
    );
    
    // Check isolation
    let context1 = memory.get_conversation_context("session-1", 10).unwrap();
    let context2 = memory.get_conversation_context("session-2", 10).unwrap();
    
    let context1_str = context1.iter().map(|(_, c)| c.as_str()).collect::<Vec<_>>().join(" ");
    let context2_str = context2.iter().map(|(_, c)| c.as_str()).collect::<Vec<_>>().join(" ");
    
    assert!(context1_str.contains("Alice") && !context1_str.contains("Bob"));
    assert!(context2_str.contains("Bob") && !context2_str.contains("Alice"));
}

#[test]
fn test_context_ordering() {
    let memory = Arc::new(EnhancedConversationMemory::new());
    let session_id = "test-ordering";
    
    // Add messages in order
    for i in 1..=5 {
        memory.add_message(
            session_id.to_string(),
            "user".to_string(),
            format!("Message {}", i),
        );
    }
    
    // Get last 3 messages
    let context = memory.get_conversation_context(session_id, 3).unwrap();
    assert_eq!(context.len(), 3);
    
    // Verify they are the last 3 messages in correct order
    assert!(context[0].1.contains("Message 3"));
    assert!(context[1].1.contains("Message 4"));
    assert!(context[2].1.contains("Message 5"));
}