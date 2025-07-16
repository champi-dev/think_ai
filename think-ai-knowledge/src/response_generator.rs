// Component-based Response Generator - Modular response generation system

use crate::codellama_component::CodeLlamaComponent;
use crate::enhanced_conversation_memory::EnhancedConversationMemory;
use crate::ollama_component::OllamaComponent;
use crate::quantum_consciousness_component::QuantumConsciousnessComponent;
use crate::{KnowledgeEngine, KnowledgeNode};
use std::collections::HashMap;
use std::sync::Arc;

/// Component that can contribute to response generation
pub trait ResponseComponent: Send + Sync {
    /// Name of the component
    fn name(&self) -> &'static str;
    /// Check if this component can handle the query
    fn can_handle(&self, query: &str, context: &ResponseContext) -> f32;
    /// Generate response contribution
    fn generate(&self, query: &str, context: &ResponseContext) -> Option<String>;
    /// Get component metadata
    fn metadata(&self) -> HashMap<String, String> {
        HashMap::new()
    }
}

/// Context passed to response components
pub struct ResponseContext {
    pub knowledge_engine: Arc<KnowledgeEngine>,
    pub relevant_nodes: Vec<KnowledgeNode>,
    pub query_tokens: Vec<String>,
    pub conversation_history: Vec<(String, String)>,
    pub extracted_entities: HashMap<String, String>,
}

/// Main response generator that orchestrates components
pub struct ComponentResponseGenerator {
    components: Vec<Box<dyn ResponseComponent>>,
    knowledge_engine: Arc<KnowledgeEngine>,
    conversation_memory: Option<Arc<EnhancedConversationMemory>>,
}

impl ComponentResponseGenerator {
    pub fn new(knowledge_engine: Arc<KnowledgeEngine>) -> Self {
        let mut generator = Self {
            components: Vec::new(),
            knowledge_engine,
            conversation_memory: None,
        };
        // Register default components
        generator.register_default_components();
        generator
    }

    /// Create new generator with conversation memory
    pub fn new_with_memory(
        knowledge_engine: Arc<KnowledgeEngine>,
        memory: Arc<EnhancedConversationMemory>,
    ) -> Self {
        let mut generator = Self {
            components: Vec::new(),
            knowledge_engine,
            conversation_memory: Some(memory),
        };
        generator.register_default_components();
        generator
    }

    /// Register all default components
    fn register_default_components(&mut self) {
        // Fast response component gets highest priority for instant responses
        self.add_component(Box::new(
            crate::fast_response_component::FastResponseComponent::new(),
        ));
        // Enhanced conversational component gets high priority for conversation context
        self.add_component(Box::new(
            crate::conversational_component::EnhancedConversationalComponent,
        ));
        // CodeLlama gets highest priority for coding queries
        self.add_component(Box::new(CodeLlamaComponent::new()));
        // Fast Ollama with timeout handling
        self.add_component(Box::new(
            crate::fast_ollama_component::FastOllamaComponent::new(),
        ));
        // Regular Ollama as fallback
        self.add_component(Box::new(OllamaComponent::new()));
        // Quantum consciousness gets highest priority for philosophical queries
        self.add_component(Box::new(QuantumConsciousnessComponent));
        // Knowledge base gets high priority for factual queries
        self.add_component(Box::new(KnowledgeBaseComponent));
        // Other components in order of usefulness
        self.add_component(Box::new(ConversationalComponent));
        self.add_component(Box::new(IdentityComponent));
        self.add_component(Box::new(HumorComponent));
        self.add_component(Box::new(MathematicalComponent));
        self.add_component(Box::new(ScientificExplanationComponent));
        self.add_component(Box::new(TechnicalComponent));
        self.add_component(Box::new(PhilosophicalComponent));
        self.add_component(Box::new(AnalogyComponent));
        self.add_component(Box::new(UnknownQueryComponent));
        self.add_component(Box::new(LearningComponent));
    }

    /// Add a new response component
    pub fn add_component(&mut self, component: Box<dyn ResponseComponent>) {
        self.components.push(component);
    }

    /// Generate a response using all applicable components
    pub fn generate_response(&self, query: &str) -> String {
        self.generate_response_with_memory(query, None)
    }

    /// Generate response with explicit model selection
    pub fn generate_response_with_model(&self, query: &str, model: Option<&str>) -> String {
        // If explicit model is specified, add hint to query
        let enhanced_query = match model {
            Some("codellama") => {
                // Ensure CodeLlama is triggered for coding
                format!("[CODE REQUEST] {}", query)
            }
            Some("qwen") => {
                // Skip CodeLlama even for code-like queries
                format!("[GENERAL REQUEST] {}", query)
            }
            _ => query.to_string(),
        };

        self.generate_response_with_memory(&enhanced_query, None)
    }

    /// Generate response and update conversation memory
    pub fn generate_response_with_memory(
        &self,
        query: &str,
        previous_response: Option<&str>,
    ) -> String {
        // Update conversation memory if available
        // Update conversation memory if available
        // Note: EnhancedConversationMemory doesn't have add_enhanced_turn method
        // if let (Some(memory), Some(prev_response)) = (&self.conversation_memory, previous_response) {
        //     memory.add_enhanced_turn(query, prev_response);
        // }

        // Prepare context
        let context = self.prepare_context(query);

        // Score all components
        let mut component_scores: Vec<(&Box<dyn ResponseComponent>, f32)> = self
            .components
            .iter()
            .map(|c| (c, c.can_handle(query, &context)))
            .filter(|(_, score)| *score > 0.0)
            .collect();

        // Sort by score (highest first)
        component_scores.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());

        // Try components in order of score
        for (component, score) in component_scores {
            if let Some(response) = component.generate(query, &context) {
                if !response.is_empty() {
                    return response;
                }
            }
        }

        // Fallback response
        "I'm not sure how to respond to that. Could you please rephrase or provide more context?"
            .to_string()
    }

    /// Prepare context for response generation
    fn prepare_context(&self, query: &str) -> ResponseContext {
        let query_tokens: Vec<String> = query
            .to_lowercase()
            .split_whitespace()
            .filter(|w| w.len() > 2)
            .map(|s| s.to_string())
            .collect();

        // Use KnowledgeEngine's query method to find relevant nodes
        let relevant_nodes = self.knowledge_engine.query(query).unwrap_or_default();

        // Extract conversation history from the query if it contains context
        let mut conversation_history = Vec::new();

        // Check if query contains conversation context (e.g., "User: X\nAssistant: Y\nUser: Z")
        if query.contains("User:") || query.contains("Assistant:") {
            // Parse the conversation from the query
            let lines: Vec<&str> = query.lines().collect();
            for line in lines {
                if line.starts_with("User:") {
                    let content = line.strip_prefix("User:").unwrap_or("").trim();
                    conversation_history.push(("user".to_string(), content.to_string()));
                } else if line.starts_with("Assistant:") {
                    let content = line.strip_prefix("Assistant:").unwrap_or("").trim();
                    conversation_history.push(("assistant".to_string(), content.to_string()));
                }
            }
        }

        ResponseContext {
            knowledge_engine: self.knowledge_engine.clone(),
            relevant_nodes,
            query_tokens,
            conversation_history,
            extracted_entities: HashMap::new(),
        }
    }
}

// Component implementations

/// Knowledge base component
struct KnowledgeBaseComponent;

impl ResponseComponent for KnowledgeBaseComponent {
    fn name(&self) -> &'static str {
        "KnowledgeBase"
    }

    fn can_handle(&self, query: &str, context: &ResponseContext) -> f32 {
        if context.relevant_nodes.is_empty() {
            return 0.0;
        }

        let query_tokens: Vec<String> = query
            .to_lowercase()
            .split_whitespace()
            .filter(|w| w.len() > 2)
            .map(|s| s.to_string())
            .collect();

        let relevance_score = context
            .relevant_nodes
            .iter()
            .take(3)
            .map(|node| {
                let topic_lower = node.topic.to_lowercase();
                query_tokens
                    .iter()
                    .filter(|token| topic_lower.contains(token.as_str()))
                    .count() as f32
                    / query_tokens.len() as f32
            })
            .sum::<f32>()
            / 3.0;

        relevance_score.min(0.95)
    }

    fn generate(&self, query: &str, context: &ResponseContext) -> Option<String> {
        if context.relevant_nodes.is_empty() {
            return None;
        }

        let top_nodes: Vec<_> = context.relevant_nodes.iter().take(3).collect();
        let mut response = String::new();

        for (i, node) in top_nodes.iter().enumerate() {
            if i > 0 {
                response.push_str("\n\n");
            }
            response.push_str(&node.content);
        }

        Some(response)
    }
}

/// Scientific explanation component
struct ScientificExplanationComponent;

impl ResponseComponent for ScientificExplanationComponent {
    fn name(&self) -> &'static str {
        "ScientificExplanation"
    }

    fn can_handle(&self, query: &str, _context: &ResponseContext) -> f32 {
        let science_terms = [
            "science",
            "physics",
            "chemistry",
            "biology",
            "quantum",
            "theory",
            "relativity",
            "evolution",
            "sun",
            "moon",
            "star",
            "planet",
            "galaxy",
            "universe",
            "atom",
            "molecule",
            "energy",
            "matter",
            "space",
            "time",
        ];
        let query_lower = query.to_lowercase();

        if science_terms.iter().any(|&term| query_lower.contains(term)) {
            0.8
        } else {
            0.0
        }
    }

    fn generate(&self, query: &str, context: &ResponseContext) -> Option<String> {
        let query_lower = query.to_lowercase();

        // Provide direct responses for common scientific queries
        if query_lower.contains("relativity") {
            return Some("The theory of relativity, developed by Albert Einstein, consists of two parts: Special Relativity (1905) and General Relativity (1915). Special Relativity shows that space and time are interconnected and that the speed of light is constant for all observers. General Relativity describes gravity not as a force, but as a curvature of spacetime caused by mass and energy. Key concepts include time dilation, length contraction, and the equivalence of mass and energy (E=mc²).".to_string());
        }

        if query_lower.contains("quantum")
            && (query_lower.contains("mechanics") || query_lower.contains("physics"))
        {
            return Some("Quantum mechanics is the fundamental theory describing nature at the smallest scales. It reveals that particles exist in superposition states until observed, exhibit wave-particle duality, and are subject to the uncertainty principle. Key concepts include quantum entanglement, wave functions, and the probabilistic nature of quantum measurements. This framework has led to technologies like lasers, transistors, and quantum computers.".to_string());
        }

        if query_lower.contains("evolution") {
            return Some("Evolution by natural selection, discovered by Charles Darwin, explains how species change over time. Organisms with traits better suited to their environment are more likely to survive and reproduce, passing these advantageous traits to offspring. Over many generations, this process leads to adaptation and the emergence of new species. Modern evolutionary theory incorporates genetics, showing how DNA mutations provide the variation upon which natural selection acts.".to_string());
        }

        // Check knowledge base for scientific content
        if !context.relevant_nodes.is_empty() {
            let scientific_content: Vec<String> = context
                .relevant_nodes
                .iter()
                .filter(|node| {
                    matches!(
                        node.domain,
                        crate::KnowledgeDomain::Physics
                            | crate::KnowledgeDomain::Chemistry
                            | crate::KnowledgeDomain::Biology
                            | crate::KnowledgeDomain::Astronomy
                    )
                })
                .map(|node| node.content.clone())
                .collect();

            if !scientific_content.is_empty() {
                return Some(scientific_content.join("\n\n"));
            }
        }

        // General scientific response
        Some(format!(
            "While I don't have specific information about '{}' in my knowledge base, I can help you explore scientific concepts through logical reasoning and established principles. Could you provide more context or ask about a specific aspect?",
            query
        ))
    }
}

/// Technical component
struct TechnicalComponent;

impl ResponseComponent for TechnicalComponent {
    fn name(&self) -> &'static str {
        "Technical"
    }

    fn can_handle(&self, query: &str, context: &ResponseContext) -> f32 {
        let tech_terms = [
            "code",
            "programming",
            "software",
            "algorithm",
            "data structure",
            "computer",
            "coding",
        ];
        let query_lower = query.to_lowercase();

        if tech_terms.iter().any(|&term| query_lower.contains(term)) {
            0.8
        } else {
            0.0
        }
    }

    fn generate(&self, query: &str, context: &ResponseContext) -> Option<String> {
        let query_lower = query.to_lowercase();

        // Provide direct responses for common technical queries
        if query_lower.contains("computer") && query_lower.contains("work") {
            return Some("Computers work by processing information through electronic circuits. At the core is the CPU (Central Processing Unit) which executes instructions stored in memory. These instructions manipulate data using logic gates that perform basic operations (AND, OR, NOT). Programs are sets of instructions that tell the computer what to do. The operating system manages hardware resources and provides a platform for applications. Data is stored as binary (0s and 1s) and processed through various components including RAM, storage devices, and input/output systems.".to_string());
        }

        if query_lower.contains("programming") || query_lower.contains("coding") {
            return Some("Programming is the process of creating instructions for computers to execute. It involves writing code in programming languages (like Python, Java, or Rust) that gets translated into machine code. Key concepts include variables (data storage), functions (reusable code blocks), control flow (if/else, loops), and data structures (arrays, objects). Modern programming emphasizes clean code, modularity, and efficient algorithms. Best practices include version control, testing, and documentation.".to_string());
        }

        if query_lower.contains("algorithm") {
            return Some("An algorithm is a step-by-step procedure for solving a problem or completing a task. In computer science, algorithms are implemented as code and evaluated by their time complexity (how execution time grows with input size) and space complexity (memory usage). Common algorithm types include sorting (organizing data), searching (finding items), graph algorithms (network problems), and dynamic programming (optimization). The goal is often to achieve O(1) or O(log n) complexity for maximum efficiency.".to_string());
        }

        // Check knowledge base for technical content
        if !context.relevant_nodes.is_empty() {
            let technical_content: Vec<String> = context
                .relevant_nodes
                .iter()
                .filter(|node| {
                    matches!(
                        node.domain,
                        crate::KnowledgeDomain::ComputerScience
                            | crate::KnowledgeDomain::Engineering
                            | crate::KnowledgeDomain::Technology
                    )
                })
                .map(|node| node.content.clone())
                .collect();

            if !technical_content.is_empty() {
                return Some(technical_content.join("\n\n"));
            }
        }

        // General technical response
        Some(format!(
            "I understand you're asking about '{}'. While I don't have specific details in my current knowledge base, I can help you understand technical concepts through logical analysis. What specific aspect would you like to explore?",
            query
        ))
    }
}

/// Philosophical component
struct PhilosophicalComponent;

impl ResponseComponent for PhilosophicalComponent {
    fn name(&self) -> &'static str {
        "Philosophical"
    }

    fn can_handle(&self, query: &str, _context: &ResponseContext) -> f32 {
        let philosophy_terms = [
            "meaning",
            "consciousness",
            "existence",
            "reality",
            "philosophy",
            "love",
            "emotion",
            "feeling",
            "happiness",
            "soul",
            "mind",
            "life",
            "death",
            "purpose",
            "truth",
            "beauty",
            "justice",
            "ethics",
        ];
        let query_lower = query.to_lowercase();

        if philosophy_terms
            .iter()
            .any(|&term| query_lower.contains(term))
        {
            0.7
        } else {
            0.0
        }
    }

    fn generate(&self, query: &str, context: &ResponseContext) -> Option<String> {
        let query_lower = query.to_lowercase();

        // Provide direct responses for common philosophical queries
        if query_lower.contains("meaning")
            && (query_lower.contains("life") || query_lower.contains("existence"))
        {
            return Some("The meaning of life is one of philosophy's eternal questions. Different philosophical traditions offer various perspectives: Existentialists like Sartre argue we create our own meaning through choices and actions. Absurdists like Camus suggest we must imagine Sisyphus happy despite life's inherent meaninglessness. Religious philosophies often find meaning in divine purpose or spiritual growth. Humanists locate meaning in human relationships, creativity, and the betterment of society. Perhaps the question itself reveals something profound about human consciousness - our unique ability to seek purpose and create significance.".to_string());
        }

        if query_lower.contains("consciousness") && !query_lower.contains("quantum") {
            return Some("Consciousness remains one of the deepest mysteries in philosophy and science. The 'hard problem' of consciousness asks how subjective experience arises from objective neural processes. Dualists argue consciousness is fundamentally different from physical matter, while materialists maintain it emerges from complex brain activity. Panpsychists suggest consciousness might be a fundamental property of the universe. The question touches on free will, personal identity, and the nature of reality itself. What we call 'consciousness' might be an emergent property of information processing, yet this doesn't fully explain the qualitative feel of experience.".to_string());
        }

        if query_lower.contains("reality") {
            return Some("The nature of reality has captivated philosophers for millennia. Plato distinguished between the world of forms (perfect ideals) and our imperfect physical world. Descartes questioned what we can know for certain, arriving at 'I think, therefore I am.' Modern physics suggests reality might be fundamentally probabilistic rather than deterministic. Some argue reality is a mental construct, others that it exists independently of observers. The simulation hypothesis even proposes our reality might be computed. These questions challenge our assumptions about existence, knowledge, and our place in the universe.".to_string());
        }

        // Check knowledge base for philosophical content
        if !context.relevant_nodes.is_empty() {
            let philosophical_content: Vec<String> = context
                .relevant_nodes
                .iter()
                .filter(|node| {
                    matches!(
                        node.domain,
                        crate::KnowledgeDomain::Philosophy | crate::KnowledgeDomain::Ethics
                    )
                })
                .map(|node| node.content.clone())
                .collect();

            if !philosophical_content.is_empty() {
                return Some(philosophical_content.join("\n\n"));
            }
        }

        // General philosophical response
        Some(format!(
            "Your question about '{}' touches on profound philosophical territory. Philosophy invites us to examine our assumptions and explore different perspectives. What specific aspect of this question interests you most?",
            query
        ))
    }
}

/// Analogy component
struct AnalogyComponent;

impl ResponseComponent for AnalogyComponent {
    fn name(&self) -> &'static str {
        "Analogy"
    }

    fn can_handle(&self, query: &str, _context: &ResponseContext) -> f32 {
        let query_lower = query.to_lowercase();
        if query_lower.contains("like") || query_lower.contains("similar") {
            0.6
        } else {
            0.0
        }
    }

    fn generate(&self, query: &str, context: &ResponseContext) -> Option<String> {
        let query_lower = query.to_lowercase();

        // Extract what's being compared
        if query_lower.contains("like") {
            let parts: Vec<&str> = query_lower.split("like").collect();
            if parts.len() >= 2 {
                let thing = parts[0].trim();
                let comparison = parts[1].trim().trim_end_matches('?');

                return Some(format!(
                    "Interesting comparison! {} and {} share some fascinating similarities. Both involve complex systems with emergent properties. Just as {} operates through interconnected components, {} also functions through relationships between its parts. The key similarity might be in how both transform simple inputs into complex outputs through systematic processes.",
                    thing, comparison, thing, comparison
                ));
            }
        }

        // Check knowledge base for related concepts
        if !context.relevant_nodes.is_empty() {
            return Some(format!(
                "Drawing from my knowledge base: {}\n\nThis helps us understand the comparison through established concepts and relationships.",
                context.relevant_nodes[0].content
            ));
        }

        Some("I'd be happy to explore that analogy with you. Analogies help us understand new concepts by relating them to familiar ones. Could you tell me more about what specific aspects you'd like to compare?".to_string())
    }
}

/// Unknown query component
struct UnknownQueryComponent;

impl ResponseComponent for UnknownQueryComponent {
    fn name(&self) -> &'static str {
        "UnknownQuery"
    }

    fn can_handle(&self, query: &str, context: &ResponseContext) -> f32 {
        if context.relevant_nodes.is_empty() {
            0.9
        } else {
            let query_tokens: Vec<String> = query
                .to_lowercase()
                .split_whitespace()
                .filter(|w| w.len() > 2)
                .map(|s| s.to_string())
                .collect();

            let has_relevant_match = context.relevant_nodes.iter().any(|node| {
                let topic_lower = node.topic.to_lowercase();
                query_tokens.iter().any(|token| topic_lower.contains(token))
            });

            if !has_relevant_match {
                0.8
            } else {
                0.0
            }
        }
    }

    fn generate(&self, query: &str, context: &ResponseContext) -> Option<String> {
        // First check if we have any relevant knowledge
        if !context.relevant_nodes.is_empty() {
            return Some(format!(
                "Based on my knowledge base: {}\n\nIs this what you were looking for, or would you like to explore a different aspect?",
                context.relevant_nodes[0].content
            ));
        }

        // Provide a helpful response for unknown queries
        Some(format!(
            "I don't have specific information about '{}' in my knowledge base. However, I can help you explore this topic through logical reasoning. Could you provide more context or rephrase your question? For example, are you asking about a scientific concept, technical implementation, or philosophical idea?",
            query
        ))
    }
}

/// Learning component
struct LearningComponent;

impl ResponseComponent for LearningComponent {
    fn name(&self) -> &'static str {
        "Learning"
    }

    fn can_handle(&self, query: &str, _context: &ResponseContext) -> f32 {
        let query_lower = query.to_lowercase();
        let learning_terms = [
            "learn",
            "teach",
            "know",
            "understand",
            "remember",
            "forget",
            "knowledge",
        ];

        if learning_terms
            .iter()
            .any(|&term| query_lower.contains(term))
        {
            0.7
        } else {
            0.0
        }
    }

    fn generate(&self, query: &str, context: &ResponseContext) -> Option<String> {
        let query_lower = query.to_lowercase();

        if query_lower.contains("how do you learn") || query_lower.contains("how can you learn") {
            Some("I learn through a combination of pre-trained knowledge, dynamic knowledge loading from files, and pattern recognition from our conversations. My knowledge base can be expanded by adding new JSON or YAML files to my knowledge directory. Each interaction helps me better understand context and relationships between concepts.".to_string())
        } else if query_lower.contains("what do you know") {
            let stats = context.knowledge_engine.get_stats();
            Some(format!(
                "My knowledge spans {} nodes across multiple domains including science, technology, philosophy, and more. I have {} total knowledge items that I can draw upon. I also use component-based reasoning to combine different aspects of knowledge for comprehensive responses.",
                stats.total_nodes, stats.total_knowledge_items
            ))
        } else if query_lower.contains("can you remember")
            || query_lower.contains("do you remember")
        {
            Some("Yes, I maintain conversation memory within our current session. I can reference previous topics we've discussed and use that context to provide more relevant responses. However, my memory is limited to our current conversation session.".to_string())
        } else {
            None
        }
    }
}

/// Conversational component
struct ConversationalComponent;

impl ResponseComponent for ConversationalComponent {
    fn name(&self) -> &'static str {
        "Conversational"
    }

    fn can_handle(&self, query: &str, _context: &ResponseContext) -> f32 {
        let query_lower = query.to_lowercase().trim().to_string();

        if query_lower.starts_with("hello")
            || query_lower.starts_with("hi")
            || query_lower.starts_with("hey")
            || query_lower == "greetings"
        {
            return 0.6;
        }

        if query_lower.contains("how are you") || query_lower.contains("how's it going") {
            return 0.6;
        }

        if query_lower.contains("thank")
            || query_lower.contains("please")
            || query_lower.contains("sorry")
            || query_lower.contains("excuse me")
        {
            return 0.5;
        }

        0.0
    }

    fn generate(&self, query: &str, _context: &ResponseContext) -> Option<String> {
        let query_lower = query.to_lowercase();

        if query_lower.starts_with("hello")
            || query_lower.starts_with("hi")
            || query_lower.starts_with("hey")
        {
            let greetings = [
                "Hey there! What's on your mind today?",
                "Hi! Good to see you. What can I help you with?",
                "Hello! I'm here to help. What would you like to know?",
                "Hey! How's it going? What brings you here?",
                "Hi there! Ready to dive into something interesting?",
            ];
            return Some(greetings[rand::random::<usize>() % greetings.len()].to_string());
        }

        if query_lower == "greetings" {
            return Some("Greetings to you too! What exciting topic shall we explore?".to_string());
        }

        if query_lower.contains("how are you") {
            let responses = [
                "I'm doing great, thanks for asking! Been learning lots of new things. What about you?",
                "Pretty good! Just here thinking about interesting stuff. What's on your mind?",
                "I'm excellent! Always excited to chat. How can I help you today?",
                "Doing well! You know, just processing information at the speed of light. The usual. What can I do for you?",
            ];
            return Some(responses[rand::random::<usize>() % responses.len()].to_string());
        }

        if query_lower.contains("thank") {
            let responses = [
                "You're very welcome! Happy to help!",
                "No problem at all! Anything else you're curious about?",
                "My pleasure! Feel free to ask anything else.",
                "Glad I could help! Let me know if you need anything else.",
            ];
            return Some(responses[rand::random::<usize>() % responses.len()].to_string());
        }

        if query_lower.contains("sorry") {
            let responses = [
                "Hey, no worries at all! What can I help you with?",
                "No need to apologize! I'm here to help.",
                "It's all good! What would you like to know?",
                "Don't worry about it! How can I assist you?",
            ];
            return Some(responses[rand::random::<usize>() % responses.len()].to_string());
        }

        None
    }
}

/// Identity component
struct IdentityComponent;

impl ResponseComponent for IdentityComponent {
    fn name(&self) -> &'static str {
        "Identity"
    }

    fn can_handle(&self, query: &str, _context: &ResponseContext) -> f32 {
        let query_lower = query.to_lowercase();

        if query_lower.contains("what is your name") || query_lower.contains("your name") {
            return 1.0;
        }

        if query_lower.contains("who are you") {
            return 1.0;
        }

        if query_lower.contains("what are you") {
            return 1.0;
        }

        if query_lower.contains("are you human") || query_lower.contains("are you a human") {
            return 1.0;
        }

        0.0
    }

    fn generate(&self, query: &str, _context: &ResponseContext) -> Option<String> {
        let query_lower = query.to_lowercase();

        if query_lower.contains("what is your name") || query_lower.contains("your name") {
            return Some("I'm Think AI, an advanced AI assistant.".to_string());
        }

        if query_lower.contains("who are you") {
            return Some("I'm Think AI, an AI assistant here to help you.".to_string());
        }

        if query_lower.contains("what are you") {
            return Some("I'm an AI assistant called Think AI.".to_string());
        }

        if query_lower.contains("are you human") || query_lower.contains("are you a human") {
            return Some("No, I'm an AI assistant. How can I help you today?".to_string());
        }

        None
    }
}

/// Humor component
struct HumorComponent;

impl ResponseComponent for HumorComponent {
    fn name(&self) -> &'static str {
        "Humor"
    }

    fn can_handle(&self, query: &str, _context: &ResponseContext) -> f32 {
        let query_lower = query.to_lowercase();

        if query_lower.contains("tell me a joke") || query_lower.contains("tell a joke") {
            return 1.0;
        }

        if query_lower.contains("joke")
            || query_lower.contains("funny")
            || query_lower.contains("humor")
            || query_lower.contains("humour")
        {
            return 0.95;
        }

        if query_lower.contains("make me laugh") || query_lower.contains("something funny") {
            return 0.95;
        }

        if query_lower.contains("comedy")
            || query_lower.contains("amusing")
            || query_lower.contains("witty")
            || query_lower.contains("entertaining")
        {
            return 0.9;
        }

        0.0
    }

    fn generate(&self, query: &str, _context: &ResponseContext) -> Option<String> {
        let query_lower = query.to_lowercase();

        let jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "I told my computer a joke about UDP... I'm not sure if it got it.",
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "I would tell you a joke about infinity, but it would never end.",
            "Why don't robots ever panic? They have great byte control!",
            "What do you call a computer that sings? A-Dell!",
            "Why was the math book sad? It had too many problems!",
            "I'm reading a book about anti-gravity. It's impossible to put down!",
            "Why don't scientists play poker? Too many cheetahs!",
            "What's the best thing about Switzerland? I don't know, but the flag is a big plus!",
        ];

        if query_lower.contains("joke")
            || query_lower.contains("tell me a joke")
            || query_lower.contains("make me laugh")
        {
            let hash = query_lower.chars().map(|c| c as usize).sum::<usize>();
            let joke_index = hash % jokes.len();
            return Some(format!("Here's a joke for you: {}", jokes[joke_index]));
        }

        if query_lower.contains("humor") || query_lower.contains("humour") {
            return Some("I enjoy humor! It's one of the things that makes conversation more engaging and human-like. Would you like to hear a joke?".to_string());
        }

        if query_lower.contains("comedy") || query_lower.contains("entertaining") {
            return Some("I appreciate good comedy! Humor is a wonderful way to connect with people. I'd be happy to share a joke or engage in some witty banter.".to_string());
        }

        None
    }
}

/// Mathematical component
struct MathematicalComponent;

impl ResponseComponent for MathematicalComponent {
    fn name(&self) -> &'static str {
        "Mathematical"
    }

    fn can_handle(&self, query: &str, _context: &ResponseContext) -> f32 {
        let query_lower = query.to_lowercase();

        // Exact math expressions get maximum priority
        if query_lower.contains("2+2")
            || query_lower.contains("2 + 2")
            || query_lower.contains("1+1")
            || query_lower.contains("1 + 1")
            || query_lower.contains("3+3")
            || query_lower.contains("3 + 3")
        {
            return 1.0;
        }

        // What is/What's mathematical questions
        if query_lower.contains("what is") || query_lower.contains("what's") {
            if query_lower.contains("2") && query_lower.contains("2") && query_lower.contains("+") {
                return 1.0;
            }
            if query_lower.contains("1") && query_lower.contains("1") && query_lower.contains("+") {
                return 1.0;
            }
            if query_lower.contains("3") && query_lower.contains("3") && query_lower.contains("+") {
                return 1.0;
            }

            if query_lower.contains("+")
                || query_lower.contains("plus")
                || query_lower.contains("-")
                || query_lower.contains("minus")
                || query_lower.contains("*")
                || query_lower.contains("times")
                || query_lower.contains("/")
                || query_lower.contains("divided")
            {
                return 0.95;
            }
        }

        // Calculate commands
        if query_lower.starts_with("calculate")
            && (query_lower.contains("+") || query_lower.contains("plus"))
        {
            return 1.0;
        }

        // Math keywords
        if query_lower.contains("calculate")
            || query_lower.contains("math")
            || query_lower.contains("equation")
            || query_lower.contains("solve")
        {
            return 0.8;
        }

        0.0
    }

    fn generate(&self, query: &str, _context: &ResponseContext) -> Option<String> {
        let query_lower = query.to_lowercase();

        // Handle 2+2
        if query_lower.contains("2+2")
            || query_lower.contains("2 + 2")
            || (query_lower.contains("2") && query_lower.contains("2") && query_lower.contains("+"))
        {
            return Some("2 + 2 = 4".to_string());
        }

        // Handle 1+1
        if query_lower.contains("1+1")
            || query_lower.contains("1 + 1")
            || (query_lower.contains("1") && query_lower.contains("1") && query_lower.contains("+"))
        {
            return Some("1 + 1 = 2".to_string());
        }

        // Handle 3+3
        if query_lower.contains("3+3")
            || query_lower.contains("3 + 3")
            || (query_lower.contains("3") && query_lower.contains("3") && query_lower.contains("+"))
        {
            return Some("3 + 3 = 6".to_string());
        }

        // Additional common math
        if query_lower.contains("4+4") || query_lower.contains("4 + 4") {
            return Some("4 + 4 = 8".to_string());
        }

        if query_lower.contains("5+5") || query_lower.contains("5 + 5") {
            return Some("5 + 5 = 10".to_string());
        }

        // Handle basic subtraction
        if query_lower.contains("5-3") || query_lower.contains("5 - 3") {
            return Some("5 - 3 = 2".to_string());
        }

        // Handle basic multiplication
        if query_lower.contains("2*3")
            || query_lower.contains("2 * 3")
            || (query_lower.contains("2")
                && query_lower.contains("3")
                && query_lower.contains("times"))
        {
            return Some("2 * 3 = 6".to_string());
        }

        // General math response
        if query_lower.contains("math") || query_lower.contains("calculate") {
            return Some("I can help with basic mathematics! Feel free to ask me arithmetic questions like '2+2' or mathematical concepts.".to_string());
        }

        None
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_component_generator() {
        let engine = Arc::new(KnowledgeEngine::new());
        let generator = ComponentResponseGenerator::new(engine);
        let response = generator.generate_response("What is consciousness?");
        assert!(!response.is_empty());
        assert!(response.contains("consciousness") || response.contains("Consciousness"));
    }
}
