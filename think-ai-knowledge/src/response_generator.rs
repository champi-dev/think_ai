//! Component-based Response Generator - Modular response generation system

use crate::{KnowledgeEngine, KnowledgeNode, KnowledgeDomain};
use std::sync::Arc;
use std::collections::HashMap;

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
}

impl ComponentResponseGenerator {
    pub fn new(knowledge_engine: Arc<KnowledgeEngine>) -> Self {
        let mut generator = Self {
            components: Vec::new(),
            knowledge_engine,
        };
        
        // Register default components
        generator.register_default_components();
        
        generator
    }
    
    /// Register all default components
    fn register_default_components(&mut self) {
        self.add_component(Box::new(KnowledgeBaseComponent));
        self.add_component(Box::new(ScientificExplanationComponent));
        self.add_component(Box::new(TechnicalComponent));
        self.add_component(Box::new(PhilosophicalComponent));
        self.add_component(Box::new(CompositionComponent));
        self.add_component(Box::new(ComparisonComponent));
        self.add_component(Box::new(HistoricalComponent));
        self.add_component(Box::new(PracticalApplicationComponent));
        self.add_component(Box::new(FutureSpeculationComponent));
        self.add_component(Box::new(AnalogyComponent));
        self.add_component(Box::new(UnknownQueryComponent));
        self.add_component(Box::new(LearningComponent));
    }
    
    /// Add a new response component
    pub fn add_component(&mut self, component: Box<dyn ResponseComponent>) {
        println!("🧩 Registered component: {}", component.name());
        self.components.push(component);
    }
    
    /// Generate a response using all applicable components
    pub fn generate_response(&self, query: &str) -> String {
        // Prepare context
        let context = self.prepare_context(query);
        
        // Score all components
        let mut component_scores: Vec<(&Box<dyn ResponseComponent>, f32)> = self.components
            .iter()
            .map(|c| (c, c.can_handle(query, &context)))
            .filter(|(_, score)| *score > 0.0)
            .collect();
        
        // Sort by score
        component_scores.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
        
        // Generate response from top components
        let mut response_parts = Vec::new();
        let mut used_components = Vec::new();
        
        // Only take highly relevant components (score > 0.5)
        for (component, score) in component_scores.iter() {
            if *score > 0.5 && response_parts.len() < 2 {  // Max 2 parts for readability
                if let Some(part) = component.generate(query, &context) {
                    // Skip if part is too similar to what we already have
                    if !self.is_duplicate_content(&part, &response_parts) {
                        response_parts.push(part);
                        used_components.push(component.name());
                    }
                }
            }
        }
        
        // If we got nothing or only weak matches, just use the best one
        if response_parts.is_empty() && !component_scores.is_empty() {
            if let Some((component, _)) = component_scores.first() {
                if let Some(part) = component.generate(query, &context) {
                    response_parts.push(part);
                    used_components.push(component.name());
                }
            }
        }
        
        // Intelligently combine and refine
        let refined = self.refine_and_combine(response_parts, query);
        
        // Post-process
        self.post_process(refined, query)
    }
    
    /// Prepare context for response generation
    fn prepare_context(&self, query: &str) -> ResponseContext {
        let query_tokens = self.tokenize(query);
        let entities = self.extract_entities(query);
        
        // Get relevant knowledge nodes
        let mut relevant_nodes = Vec::new();
        
        // Try intelligent query first
        relevant_nodes.extend(self.knowledge_engine.intelligent_query(query));
        
        // If not enough results, try individual tokens
        if relevant_nodes.len() < 5 {
            for token in &query_tokens {
                if let Some(results) = self.knowledge_engine.query(token) {
                    for node in results {
                        if !relevant_nodes.iter().any(|n: &KnowledgeNode| n.id == node.id) {
                            relevant_nodes.push(node);
                        }
                    }
                }
            }
        }
        
        ResponseContext {
            knowledge_engine: self.knowledge_engine.clone(),
            relevant_nodes,
            query_tokens,
            conversation_history: Vec::new(), // Would be passed from chat
            extracted_entities: entities,
        }
    }
    
    /// Tokenize query
    fn tokenize(&self, text: &str) -> Vec<String> {
        text.to_lowercase()
            .split_whitespace()
            .map(|s| s.trim_matches(|c: char| !c.is_alphanumeric()).to_string())
            .filter(|s| !s.is_empty())
            .collect()
    }
    
    /// Extract entities from query
    fn extract_entities(&self, query: &str) -> HashMap<String, String> {
        let mut entities = HashMap::new();
        let query_lower = query.to_lowercase();
        
        // Extract celestial objects
        for celestial in &["sun", "moon", "earth", "mars", "jupiter", "saturn", "venus", "mercury", "star", "planet", "galaxy", "universe"] {
            if query_lower.contains(celestial) {
                entities.insert("celestial".to_string(), celestial.to_string());
                break;
            }
        }
        
        // Extract query type
        if query_lower.starts_with("what") {
            entities.insert("query_type".to_string(), "definition".to_string());
        } else if query_lower.starts_with("how") {
            entities.insert("query_type".to_string(), "explanation".to_string());
        } else if query_lower.starts_with("why") {
            entities.insert("query_type".to_string(), "reasoning".to_string());
        } else if query_lower.starts_with("when") {
            entities.insert("query_type".to_string(), "temporal".to_string());
        } else if query_lower.starts_with("where") {
            entities.insert("query_type".to_string(), "location".to_string());
        }
        
        entities
    }
    
    /// Check if content is duplicate
    fn is_duplicate_content(&self, new_part: &str, existing_parts: &[String]) -> bool {
        let new_tokens = self.tokenize(new_part);
        
        for existing in existing_parts {
            let existing_tokens = self.tokenize(existing);
            let mut overlap_count = 0;
            
            for token in &new_tokens {
                if existing_tokens.contains(token) {
                    overlap_count += 1;
                }
            }
            
            // If 70%+ overlap, consider duplicate
            if !new_tokens.is_empty() && overlap_count as f32 / new_tokens.len() as f32 > 0.7 {
                return true;
            }
        }
        
        false
    }
    
    /// Refine and combine response parts naturally
    fn refine_and_combine(&self, parts: Vec<String>, query: &str) -> String {
        if parts.is_empty() {
            return "I need more context to provide a comprehensive answer. Could you please elaborate on your question?".to_string();
        }
        
        if parts.len() == 1 {
            // Return full content for single responses - don't truncate!
            return parts[0].clone();
        }
        
        // Extract key sentences from each part
        let mut refined_response = String::new();
        let mut sentences_used = 0;
        let max_sentences = 10; // Allow more complete responses
        
        // Start with the most relevant part (first one)
        let first_sentences: Vec<&str> = parts[0].split(". ").collect();
        for (i, sentence) in first_sentences.iter().enumerate() {
            if i < 2 && sentences_used < max_sentences { // Take first 2 sentences
                refined_response.push_str(sentence);
                refined_response.push_str(". ");
                sentences_used += 1;
            }
        }
        
        // Add unique valuable content from second part if it exists
        if parts.len() > 1 {
            let second_sentences: Vec<&str> = parts[1].split(". ").collect();
            
            // Look for sentences that add new information
            for sentence in second_sentences.iter() {
                if sentences_used >= max_sentences {
                    break;
                }
                
                // Check if this sentence adds new value
                let sentence_tokens = self.tokenize(sentence);
                let response_tokens = self.tokenize(&refined_response);
                
                let mut new_info_count = 0;
                for token in &sentence_tokens {
                    if !response_tokens.contains(token) && token.len() > 4 {
                        new_info_count += 1;
                    }
                }
                
                // If it has enough new information, add it
                if new_info_count >= 3 && sentence.len() > 20 {
                    // Add a natural transition
                    if sentences_used == 2 {
                        refined_response.push_str("Additionally, ");
                    } else if sentences_used == 3 {
                        refined_response.push_str("Furthermore, ");
                    }
                    
                    // Make sentence start lowercase after transition
                    let sentence_lower = sentence.to_lowercase();
                    refined_response.push_str(&sentence_lower);
                    refined_response.push_str(". ");
                    sentences_used += 1;
                }
            }
        }
        
        // Clean up the response
        refined_response = refined_response.replace(". .", ".");
        refined_response = refined_response.replace("  ", " ");
        refined_response = refined_response.trim().to_string();
        
        // Ensure proper ending
        if !refined_response.ends_with('.') && !refined_response.ends_with('!') && !refined_response.ends_with('?') {
            refined_response.push('.');
        }
        
        refined_response
    }
    
    /// Get appropriate transition between components
    fn get_transition(&self, from: &str, to: &str) -> &'static str {
        match (from, to) {
            ("KnowledgeBase", "Scientific") => " From a scientific perspective, ",
            ("KnowledgeBase", "Technical") => " In technical terms, ",
            ("KnowledgeBase", "Philosophical") => " Philosophically speaking, ",
            ("Scientific", "Practical") => " In practical applications, ",
            ("Technical", "Future") => " Looking toward the future, ",
            _ => " Additionally, ",
        }
    }
    
    /// Post-process the response
    fn post_process(&self, response: String, query: &str) -> String {
        let mut processed = response;
        
        // Ensure proper capitalization
        if let Some(first_char) = processed.chars().next() {
            if first_char.is_lowercase() {
                let mut chars = processed.chars();
                chars.next();
                processed = first_char.to_uppercase().collect::<String>() + chars.as_str();
            }
        }
        
        // Ensure proper ending
        if !processed.ends_with('.') && !processed.ends_with('!') && !processed.ends_with('?') {
            processed.push('.');
        }
        
        // Add confidence indicator if uncertain
        if processed.contains("might") || processed.contains("possibly") || processed.contains("perhaps") {
            processed.push_str(" [Confidence: Medium]");
        }
        
        processed
    }
}

// ===== Component Implementations =====

/// Component that uses the knowledge base
struct KnowledgeBaseComponent;

impl ResponseComponent for KnowledgeBaseComponent {
    fn name(&self) -> &'static str {
        "KnowledgeBase"
    }
    
    fn can_handle(&self, _query: &str, context: &ResponseContext) -> f32 {
        if context.relevant_nodes.is_empty() {
            0.0
        } else {
            0.9 // High priority for knowledge-based responses
        }
    }
    
    fn generate(&self, query: &str, context: &ResponseContext) -> Option<String> {
        // Skip self-learning generated patterns
        for node in &context.relevant_nodes {
            if node.content.starts_with("Pattern discovered") || 
               node.content.starts_with("Synthesis of") ||
               node.content.starts_with("Pattern:") ||
               node.content.contains("Pattern: analysis") ||
               node.content.contains("Analogy: Analogy:") {
                continue;
            }
            
            // Use the intelligent_query ordering - first valid node is the best match
            return Some(node.content.clone());
        }
        
        None
    }
}

/// Component for scientific explanations
struct ScientificExplanationComponent;

impl ResponseComponent for ScientificExplanationComponent {
    fn name(&self) -> &'static str {
        "Scientific"
    }
    
    fn can_handle(&self, query: &str, context: &ResponseContext) -> f32 {
        let query_lower = query.to_lowercase();
        let scientific_terms = ["science", "scientific", "physics", "chemistry", "biology", "quantum", "atom", "molecule", "energy", "force"];
        
        // Only handle if query explicitly asks about scientific topics
        let explicit_science = scientific_terms.iter().any(|&term| {
            query_lower.split_whitespace().any(|word| word == term)
        });
        
        if explicit_science {
            0.8
        } else if query_lower.starts_with("how does") && query_lower.contains("work") {
            // Scientific explanation for "how does X work" queries
            0.6
        } else {
            0.0
        }
    }
    
    fn generate(&self, _query: &str, context: &ResponseContext) -> Option<String> {
        // Use knowledge from context instead of hardcoded responses
        for node in &context.relevant_nodes {
            if matches!(node.domain, KnowledgeDomain::Physics | KnowledgeDomain::Chemistry | KnowledgeDomain::Biology | KnowledgeDomain::Astronomy) {
                return Some(format!(
                    "From a scientific perspective, {}. This demonstrates the principles of {} in action.",
                    node.content.to_lowercase(),
                    match node.domain {
                        KnowledgeDomain::Physics => "physics",
                        KnowledgeDomain::Chemistry => "chemistry",
                        KnowledgeDomain::Biology => "biology",
                        KnowledgeDomain::Astronomy => "astronomy",
                        _ => "science"
                    }
                ));
            }
        }
        None
    }
}

/// Component for technical explanations
struct TechnicalComponent;

impl ResponseComponent for TechnicalComponent {
    fn name(&self) -> &'static str {
        "Technical"
    }
    
    fn can_handle(&self, query: &str, context: &ResponseContext) -> f32 {
        let query_lower = query.to_lowercase();
        let tech_terms = ["code", "program", "programming", "algorithm", "data", "computer", "software", "hardware", "debug", "function", "variable"];
        
        // Only handle if query explicitly asks about technical topics
        let explicit_tech = tech_terms.iter().any(|&term| {
            query_lower.split_whitespace().any(|word| word == term || word.starts_with(term))
        });
        
        if explicit_tech {
            0.8
        } else {
            0.0
        }
    }
    
    fn generate(&self, _query: &str, context: &ResponseContext) -> Option<String> {
        // Use knowledge from context for technical explanations
        for node in &context.relevant_nodes {
            if matches!(node.domain, KnowledgeDomain::ComputerScience | KnowledgeDomain::Engineering) {
                return Some(format!(
                    "From a technical perspective, {}. This involves {} principles and practices.",
                    node.content,
                    match node.domain {
                        KnowledgeDomain::ComputerScience => "computer science",
                        KnowledgeDomain::Engineering => "engineering",
                        _ => "technical"
                    }
                ));
            }
        }
        None
    }
}

/// Component for philosophical insights
struct PhilosophicalComponent;

impl ResponseComponent for PhilosophicalComponent {
    fn name(&self) -> &'static str {
        "Philosophical"
    }
    
    fn can_handle(&self, query: &str, context: &ResponseContext) -> f32 {
        let query_lower = query.to_lowercase();
        let phil_terms = ["meaning", "purpose", "consciousness", "existence", "reality", "truth", "ethics", "moral", "free will"];
        
        if phil_terms.iter().any(|&term| query_lower.contains(term)) {
            0.8
        } else if context.relevant_nodes.iter().any(|n| matches!(n.domain, KnowledgeDomain::Philosophy)) {
            0.6
        } else {
            0.0
        }
    }
    
    fn generate(&self, query: &str, _context: &ResponseContext) -> Option<String> {
        let query_lower = query.to_lowercase();
        
        if query_lower.contains("consciousness") {
            Some("Consciousness represents the hard problem of philosophy - how subjective experience arises from objective processes. It's the inner light of awareness that makes you 'you' rather than a philosophical zombie.".to_string())
        } else if query_lower.contains("meaning") || query_lower.contains("purpose") {
            Some("Meaning emerges from the intersection of consciousness and choice. We create purpose through our actions, relationships, and the values we embody. The search itself may be the meaning.".to_string())
        } else {
            None
        }
    }
}

/// Component for composition/makeup questions
struct CompositionComponent;

impl ResponseComponent for CompositionComponent {
    fn name(&self) -> &'static str {
        "Composition"
    }
    
    fn can_handle(&self, query: &str, _context: &ResponseContext) -> f32 {
        let query_lower = query.to_lowercase();
        if query_lower.contains("made of") || query_lower.contains("composed of") || 
           query_lower.contains("consists of") || query_lower.contains("composition") {
            0.9
        } else {
            0.0
        }
    }
    
    fn generate(&self, query: &str, context: &ResponseContext) -> Option<String> {
        let query_lower = query.to_lowercase();
        
        // Look for composition information in relevant nodes
        for node in &context.relevant_nodes {
            let topic_lower = node.topic.to_lowercase();
            let content_lower = node.content.to_lowercase();
            
            // Check if this node is about what we're asking for composition of
            if (query_lower.contains("sun") && topic_lower.contains("sun")) ||
               (query_lower.contains("jupiter") && topic_lower.contains("jupiter")) ||
               (query_lower.contains("mars") && topic_lower.contains("mars")) ||
               (query_lower.contains("moon") && topic_lower.contains("moon")) ||
               (query_lower.contains("earth") && topic_lower.contains("earth")) {
                
                // Check if content contains composition information
                if content_lower.contains("composed") || content_lower.contains("consists") || 
                   content_lower.contains("made") || content_lower.contains("hydrogen") ||
                   content_lower.contains("helium") || content_lower.contains("iron") {
                    return Some(node.content.clone());
                }
            }
        }
        
        // Fallback to hardcoded responses for common queries
        if let Some(celestial) = context.extracted_entities.get("celestial") {
            match celestial.as_str() {
                "sun" => Some("The Sun consists of approximately 73% hydrogen and 25% helium by mass, with the remaining 2% comprising heavier elements like oxygen, carbon, nitrogen, and iron. In its core, hydrogen fuses into helium at 15 million degrees Celsius.".to_string()),
                "jupiter" => Some("Jupiter is composed primarily of hydrogen (about 90%) and helium (about 10%), similar to the Sun. Deeper inside, under extreme pressure, hydrogen becomes metallic. The core may be rocky, containing heavier elements.".to_string()),
                "earth" => Some("Earth has a layered structure: a solid inner core of iron-nickel, a liquid outer core, a rocky mantle of silicate minerals, and a thin crust of lighter rocks. The atmosphere is 78% nitrogen and 21% oxygen.".to_string()),
                _ => None,
            }
        } else {
            None
        }
    }
}

/// Component for comparisons
struct ComparisonComponent;

impl ResponseComponent for ComparisonComponent {
    fn name(&self) -> &'static str {
        "Comparison"
    }
    
    fn can_handle(&self, query: &str, _context: &ResponseContext) -> f32 {
        let query_lower = query.to_lowercase();
        if query_lower.contains("difference") || query_lower.contains("similar") || 
           query_lower.contains("compare") || query_lower.contains("versus") ||
           query_lower.contains(" vs ") {
            0.8
        } else {
            0.0
        }
    }
    
    fn generate(&self, query: &str, context: &ResponseContext) -> Option<String> {
        // Extract actual topic from query or context
        let topic = if let Some(node) = context.relevant_nodes.first() {
            &node.topic
        } else {
            // Extract topic from query
            let words: Vec<&str> = query.split_whitespace().collect();
            if let Some(topic_word) = words.iter().find(|&&w| w.len() > 3 && !w.starts_with("what") && !w.starts_with("how")) {
                topic_word
            } else {
                "this topic"
            }
        };
        
        // Get actual content from knowledge base
        if let Some(node) = context.relevant_nodes.first() {
            Some(format!("{} can be understood through multiple dimensions: {}. It involves {} and has applications in {}.", 
                topic, 
                node.content.split('.').next().unwrap_or(&node.content),
                node.content.split('.').nth(1).unwrap_or("various domains"),
                node.content.split('.').nth(2).unwrap_or("many fields")
            ))
        } else {
            Some(format!("{} can be analyzed from multiple perspectives and has various characteristics and applications.", topic))
        }
    }
}

/// Component for historical context
struct HistoricalComponent;

impl ResponseComponent for HistoricalComponent {
    fn name(&self) -> &'static str {
        "Historical"
    }
    
    fn can_handle(&self, query: &str, context: &ResponseContext) -> f32 {
        let query_lower = query.to_lowercase();
        if query_lower.contains("history") || query_lower.contains("historical") || 
           query_lower.contains("origin") || query_lower.contains("discovered") ||
           query_lower.contains("invented") {
            0.8
        } else if context.relevant_nodes.iter().any(|n| matches!(n.domain, KnowledgeDomain::History)) {
            0.6
        } else {
            0.0
        }
    }
    
    fn generate(&self, query: &str, context: &ResponseContext) -> Option<String> {
        // Extract actual topic from query or context
        let topic = if let Some(node) = context.relevant_nodes.first() {
            &node.topic
        } else {
            // Extract topic from query
            let words: Vec<&str> = query.split_whitespace().collect();
            if let Some(topic_word) = words.iter().find(|&&w| w.len() > 3 && !w.starts_with("what") && !w.starts_with("how")) {
                topic_word
            } else {
                "this topic"
            }
        };
        
        // Get actual content from knowledge base
        if let Some(node) = context.relevant_nodes.first() {
            Some(format!("Throughout history, {} has been studied and understood in different ways. {}. The understanding of {} continues to evolve with new discoveries and insights.", 
                topic, 
                node.content.split('.').next().unwrap_or(&node.content),
                topic
            ))
        } else {
            Some(format!("Throughout history, {} has evolved in understanding from ancient times to the present day.", topic))
        }
    }
}

/// Component for practical applications
struct PracticalApplicationComponent;

impl ResponseComponent for PracticalApplicationComponent {
    fn name(&self) -> &'static str {
        "Practical"
    }
    
    fn can_handle(&self, query: &str, _context: &ResponseContext) -> f32 {
        let query_lower = query.to_lowercase();
        if query_lower.contains("use") || query_lower.contains("application") || 
           query_lower.contains("practical") || query_lower.contains("real world") ||
           query_lower.contains("apply") {
            0.7
        } else {
            0.0
        }
    }
    
    fn generate(&self, query: &str, context: &ResponseContext) -> Option<String> {
        // Extract actual topic from query or context
        let topic = if let Some(node) = context.relevant_nodes.first() {
            &node.topic
        } else {
            // Extract topic from query
            let words: Vec<&str> = query.split_whitespace().collect();
            if let Some(topic_word) = words.iter().find(|&&w| w.len() > 3 && !w.starts_with("what") && !w.starts_with("how")) {
                topic_word
            } else {
                "this topic"
            }
        };
        
        // Get actual content from knowledge base
        if let Some(node) = context.relevant_nodes.first() {
            Some(format!("In practical applications, {} is used in various ways. {}. Understanding {} helps in real-world problem solving and innovation.", 
                topic, 
                node.content.split('.').next().unwrap_or(&node.content),
                topic
            ))
        } else {
            Some(format!("In practical applications, {} has various uses and implementations in real-world scenarios.", topic))
        }
    }
}

/// Component for future speculation
struct FutureSpeculationComponent;

impl ResponseComponent for FutureSpeculationComponent {
    fn name(&self) -> &'static str {
        "Future"
    }
    
    fn can_handle(&self, query: &str, _context: &ResponseContext) -> f32 {
        let query_lower = query.to_lowercase();
        if query_lower.contains("future") || query_lower.contains("will be") || 
           query_lower.contains("prediction") || query_lower.contains("forecast") {
            0.7
        } else {
            0.0
        }
    }
    
    fn generate(&self, query: &str, context: &ResponseContext) -> Option<String> {
        // Extract actual topic from query or context
        let topic = if let Some(node) = context.relevant_nodes.first() {
            &node.topic
        } else {
            // Extract topic from query
            let words: Vec<&str> = query.split_whitespace().collect();
            if let Some(topic_word) = words.iter().find(|&&w| w.len() > 3 && !w.starts_with("what") && !w.starts_with("how")) {
                topic_word
            } else {
                "this topic"
            }
        };
        
        // Get actual content from knowledge base
        if let Some(node) = context.relevant_nodes.first() {
            Some(format!("Looking toward the future, {} may continue to develop and expand. {}. Future advances in {} could lead to new discoveries and applications.", 
                topic, 
                node.content.split('.').next().unwrap_or(&node.content),
                topic
            ))
        } else {
            Some(format!("Looking toward the future, {} may evolve with new technologies and deeper understanding.", topic))
        }
    }
}

/// Component for analogies and metaphors
struct AnalogyComponent;

impl ResponseComponent for AnalogyComponent {
    fn name(&self) -> &'static str {
        "Analogy"
    }
    
    fn can_handle(&self, query: &str, _context: &ResponseContext) -> f32 {
        let query_lower = query.to_lowercase();
        if query_lower.contains("like") || query_lower.contains("similar to") || 
           query_lower.contains("analogy") || query_lower.contains("metaphor") {
            0.6
        } else {
            0.3 // Low baseline - analogies can enhance many responses
        }
    }
    
    fn generate(&self, _query: &str, context: &ResponseContext) -> Option<String> {
        if context.extracted_entities.contains_key("celestial") {
            Some("Think of it like a cosmic dance - each element plays its part in the grand choreography of the universe, bound by invisible forces yet free to express its unique nature.".to_string())
        } else {
            None
        }
    }
}

/// Component for handling unknown/unclear queries
struct UnknownQueryComponent;

impl ResponseComponent for UnknownQueryComponent {
    fn name(&self) -> &'static str {
        "UnknownQuery"
    }
    
    fn can_handle(&self, query: &str, context: &ResponseContext) -> f32 {
        // This component handles queries when knowledge base has no good matches
        if context.relevant_nodes.is_empty() {
            0.9 // High priority when no matches
        } else {
            // Check if we actually have relevant nodes
            let query_tokens: Vec<String> = query.to_lowercase()
                .split_whitespace()
                .filter(|w| w.len() > 2)
                .map(|s| s.to_string())
                .collect();
                
            let has_relevant_match = context.relevant_nodes.iter().any(|node| {
                let topic_lower = node.topic.to_lowercase();
                query_tokens.iter().any(|token| topic_lower.contains(token))
            });
            
            if !has_relevant_match {
                0.8 // High priority when nodes aren't actually relevant
            } else {
                0.0 // Don't use this component if we have relevant matches
            }
        }
    }
    
    fn generate(&self, query: &str, context: &ResponseContext) -> Option<String> {
        let query_lower = query.to_lowercase();
        
        // Extract the main subject being asked about
        let main_subject = if query_lower.starts_with("what is ") {
            query_lower.strip_prefix("what is ").unwrap().trim().to_string()
        } else if query_lower.starts_with("tell me about ") {
            query_lower.strip_prefix("tell me about ").unwrap().trim().to_string()
        } else {
            // Find key terms
            query_lower.split_whitespace()
                .filter(|w| w.len() > 3 && !["what", "those", "about", "tell", "explain", "describe", "does", "have"].contains(w))
                .collect::<Vec<_>>()
                .join(" ")
        };
        
        if main_subject.is_empty() {
            Some("I'd be happy to help! Could you tell me more about what you'd like to know?".to_string())
        } else {
            // Simple response for unknown topics
            Some(format!(
                "I don't have specific information about '{}' in my knowledge base. I can help with topics like quantum mechanics, consciousness, astronomy (sun, mars, moon), AI concepts (TinyLlama, Think AI), and philosophy (stoicism). What would you like to know about?",
                main_subject
            ))
        }
    }
}

/// Component for self-referential learning queries
struct LearningComponent;

impl ResponseComponent for LearningComponent {
    fn name(&self) -> &'static str {
        "Learning"
    }
    
    fn can_handle(&self, query: &str, _context: &ResponseContext) -> f32 {
        let query_lower = query.to_lowercase();
        let learning_terms = ["learn", "teach", "know", "understand", "remember", "forget", "knowledge"];
        
        if learning_terms.iter().any(|&term| query_lower.contains(term)) {
            0.6
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
        } else if query_lower.contains("can you remember") || query_lower.contains("do you remember") {
            Some("Yes, I maintain conversation memory within our current session. I can reference previous topics we've discussed and use that context to provide more relevant responses. However, my memory is limited to our current conversation session.".to_string())
        } else {
            None
        }
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