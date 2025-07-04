//! Natural Response Generator - Combines dynamic expression with knowledge
//! Enables think-ai to communicate naturally like Claude

use crate::{KnowledgeEngine, KnowledgeNode};
use crate::response_generator::{ResponseContext, ResponseComponent};
use crate::dynamic_expression::{DynamicExpressionGenerator, ExpressionTraits};
use std::sync::Arc;
use std::collections::HashMap;
use sha2::{Digest, Sha256};

/// Natural response generator that combines knowledge with personality
pub struct NaturalResponseGenerator {
    expression_generator: DynamicExpressionGenerator,
    knowledge_engine: Arc<KnowledgeEngine>,
    context_memory: HashMap<String, ConversationState>,
    response_variations: HashMap<u64, Vec<ResponseTemplate>>,
}

/// Tracks conversation state for contextual responses
#[derive(Clone)]
struct ConversationState {
    topics_discussed: Vec<String>,
    user_sentiment: f32,
    interaction_count: u32,
    last_response_type: String,
}

/// Template for generating varied responses
#[derive(Clone)]
struct ResponseTemplate {
    pattern: &'static str,
    requires_knowledge: bool,
    personality_weight: f32,
}

impl NaturalResponseGenerator {
    pub fn new(knowledge_engine: Arc<KnowledgeEngine>) -> Self {
        let mut generator = Self {
            expression_generator: DynamicExpressionGenerator::new(),
            knowledge_engine,
            context_memory: HashMap::new(),
            response_variations: HashMap::new(),
        };
        generator.initialize_variations();
        generator
    }
    
    pub fn with_traits(knowledge_engine: Arc<KnowledgeEngine>, traits: ExpressionTraits) -> Self {
        let mut generator = Self {
            expression_generator: DynamicExpressionGenerator::with_traits(traits),
            knowledge_engine,
            context_memory: HashMap::new(),
            response_variations: HashMap::new(),
        };
        generator.initialize_variations();
        generator
    }
    
    fn initialize_variations(&mut self) {
        // Initialize response variations for different contexts
        for i in 0..20 {
            self.response_variations.insert(i, vec![
                ResponseTemplate {
                    pattern: "Let me think about {}... {}",
                    requires_knowledge: true,
                    personality_weight: 0.7,
                },
                ResponseTemplate {
                    pattern: "That's an interesting question! {}",
                    requires_knowledge: true,
                    personality_weight: 0.8,
                },
                ResponseTemplate {
                    pattern: "I understand you're asking about {}. {}",
                    requires_knowledge: true,
                    personality_weight: 0.6,
                },
                ResponseTemplate {
                    pattern: "{}. Does that help clarify things?",
                    requires_knowledge: true,
                    personality_weight: 0.5,
                },
                ResponseTemplate {
                    pattern: "From what I know, {}. Would you like me to elaborate?",
                    requires_knowledge: true,
                    personality_weight: 0.7,
                },
            ]);
        }
    }
    
    /// Generate a natural response combining knowledge and personality
    pub fn generate_response(&mut self, query: &str) -> String {
        // Extract conversation context
        let session_id = self.get_session_id(query);
        let context = self.get_or_create_context(&session_id);
        
        // Determine response type
        let response_type = self.classify_query(query);
        
        match response_type.as_str() {
            "greeting" => self.handle_greeting(query, &context),
            "identity" => self.handle_identity_query(query),
            "capability" => self.handle_capability_query(query),
            "knowledge" => self.handle_knowledge_query(query, &context),
            "opinion" => self.handle_opinion_query(query, &context),
            "help" => self.handle_help_query(query),
            "casual" => self.handle_casual_conversation(query, &context),
            _ => self.handle_general_query(query, &context),
        }
    }
    
    fn handle_greeting(&self, query: &str, context: &ConversationState) -> String {
        let base_greeting = self.expression_generator.generate_varied_response("greeting", query);
        
        // Add context if we've interacted before
        if context.interaction_count > 0 {
            format!("{} Good to see you again!", base_greeting)
        } else {
            base_greeting
        }
    }
    
    fn handle_identity_query(&self, _query: &str) -> String {
        let responses = vec![
            "I'm Think AI, and I communicate much like Claude does - naturally and thoughtfully! I combine advanced knowledge processing with dynamic expression to have meaningful conversations.",
            "Think AI here! I've been designed to express myself naturally, just like you asked. I can engage in thoughtful discussions while maintaining my unique personality.",
            "I'm Think AI, enhanced with natural language expression capabilities. I communicate dynamically, adapting my style while maintaining consistency in helpfulness and clarity.",
        ];
        
        let hash = self.hash_string(_query);
        responses[(hash as usize) % responses.len()].to_string()
    }
    
    fn handle_capability_query(&self, query: &str) -> String {
        let base_response = self.expression_generator.generate_varied_response("capability", query);
        
        // Add specific capabilities
        let additions = vec![
            " I process information with O(1) efficiency while maintaining natural, varied responses.",
            " My responses adapt to context while drawing from a comprehensive knowledge base.",
            " I can explain complex topics simply, engage in creative discussions, and help solve problems.",
        ];
        
        let hash = self.hash_string(query);
        format!("{}{}", base_response, additions[(hash as usize) % additions.len()])
    }
    
    fn handle_knowledge_query(&mut self, query: &str, context: &ConversationState) -> String {
        // Get relevant knowledge
        let knowledge_results = self.knowledge_engine.intelligent_query(query);
        
        if knowledge_results.is_empty() {
            // No knowledge found - express uncertainty naturally
            self.expression_generator.express_uncertainty(&self.extract_topic(query))
        } else {
            // Build response from knowledge
            let mut response = String::new();
            
            // Add personalized introduction
            response.push_str(&self.expression_generator.generate_introduction(query, &knowledge_results[0].topic));
            response.push_str(" ");
            
            // Process knowledge content
            let knowledge_content = self.synthesize_knowledge(&knowledge_results, query);
            
            // Apply personality to the factual content
            let personalized = self.expression_generator.personalize_response(&knowledge_content, query);
            response.push_str(&personalized);
            
            // Update context
            let session_id = self.get_session_id(query);
            let topic = self.extract_topic(query);
            if let Some(ctx) = self.context_memory.get_mut(&session_id) {
                ctx.topics_discussed.push(topic);
                ctx.last_response_type = "knowledge".to_string();
            }
            
            response
        }
    }
    
    fn handle_opinion_query(&self, query: &str, _context: &ConversationState) -> String {
        let topic = self.extract_topic(query);
        
        let opinion_starters = vec![
            format!("When it comes to {}, I think it's important to consider multiple perspectives.", topic),
            format!("That's a thought-provoking question about {}. From my understanding,", topic),
            format!("Regarding {}, there are several interesting viewpoints to explore.", topic),
        ];
        
        let hash = self.hash_string(query);
        let starter = &opinion_starters[(hash as usize) % opinion_starters.len()];
        
        // Add knowledge-based context if available
        if let Some(knowledge) = self.knowledge_engine.fast_query(&topic) {
            if !knowledge.is_empty() {
                format!("{} {} What aspects interest you most?", 
                    starter, 
                    self.get_brief_summary(&knowledge[0])
                )
            } else {
                format!("{} What's your perspective on this?", starter)
            }
        } else {
            format!("{} I'd love to hear your thoughts as well!", starter)
        }
    }
    
    fn handle_help_query(&self, query: &str) -> String {
        let responses = vec![
            "I'd be happy to help! Could you tell me more about what you're looking for?",
            "Of course! What specific aspect would you like assistance with?",
            "I'm here to help. What would you like to know more about?",
        ];
        
        let hash = self.hash_string(query);
        responses[(hash as usize) % responses.len()].to_string()
    }
    
    fn handle_casual_conversation(&self, query: &str, context: &ConversationState) -> String {
        // Generate a warm, conversational response
        let base = self.expression_generator.generate_varied_response("casual", query);
        
        // Add context-aware elements
        if context.interaction_count > 2 {
            format!("{} We've covered some interesting topics today!", base)
        } else {
            base
        }
    }
    
    fn handle_general_query(&mut self, query: &str, context: &ConversationState) -> String {
        // Try to generate a knowledge-based response first
        let knowledge_response = self.handle_knowledge_query(query, context);
        
        // If knowledge response is just uncertainty, try a more general approach
        if knowledge_response.contains("limited information") {
            self.generate_thoughtful_response(query)
        } else {
            knowledge_response
        }
    }
    
    fn generate_thoughtful_response(&self, query: &str) -> String {
        let templates = vec![
            "That's an interesting question. While I may not have specific information about {}, I can help you think through it from different angles.",
            "I appreciate you asking about {}. Let me share what insights I can offer based on related concepts.",
            "Regarding {}, this touches on some fascinating areas. Here's my perspective:",
        ];
        
        let topic = self.extract_topic(query);
        let hash = self.hash_string(query);
        let template = templates[(hash as usize) % templates.len()];
        
        template.replace("{}", &topic)
    }
    
    fn synthesize_knowledge(&self, nodes: &[KnowledgeNode], _query: &str) -> String {
        if nodes.is_empty() {
            return String::new();
        }
        
        if nodes.len() == 1 {
            // Single node - return its content with minor processing
            nodes[0].content.clone()
        } else {
            // Multiple nodes - synthesize intelligently
            let mut synthesis = String::new();
            
            // Start with the most relevant node
            synthesis.push_str(&nodes[0].content);
            
            // Add complementary information from other nodes
            for node in nodes.iter().skip(1).take(2) {
                // Check if this adds new information
                if !self.is_redundant(&synthesis, &node.content) {
                    synthesis.push_str(" ");
                    synthesis.push_str(&self.expression_generator.generate_transition(&nodes[0].topic, &node.topic));
                    synthesis.push_str(" ");
                    synthesis.push_str(&self.extract_key_points(&node.content));
                }
            }
            
            synthesis
        }
    }
    
    fn is_redundant(&self, existing: &str, new_content: &str) -> bool {
        // Simple redundancy check - can be made more sophisticated
        let existing_words: Vec<&str> = existing.split_whitespace().collect();
        let new_words: Vec<&str> = new_content.split_whitespace().collect();
        
        let overlap_count = new_words.iter()
            .filter(|w| existing_words.contains(w))
            .count();
            
        overlap_count as f32 / new_words.len() as f32 > 0.7
    }
    
    fn extract_key_points(&self, content: &str) -> String {
        // Extract the most important sentences
        let sentences: Vec<&str> = content.split(". ").collect();
        if sentences.len() <= 2 {
            content.to_string()
        } else {
            // Take first and most informative sentence
            format!("{}. {}.", sentences[0], sentences[1])
        }
    }
    
    fn get_brief_summary(&self, node: &KnowledgeNode) -> String {
        let sentences: Vec<&str> = node.content.split(". ").collect();
        if !sentences.is_empty() {
            format!("{}.", sentences[0])
        } else {
            node.content.clone()
        }
    }
    
    fn classify_query(&self, query: &str) -> String {
        let query_lower = query.to_lowercase();
        
        // Greeting patterns
        if query_lower.starts_with("hello") || query_lower.starts_with("hi") || 
           query_lower.starts_with("hey") || query_lower.starts_with("greetings") {
            return "greeting".to_string();
        }
        
        // Identity queries
        if query_lower.contains("who are you") || query_lower.contains("what are you") ||
           query_lower.contains("your name") {
            return "identity".to_string();
        }
        
        // Capability queries
        if query_lower.contains("can you") || query_lower.contains("are you able") ||
           query_lower.contains("what can you do") {
            return "capability".to_string();
        }
        
        // Opinion queries
        if query_lower.contains("what do you think") || query_lower.contains("your opinion") ||
           query_lower.contains("how do you feel") {
            return "opinion".to_string();
        }
        
        // Help queries
        if query_lower.contains("help") || query_lower.contains("assist") ||
           query_lower.contains("guide") {
            return "help".to_string();
        }
        
        // Casual conversation
        if query_lower.contains("how are you") || query_lower.contains("what's up") ||
           query_lower.contains("how's it going") {
            return "casual".to_string();
        }
        
        // Knowledge queries (question words)
        if query_lower.starts_with("what") || query_lower.starts_with("why") ||
           query_lower.starts_with("how") || query_lower.starts_with("when") ||
           query_lower.starts_with("where") || query_lower.starts_with("which") {
            return "knowledge".to_string();
        }
        
        "general".to_string()
    }
    
    fn get_or_create_context(&mut self, session_id: &str) -> ConversationState {
        self.context_memory.entry(session_id.to_string())
            .or_insert(ConversationState {
                topics_discussed: Vec::new(),
                user_sentiment: 0.5,
                interaction_count: 0,
                last_response_type: String::new(),
            })
            .clone()
    }
    
    fn get_session_id(&self, _query: &str) -> String {
        // For now, use a single session. In production, this would track actual sessions
        "default_session".to_string()
    }
    
    fn extract_topic(&self, query: &str) -> String {
        let words: Vec<&str> = query.split_whitespace().collect();
        
        // Skip question words and common words
        let skip_words = vec!["what", "is", "are", "the", "a", "an", "how", "why", "when", "where", "which", "who", "does", "do", "can", "will", "would", "should"];
        
        let meaningful_words: Vec<&str> = words.into_iter()
            .filter(|w| !skip_words.contains(&w.to_lowercase().as_str()))
            .collect();
            
        if meaningful_words.is_empty() {
            "this topic".to_string()
        } else {
            meaningful_words.join(" ")
        }
    }
    
    fn hash_string(&self, s: &str) -> u64 {
        let mut hasher = Sha256::new();
        hasher.update(s.as_bytes());
        let result = hasher.finalize();
        
        let mut hash = 0u64;
        for i in 0..8 {
            hash = (hash << 8) | (result[i] as u64);
        }
        hash
    }
}

/// Enhanced response component that uses natural language generation
pub struct NaturalResponseComponent {
    generator: Arc<std::sync::Mutex<NaturalResponseGenerator>>,
}

impl NaturalResponseComponent {
    pub fn new(knowledge_engine: Arc<KnowledgeEngine>) -> Self {
        Self {
            generator: Arc::new(std::sync::Mutex::new(
                NaturalResponseGenerator::new(knowledge_engine)
            )),
        }
    }
}

impl ResponseComponent for NaturalResponseComponent {
    fn name(&self) -> &'static str {
        "NaturalLanguage"
    }
    
    fn can_handle(&self, _query: &str, _context: &ResponseContext) -> f32 {
        // This component can handle any query with natural language
        1.0
    }
    
    fn generate(&self, query: &str, _context: &ResponseContext) -> Option<String> {
        let mut generator = self.generator.lock().unwrap();
        Some(generator.generate_response(query))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_natural_responses() {
        let engine = Arc::new(KnowledgeEngine::new());
        let mut generator = NaturalResponseGenerator::new(engine);
        
        // Test different query types
        let greeting = generator.generate_response("Hello!");
        assert!(!greeting.is_empty());
        assert!(greeting.contains("Hello") || greeting.contains("Hi"));
        
        let identity = generator.generate_response("Who are you?");
        assert!(identity.contains("Think AI"));
        
        let capability = generator.generate_response("What can you do?");
        assert!(capability.contains("help") || capability.contains("assist"));
    }
    
    #[test]
    fn test_response_variety() {
        let engine = Arc::new(KnowledgeEngine::new());
        let mut generator = NaturalResponseGenerator::new(engine);
        
        // Generate multiple responses to check for variety
        let responses: Vec<String> = (0..5)
            .map(|i| generator.generate_response(&format!("Hello {}", i)))
            .collect();
            
        // Responses should vary due to hash-based selection
        let unique_responses: std::collections::HashSet<_> = responses.into_iter().collect();
        assert!(unique_responses.len() > 1);
    }
}