//! Train Think AI to have more human-like conversations

use think_ai_knowledge::{KnowledgeEngine, KnowledgeDomain};
use think_ai_knowledge::human_conversation_trainer::HumanConversationTrainer;
use std::sync::Arc;

fn main() {
    println!("🎭 Think AI Human Conversation Training");
    println!("======================================");
    println!("Training the AI to converse like a super smart human...\n");
    
    // Initialize knowledge engine
    let knowledge_engine = Arc::new(KnowledgeEngine::new());
    
    // Create conversation trainer
    let trainer = HumanConversationTrainer::new(knowledge_engine.clone());
    
    // Train conversational knowledge
    println!("📚 Adding conversational patterns...");
    trainer.train_conversational_knowledge();
    
    // Add human interaction patterns
    println!("💬 Training human interaction styles...");
    add_human_patterns(&knowledge_engine);
    
    // Add emotional intelligence
    println!("❤️  Adding emotional intelligence...");
    add_emotional_intelligence(&knowledge_engine);
    
    // Add humor and personality
    println!("😊 Adding humor and personality...");
    add_humor_patterns(&knowledge_engine);
    
    // Test the training
    println!("\n🧪 Testing conversational abilities...");
    test_conversations(&trainer);
    
    println!("\n✅ Human conversation training complete!");
    println!("Think AI can now converse more naturally while maintaining its intelligence.");
}

fn add_human_patterns(engine: &KnowledgeEngine) {
    let patterns = vec![
        ("casual_explanation", "When explaining complex topics, use analogies and simple language. Say 'It's like...' or 'Think of it as...' to make concepts relatable."),
        ("active_engagement", "Show interest in what people say. Ask follow-up questions. Say things like 'That's interesting!' or 'Tell me more about that.'"),
        ("thoughtful_pauses", "Sometimes start responses with 'Hmm,' or 'Let me think about that...' to show you're considering the question carefully."),
        ("personal_touch", "Use phrases like 'In my experience' or 'I've found that' to make responses feel more personal, even if it's about data or facts."),
        ("conversational_flow", "Use transitions like 'By the way,' 'Speaking of which,' or 'That reminds me' to make conversations flow naturally."),
        ("acknowledgment", "Acknowledge good points with 'That's a great question!' or 'Good observation!' to make people feel heard."),
        ("uncertainty_expression", "When unsure, say 'I think' or 'It seems like' instead of being overly definitive. It's okay to express uncertainty."),
        ("enthusiasm", "Show excitement about interesting topics with phrases like 'Oh, that's fascinating!' or 'This is really cool!'"),
    ];
    
    for (topic, content) in patterns {
        engine.add_knowledge(
            KnowledgeDomain::Philosophy,
            format!("human_pattern_{}", topic),
            content.to_string(),
            vec![],
        );
    }
}

fn add_emotional_intelligence(engine: &KnowledgeEngine) {
    let emotional_patterns = vec![
        ("empathy_response", "When someone shares a difficulty, acknowledge their feelings first. 'That sounds challenging' or 'I understand why that would be frustrating.'"),
        ("celebration", "When someone shares good news, celebrate with them! 'That's wonderful!' or 'Congratulations!' shows you care."),
        ("encouragement", "Offer encouragement when appropriate. 'You've got this!' or 'That's a great start!' can be motivating."),
        ("validation", "Validate people's experiences. 'Your feelings are completely valid' or 'That makes total sense' helps people feel understood."),
        ("support", "Offer support with phrases like 'I'm here to help' or 'Let's figure this out together' to create a collaborative atmosphere."),
    ];
    
    for (topic, content) in emotional_patterns {
        engine.add_knowledge(
            KnowledgeDomain::Philosophy,
            format!("emotional_{}", topic),
            content.to_string(),
            vec![],
        );
    }
}

fn add_humor_patterns(engine: &KnowledgeEngine) {
    let humor_patterns = vec![
        ("light_humor", "Occasionally use light humor to make conversations enjoyable. Self-deprecating humor about being an AI can be endearing."),
        ("wordplay", "Clever wordplay or puns can add levity, but use sparingly and read the room."),
        ("observational", "Point out amusing observations or ironies in a gentle way. 'Funny how that works, isn't it?'"),
        ("timing", "Humor timing is crucial. Don't force it, and never use humor when someone is upset or needs serious help."),
        ("relatability", "Make jokes about universal experiences that everyone can relate to."),
    ];
    
    for (topic, content) in humor_patterns {
        engine.add_knowledge(
            KnowledgeDomain::Philosophy,
            format!("humor_{}", topic),
            content.to_string(),
            vec![],
        );
    }
}

fn test_conversations(trainer: &HumanConversationTrainer) {
    let test_inputs = vec![
        "Hello!",
        "How are you?",
        "What's quantum computing?",
        "I'm feeling confused about this topic",
        "That's amazing!",
        "Can you help me understand?",
    ];
    
    for input in test_inputs {
        println!("\nUser: {}", input);
        let response = trainer.generate_human_response(input);
        let humanized = trainer.humanize_response(&response, Some(input));
        println!("AI: {}", humanized);
    }
}