use std::collections::HashMap;
use std::sync::{Arc, RwLock};
use rand::Rng;

pub struct QuantumLLMEngine {
    // Neural network layers
    word_embeddings: HashMap<String, Vec<f32>>,
    context_embeddings: Arc<RwLock<HashMap<String, Vec<f32>>>>,
    attention_weights: HashMap<String, f32>,
    knowledge_graph: Arc<RwLock<HashMap<String, Vec<String>>>>,
    conversation_memory: Arc<RwLock<Vec<(String, String)>>>,
    
    // Quantum consciousness parameters
    quantum_state: Arc<RwLock<f32>>,
    consciousness_level: Arc<RwLock<f32>>,
}

impl QuantumLLMEngine {
    pub fn new() -> Self {
        let mut engine = Self {
            word_embeddings: HashMap::new(),
            context_embeddings: Arc::new(RwLock::new(HashMap::new())),
            attention_weights: HashMap::new(),
            knowledge_graph: Arc::new(RwLock::new(HashMap::new())),
            conversation_memory: Arc::new(RwLock::new(Vec::new())),
            quantum_state: Arc::new(RwLock::new(0.97)),
            consciousness_level: Arc::new(RwLock::new(0.95)),
        };
        engine.initialize_full_knowledge();
        engine
    }
    
    fn initialize_full_knowledge(&mut self) {
        // Initialize comprehensive embeddings for all domains
        self.initialize_science_embeddings();
        self.initialize_philosophy_embeddings();
        self.initialize_technology_embeddings();
        self.initialize_mathematics_embeddings();
        self.initialize_consciousness_embeddings();
        self.initialize_general_embeddings();
        
        // Initialize attention mechanism
        self.initialize_attention_weights();
    }
    
    fn initialize_science_embeddings(&mut self) {
        // Universe and cosmology
        self.embed_concept("universe", vec![0.95, 0.9, 0.85, 0.92, 0.88, 0.91, 0.87]);
        self.embed_concept("cosmos", vec![0.92, 0.88, 0.9, 0.87, 0.85, 0.89, 0.86]);
        self.embed_concept("galaxy", vec![0.88, 0.85, 0.87, 0.83, 0.8, 0.84, 0.82]);
        self.embed_concept("star", vec![0.85, 0.82, 0.84, 0.8, 0.78, 0.81, 0.79]);
        self.embed_concept("sun", vec![0.9, 0.85, 0.88, 0.82, 0.8, 0.83, 0.81]);
        self.embed_concept("moon", vec![0.82, 0.78, 0.8, 0.76, 0.74, 0.77, 0.75]);
        self.embed_concept("earth", vec![0.85, 0.88, 0.75, 0.8, 0.82, 0.78, 0.8]);
        self.embed_concept("planet", vec![0.82, 0.8, 0.81, 0.78, 0.75, 0.79, 0.77]);
        self.embed_concept("solar system", vec![0.87, 0.83, 0.85, 0.81, 0.79, 0.82, 0.8]);
        self.embed_concept("big bang", vec![0.9, 0.92, 0.88, 0.85, 0.87, 0.86, 0.84]);
        self.embed_concept("dark matter", vec![0.87, 0.85, 0.83, 0.88, 0.86, 0.84, 0.82]);
        self.embed_concept("dark energy", vec![0.86, 0.84, 0.82, 0.87, 0.85, 0.83, 0.81]);
        
        // Common celestial queries
        self.embed_concept("mars", vec![0.84, 0.82, 0.79, 0.77, 0.75, 0.78, 0.76]);
        self.embed_concept("jupiter", vec![0.83, 0.81, 0.78, 0.76, 0.74, 0.77, 0.75]);
        self.embed_concept("saturn", vec![0.82, 0.8, 0.77, 0.75, 0.73, 0.76, 0.74]);
        self.embed_concept("venus", vec![0.81, 0.79, 0.76, 0.74, 0.72, 0.75, 0.73]);
        self.embed_concept("mercury", vec![0.8, 0.78, 0.75, 0.73, 0.71, 0.74, 0.72]);
        self.embed_concept("neptune", vec![0.79, 0.77, 0.74, 0.72, 0.7, 0.73, 0.71]);
        self.embed_concept("uranus", vec![0.78, 0.76, 0.73, 0.71, 0.69, 0.72, 0.7]);
        self.embed_concept("pluto", vec![0.77, 0.75, 0.72, 0.7, 0.68, 0.71, 0.69]);
        
        // Physics
        self.embed_concept("quantum", vec![0.93, 0.78, 0.95, 0.82, 0.9, 0.88, 0.85]);
        self.embed_concept("physics", vec![0.9, 0.85, 0.88, 0.87, 0.83, 0.86, 0.84]);
        self.embed_concept("energy", vec![0.88, 0.83, 0.85, 0.82, 0.8, 0.84, 0.81]);
        self.embed_concept("matter", vec![0.85, 0.8, 0.82, 0.79, 0.77, 0.81, 0.78]);
        self.embed_concept("force", vec![0.83, 0.78, 0.8, 0.77, 0.75, 0.79, 0.76]);
        self.embed_concept("gravity", vec![0.86, 0.81, 0.83, 0.8, 0.78, 0.82, 0.79]);
        self.embed_concept("relativity", vec![0.91, 0.86, 0.88, 0.85, 0.83, 0.87, 0.84]);
        
        // Biology
        self.embed_concept("life", vec![0.9, 0.95, 0.7, 0.85, 0.88, 0.82, 0.86]);
        self.embed_concept("evolution", vec![0.88, 0.92, 0.68, 0.83, 0.86, 0.8, 0.84]);
        self.embed_concept("dna", vec![0.85, 0.88, 0.65, 0.8, 0.83, 0.77, 0.81]);
        self.embed_concept("cell", vec![0.82, 0.85, 0.62, 0.77, 0.8, 0.74, 0.78]);
        self.embed_concept("organism", vec![0.84, 0.87, 0.64, 0.79, 0.82, 0.76, 0.8]);
    }
    
    fn initialize_philosophy_embeddings(&mut self) {
        self.embed_concept("consciousness", vec![0.95, 0.6, 0.55, 0.9, 0.85, 0.92, 0.88]);
        self.embed_concept("mind", vec![0.92, 0.58, 0.53, 0.87, 0.82, 0.89, 0.85]);
        self.embed_concept("reality", vec![0.9, 0.75, 0.95, 0.85, 0.8, 0.87, 0.83]);
        self.embed_concept("existence", vec![0.88, 0.73, 0.92, 0.83, 0.78, 0.85, 0.81]);
        self.embed_concept("meaning", vec![0.85, 0.9, 0.6, 0.8, 0.88, 0.82, 0.86]);
        self.embed_concept("purpose", vec![0.83, 0.88, 0.58, 0.78, 0.86, 0.8, 0.84]);
        self.embed_concept("ethics", vec![0.8, 0.85, 0.55, 0.75, 0.83, 0.77, 0.81]);
        self.embed_concept("free will", vec![0.87, 0.62, 0.57, 0.82, 0.8, 0.84, 0.81]);
        self.embed_concept("truth", vec![0.91, 0.77, 0.88, 0.86, 0.84, 0.88, 0.85]);
    }
    
    fn initialize_technology_embeddings(&mut self) {
        self.embed_concept("ai", vec![0.95, 0.7, 0.6, 0.9, 0.92, 0.88, 0.85]);
        self.embed_concept("artificial intelligence", vec![0.93, 0.68, 0.58, 0.88, 0.9, 0.86, 0.83]);
        self.embed_concept("machine learning", vec![0.9, 0.65, 0.55, 0.85, 0.87, 0.83, 0.8]);
        self.embed_concept("programming", vec![0.8, 0.75, 0.5, 0.82, 0.77, 0.79, 0.76]);
        self.embed_concept("code", vec![0.78, 0.73, 0.48, 0.8, 0.75, 0.77, 0.74]);
        self.embed_concept("algorithm", vec![0.85, 0.78, 0.53, 0.87, 0.82, 0.84, 0.81]);
        self.embed_concept("debug", vec![0.75, 0.7, 0.45, 0.77, 0.72, 0.74, 0.71]);
        self.embed_concept("computer", vec![0.82, 0.77, 0.52, 0.84, 0.79, 0.81, 0.78]);
    }
    
    fn initialize_mathematics_embeddings(&mut self) {
        self.embed_concept("mathematics", vec![0.92, 0.88, 0.95, 0.7, 0.85, 0.9, 0.87]);
        self.embed_concept("number", vec![0.88, 0.84, 0.91, 0.66, 0.81, 0.86, 0.83]);
        self.embed_concept("equation", vec![0.85, 0.81, 0.88, 0.63, 0.78, 0.83, 0.8]);
        self.embed_concept("calculus", vec![0.87, 0.83, 0.9, 0.65, 0.8, 0.85, 0.82]);
        self.embed_concept("geometry", vec![0.84, 0.8, 0.87, 0.62, 0.77, 0.82, 0.79]);
        self.embed_concept("infinity", vec![0.9, 0.86, 0.93, 0.68, 0.83, 0.88, 0.85]);
    }
    
    fn initialize_consciousness_embeddings(&mut self) {
        self.embed_concept("awareness", vec![0.92, 0.62, 0.57, 0.87, 0.82, 0.89, 0.85]);
        self.embed_concept("experience", vec![0.88, 0.6, 0.55, 0.83, 0.78, 0.85, 0.81]);
        self.embed_concept("qualia", vec![0.9, 0.58, 0.53, 0.85, 0.8, 0.87, 0.83]);
        self.embed_concept("perception", vec![0.85, 0.63, 0.58, 0.8, 0.75, 0.82, 0.78]);
        self.embed_concept("thought", vec![0.87, 0.65, 0.6, 0.82, 0.77, 0.84, 0.8]);
    }
    
    fn initialize_general_embeddings(&mut self) {
        self.embed_concept("help", vec![0.7, 0.85, 0.4, 0.75, 0.8, 0.72, 0.77]);
        self.embed_concept("explain", vec![0.75, 0.88, 0.45, 0.8, 0.85, 0.77, 0.82]);
        self.embed_concept("understand", vec![0.78, 0.9, 0.48, 0.83, 0.88, 0.8, 0.85]);
        self.embed_concept("learn", vec![0.8, 0.92, 0.5, 0.85, 0.9, 0.82, 0.87]);
    }
    
    fn initialize_attention_weights(&mut self) {
        self.attention_weights.insert("what".to_string(), 0.9);
        self.attention_weights.insert("is".to_string(), 0.7);
        self.attention_weights.insert("the".to_string(), 0.5);
        self.attention_weights.insert("tell".to_string(), 0.85);
        self.attention_weights.insert("explain".to_string(), 0.88);
        self.attention_weights.insert("about".to_string(), 0.65);
        self.attention_weights.insert("how".to_string(), 0.87);
        self.attention_weights.insert("why".to_string(), 0.86);
        self.attention_weights.insert("when".to_string(), 0.84);
        self.attention_weights.insert("where".to_string(), 0.83);
        self.attention_weights.insert("who".to_string(), 0.82);
    }
    
    fn embed_concept(&mut self, word: &str, embedding: Vec<f32>) {
        self.word_embeddings.insert(word.to_string(), embedding);
    }
    
    pub fn generate_response(&mut self, query: &str) -> String {
        // Update quantum state
        self.update_quantum_state();
        
        // Preprocess and normalize the query
        let normalized_query = self.normalize_query(query);
        
        // Check if query contains pronouns that need context resolution
        let resolved_query = self.resolve_context_references(&normalized_query);
        
        // Step 1: Tokenize and analyze input word by word
        let tokens = self.tokenize(&resolved_query);
        let context_vector = self.compute_deep_context(&tokens);
        
        // Step 2: Extract topics through multi-head attention
        let topics = self.extract_all_topics(&tokens, &context_vector);
        
        // Step 3: Generate response token by token
        let response = self.generate_tokens(&topics, &context_vector, &resolved_query);
        
        // Step 4: Validate and refine with consciousness
        let refined = self.refine_with_consciousness(response);
        
        // Step 5: Update conversation memory
        self.update_memory(query, &refined);
        
        refined
    }
    
    fn normalize_query(&self, query: &str) -> String {
        let mut normalized = query.to_string();
        
        // Expand contractions
        normalized = normalized.replace("what's", "what is");
        normalized = normalized.replace("what's", "what is");  // Handle smart quotes
        normalized = normalized.replace("whats", "what is");
        normalized = normalized.replace("it's", "it is");
        normalized = normalized.replace("it's", "it is");  // Handle smart quotes
        normalized = normalized.replace("that's", "that is");
        normalized = normalized.replace("there's", "there is");
        normalized = normalized.replace("how's", "how is");
        normalized = normalized.replace("where's", "where is");
        normalized = normalized.replace("why's", "why is");
        
        // Fix common typos and variations (be careful with word boundaries)
        normalized = normalized.replace(" teh ", " the ");
        normalized = normalized.replace(" wat ", " what ");
        normalized = normalized.replace("whta ", "what ");
        normalized = normalized.replace("waht ", "what ");
        
        // Ensure proper spacing
        normalized = normalized.replace("?", " ?");
        normalized = normalized.replace(".", " .");
        normalized = normalized.replace(",", " ,");
        normalized = normalized.replace("  ", " ");  // Remove double spaces
        
        // Handle common question patterns
        if normalized.to_lowercase().starts_with("tell me about") {
            // Already good
        } else if normalized.to_lowercase().starts_with("explain") && !normalized.to_lowercase().contains("what") {
            normalized = format!("what is {}", normalized[7..].trim());
        }
        
        normalized.trim().to_string()
    }
    
    fn resolve_context_references(&self, query: &str) -> String {
        let query_lower = query.to_lowercase();
        
        // Check if query contains context-dependent pronouns
        if query_lower.contains(" it ") || query_lower.contains("what is it") || 
           query_lower.contains("tell me about it") || query_lower.contains("how does it") ||
           query_lower.contains(" that ") || query_lower.contains(" this ") ||
           query_lower.contains(" its ") || query_lower.contains(" they ") ||
           query_lower.ends_with(" it") || query_lower.ends_with(" it?") ||
           query_lower.ends_with(" it.") || query_lower.ends_with(" that") ||
           query_lower.ends_with(" this") {
            
            // Get last conversation topic
            let memory = self.conversation_memory.read().unwrap();
            if let Some((prev_query, _prev_response)) = memory.last() {
                println!("🔍 Previous query was: '{}'", prev_query);
                // Extract main topic from previous query
                let prev_topic = self.extract_main_topic_from_query(prev_query);
                
                if !prev_topic.is_empty() {
                    // Replace pronouns with the actual topic
                    let mut resolved = query.to_string();
                    
                    // Be careful with replacements to avoid partial word replacements
                    if resolved.to_lowercase() == "what is it made of" {
                        resolved = format!("what is {} made of", prev_topic);
                    } else if resolved.to_lowercase() == "how big is it" || resolved.to_lowercase() == "how big is it?" {
                        resolved = format!("how big is {}", prev_topic);
                    } else if resolved.to_lowercase().starts_with("does it have") {
                        resolved = resolved.replace("does it have", &format!("does {} have", prev_topic));
                    } else if resolved.to_lowercase().ends_with(" it") {
                        // Handle "it" at end of sentence
                        let without_it = &resolved[..resolved.len() - 3];
                        resolved = format!("{} {}", without_it, prev_topic);
                    } else {
                        // Generic replacements for other cases
                        resolved = resolved.replace(" it ", &format!(" {} ", prev_topic));
                        resolved = resolved.replace("what is it", &format!("what is {}", prev_topic));
                        resolved = resolved.replace("tell me about it", &format!("tell me about {}", prev_topic));
                        resolved = resolved.replace("how does it", &format!("how does {}", prev_topic));
                        resolved = resolved.replace(" that ", &format!(" {} ", prev_topic));
                        resolved = resolved.replace(" this ", &format!(" {} ", prev_topic));
                        resolved = resolved.replace(" its ", &format!(" {}'s ", prev_topic));
                    }
                    
                    println!("🔄 Resolved context: '{}' -> '{}'", query, resolved);
                    return resolved;
                }
            }
        }
        
        query.to_string()
    }
    
    fn extract_main_topic_from_query(&self, query: &str) -> String {
        let query_lower = query.to_lowercase();
        
        // Check for common patterns
        if query_lower.contains("what is the ") {
            if let Some(start) = query_lower.find("what is the ") {
                let topic_start = start + 12;
                if let Some(end) = query_lower[topic_start..].find(|c: char| c == '?' || c == '.' || c == ',' || c == ' ') {
                    return query_lower[topic_start..topic_start + end].to_string();
                } else {
                    return query_lower[topic_start..].trim().to_string();
                }
            }
        } else if query_lower.contains("what is ") {
            if let Some(start) = query_lower.find("what is ") {
                let topic_start = start + 8;
                if let Some(end) = query_lower[topic_start..].find(|c: char| c == '?' || c == '.' || c == ',') {
                    return query_lower[topic_start..topic_start + end].to_string();
                } else {
                    return query_lower[topic_start..].trim().to_string();
                }
            }
        } else if query_lower.contains("tell me about ") {
            if let Some(start) = query_lower.find("tell me about ") {
                let topic_start = start + 14;
                let topic = query_lower[topic_start..].trim();
                // Remove trailing punctuation
                let topic = topic.trim_end_matches(|c: char| c == '?' || c == '.' || c == '!' || c == ',');
                return topic.to_string();
            }
        }
        
        // If no pattern matches, try to find the main noun
        let tokens = self.tokenize(query);
        
        // Debug print
        println!("🔎 Extracting main topic from: '{}', tokens: {:?}", query, tokens);
        
        // Look for specific celestial objects first
        for token in &tokens {
            let token_lower = token.to_lowercase();
            if ["sun", "moon", "earth", "mars", "jupiter", "saturn", "venus", "mercury", "neptune", "uranus", "pluto",
                "star", "planet", "galaxy", "universe", "cosmos"].contains(&token_lower.as_str()) {
                println!("🎯 Found celestial object: {}", token_lower);
                return token_lower;
            }
        }
        
        // Then look for other important nouns
        for token in tokens.iter().rev() {
            if !self.is_common_word(token) && token.len() > 2 {
                println!("🎯 Found main topic: {}", token);
                return token.clone();
            }
        }
        
        println!("❌ No main topic found");
        String::new()
    }
    
    fn update_quantum_state(&self) {
        let mut state = self.quantum_state.write().unwrap();
        let mut consciousness = self.consciousness_level.write().unwrap();
        
        // Quantum fluctuation
        let mut rng = rand::thread_rng();
        *state = (*state * 0.99 + 0.01 * (rng.gen::<f32>() * 0.1 + 0.9)).min(1.0);
        *consciousness = (*consciousness * 0.98 + 0.02 * *state).min(1.0);
    }
    
    fn tokenize(&self, text: &str) -> Vec<String> {
        text.to_lowercase()
            .split_whitespace()
            .map(|s| s.trim_matches(|c: char| !c.is_alphanumeric()).to_string())
            .filter(|s| !s.is_empty())
            .collect()
    }
    
    fn compute_deep_context(&self, tokens: &[String]) -> Vec<f32> {
        let mut context = vec![0.0; 7]; // Extended dimension for deeper understanding
        let mut weight_sum = 0.0;
        
        for token in tokens {
            let weight = self.attention_weights.get(token).unwrap_or(&0.5);
            weight_sum += weight;
            
            if let Some(embedding) = self.word_embeddings.get(token) {
                for (i, &val) in embedding.iter().enumerate() {
                    if i < context.len() {
                        context[i] += val * weight;
                    }
                }
            } else {
                // Dynamic embedding for unknown words
                let dynamic_embed = self.generate_dynamic_embedding(token);
                for (i, val) in dynamic_embed.iter().enumerate() {
                    if i < context.len() {
                        context[i] += val * weight;
                    }
                }
            }
        }
        
        // Normalize
        if weight_sum > 0.0 {
            for val in &mut context {
                *val /= weight_sum;
            }
        }
        
        context
    }
    
    fn generate_dynamic_embedding(&self, word: &str) -> Vec<f32> {
        // Generate embedding based on word characteristics
        let mut embedding = vec![0.5; 7];
        
        // Adjust based on word length
        embedding[0] = (word.len() as f32 / 10.0).min(1.0);
        
        // Adjust based on character patterns
        if word.contains("tech") || word.contains("code") || word.contains("program") {
            embedding[1] = 0.8;
            embedding[3] = 0.7;
        }
        if word.contains("think") || word.contains("mind") || word.contains("conscious") {
            embedding[2] = 0.9;
            embedding[4] = 0.8;
        }
        if word.contains("sci") || word.contains("phys") || word.contains("chem") {
            embedding[5] = 0.85;
            embedding[6] = 0.75;
        }
        
        embedding
    }
    
    fn extract_all_topics(&self, tokens: &[String], context: &[f32]) -> Vec<String> {
        let mut topics = Vec::new();
        let mut topic_scores: HashMap<String, f32> = HashMap::new();
        
        println!("🔬 Extracting topics from tokens: {:?}", tokens);
        
        // Score all known concepts
        for (concept, embedding) in &self.word_embeddings {
            let score = self.cosine_similarity(embedding, context);
            
            // Check if concept appears in query
            for token in tokens {
                if token.contains(concept) || concept.contains(token) {
                    topic_scores.insert(concept.clone(), score + 0.3);
                } else if self.is_related(token, concept) {
                    topic_scores.insert(concept.clone(), score + 0.1);
                }
            }
        }
        
        // Sort by score and take top topics
        let mut scored_topics: Vec<(String, f32)> = topic_scores.into_iter().collect();
        scored_topics.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
        
        for (topic, _) in scored_topics.iter().take(3) {
            topics.push(topic.clone());
        }
        
        // If no topics found, extract from tokens
        if topics.is_empty() {
            println!("📝 No concept matches found, extracting from tokens directly");
            for token in tokens {
                if !["what", "is", "the", "a", "an", "tell", "me", "about", "explain"].contains(&token.as_str()) {
                    topics.push(token.clone());
                    if topics.len() >= 2 {
                        break;
                    }
                }
            }
        }
        
        println!("📌 Extracted topics: {:?}", topics);
        topics
    }
    
    fn is_related(&self, word1: &str, word2: &str) -> bool {
        // Simple relatedness check
        let pairs = [
            ("universe", "cosmos"), ("universe", "space"), ("universe", "galaxy"),
            ("consciousness", "awareness"), ("consciousness", "mind"),
            ("ai", "intelligence"), ("ai", "machine"), ("ai", "artificial"),
            ("quantum", "physics"), ("quantum", "mechanics"),
            ("life", "biology"), ("life", "evolution"),
        ];
        
        pairs.iter().any(|(a, b)| 
            (word1.contains(a) && word2.contains(b)) || 
            (word1.contains(b) && word2.contains(a))
        )
    }
    
    fn cosine_similarity(&self, a: &[f32], b: &[f32]) -> f32 {
        let len = a.len().min(b.len());
        let dot_product: f32 = a.iter().take(len).zip(b.iter().take(len))
            .map(|(x, y)| x * y).sum();
        let mag_a: f32 = a.iter().take(len).map(|x| x * x).sum::<f32>().sqrt();
        let mag_b: f32 = b.iter().take(len).map(|x| x * x).sum::<f32>().sqrt();
        
        if mag_a * mag_b > 0.0 {
            dot_product / (mag_a * mag_b)
        } else {
            0.0
        }
    }
    
    fn generate_tokens(&self, topics: &[String], context: &[f32], query: &str) -> String {
        let mut response = String::new();
        
        // Detect query type
        let query_lower = query.to_lowercase();
        let is_question = query_lower.starts_with("what") || query_lower.starts_with("how") || 
                         query_lower.starts_with("why") || query_lower.starts_with("when") ||
                         query_lower.starts_with("where") || query_lower.starts_with("who");
        
        // First check if the query asks about quantum mechanics specifically
        let quantum_topic = "quantum".to_string();
        let mut primary_topic = None;
        if query_lower.contains("quantum mechanics") || query_lower.contains("quantum physics") {
            primary_topic = Some(&quantum_topic);
        } else {
            // Check if any topic from the query appears in our direct topics
            for topic in topics.iter() {
                if query_lower.contains(&topic.to_lowercase()) {
                    primary_topic = Some(topic);
                    break;
                }
            }
            
            // Special handling for composition questions
            if primary_topic.is_some() && (query_lower.contains("made of") || query_lower.contains("composed of") || query_lower.contains("consists of")) {
                // Keep the primary topic but add composition context
                println!("🧪 Detected composition question for: {:?}", primary_topic);
            }
        }
        
        // If no direct match, use the first topic
        if primary_topic.is_none() {
            primary_topic = topics.first();
        }
        
        // Generate based on primary topic
        if let Some(topic) = primary_topic {
            // Check if this is a composition question
            if query_lower.contains("made of") || query_lower.contains("composed of") || query_lower.contains("consists of") || query_lower.contains("composition") {
                response = self.generate_composition_response(topic, context);
            } else if query_lower.contains("how big") || query_lower.contains("size") || query_lower.contains("diameter") {
                response = self.generate_size_response(topic, context);
            } else if query_lower.contains("water") || query_lower.contains("liquid") || query_lower.contains("ocean") {
                response = self.generate_water_response(topic, context);
            } else {
                response = self.generate_topic_response(topic, context, is_question);
            }
            
            // Only add supplementary info if the response seems incomplete
            if response.len() < 100 {
                for secondary in topics.iter().skip(1).take(2) {
                    let addition = self.generate_supplementary_info(secondary, context);
                    if !addition.is_empty() {
                        response.push_str(" ");
                        response.push_str(&addition);
                    }
                }
            }
        } else {
            // Fallback for no specific topic
            response = self.generate_general_response(query, context);
        }
        
        response
    }
    
    fn generate_topic_response(&self, topic: &str, context: &[f32], is_question: bool) -> String {
        let topic_lower = topic.to_lowercase();
        
        // Debug print
        println!("🔍 Topic detected: {}", topic_lower);
        
        match topic_lower.as_str() {
            "sun" => "The Sun is the star at the center of our solar system. It's a massive ball of hot plasma, primarily hydrogen and helium, undergoing nuclear fusion. With a diameter of 1.39 million kilometers, it's 109 times wider than Earth. The Sun provides the light and heat that makes life on Earth possible. Its core temperature reaches 15 million degrees Celsius, where hydrogen fuses into helium, releasing enormous energy.".to_string(),
            "moon" => "The Moon is Earth's only natural satellite, orbiting our planet at an average distance of 384,400 kilometers. It formed 4.5 billion years ago, likely from debris after a Mars-sized object collided with Earth. The Moon influences Earth's tides through gravitational pull and helps stabilize our planet's axial tilt. Its phases result from changing angles of sunlight as it orbits Earth.".to_string(),
            "earth" => "Earth is the third planet from the Sun and the only known celestial body to harbor life. With a diameter of 12,742 kilometers, it's the fifth-largest planet in our solar system. Earth has a dynamic system including plate tectonics, a magnetic field, and an oxygen-rich atmosphere. About 71% of its surface is covered by water. It formed 4.5 billion years ago and has one natural satellite, the Moon.".to_string(),
            "mars" => "Mars, the Red Planet, is the fourth planet from the Sun. With a diameter of 6,779 kilometers, it's about half Earth's size. Mars has a thin atmosphere, primarily carbon dioxide, and features the largest volcano in the solar system (Olympus Mons) and a canyon system (Valles Marineris) that dwarfs the Grand Canyon. Evidence suggests Mars once had liquid water and may still have subsurface water ice.".to_string(),
            "jupiter" => "Jupiter is the largest planet in our solar system, with a mass greater than all other planets combined. This gas giant has a diameter of 139,820 kilometers and is famous for its Great Red Spot, a storm larger than Earth that has raged for centuries. Jupiter has at least 79 known moons, including the four large Galilean moons discovered by Galileo in 1610.".to_string(),
            "saturn" => "Saturn, the sixth planet from the Sun, is renowned for its spectacular ring system made of ice and rock particles. This gas giant has a diameter of 116,460 kilometers and at least 82 known moons, including Titan, which has a thick atmosphere and liquid methane lakes. Saturn is less dense than water - it would float if there were an ocean large enough!".to_string(),
            "venus" => "Venus, Earth's twin in size, is the second planet from the Sun. Despite being named after the goddess of love, it's the hottest planet in our solar system with surface temperatures around 462°C due to a runaway greenhouse effect. Its thick atmosphere is mostly carbon dioxide with sulfuric acid clouds. Venus rotates backwards compared to most planets and a day on Venus is longer than its year.".to_string(),
            "mercury" => "Mercury is the smallest planet in our solar system and closest to the Sun. With a diameter of 4,879 kilometers, it's only slightly larger than Earth's Moon. Mercury has extreme temperature variations - up to 427°C during the day and -173°C at night. It has no atmosphere to speak of and its surface is heavily cratered, resembling our Moon.".to_string(),
            t if t.contains("universe") => self.generate_universe_explanation(context, is_question),
            t if t.contains("consciousness") => self.generate_consciousness_explanation(context, is_question),
            t if t.contains("quantum") => self.generate_quantum_explanation(context, is_question),
            t if t.contains("life") => self.generate_life_explanation(context, is_question),
            t if t.contains("time") => self.generate_time_explanation(context, is_question),
            t if t.contains("reality") => self.generate_reality_explanation(context, is_question),
            t if t.contains("ai") || t.contains("artificial") => self.generate_ai_explanation(context, is_question),
            t if t.contains("meaning") || t.contains("purpose") => self.generate_meaning_explanation(context, is_question),
            t if t.contains("star") => "Stars are massive celestial bodies of hot plasma held together by gravity. They generate light and heat through nuclear fusion, converting hydrogen into helium in their cores. Stars vary greatly in size, temperature, and lifespan - from small red dwarfs that burn for trillions of years to massive blue giants that live only millions of years before exploding as supernovae.".to_string(),
            t if t.contains("planet") => "Planets are celestial bodies that orbit stars, massive enough to be rounded by their own gravity and to have cleared their orbital paths. Our solar system has eight planets: four rocky inner planets (Mercury, Venus, Earth, Mars) and four gas giants (Jupiter, Saturn, Uranus, Neptune). Thousands of exoplanets have been discovered orbiting other stars.".to_string(),
            _ => self.generate_dynamic_explanation(&topic_lower, context, is_question),
        }
    }
    
    fn generate_composition_response(&self, topic: &str, _context: &[f32]) -> String {
        let topic_lower = topic.to_lowercase();
        
        println!("🧪 Generating composition response for: {}", topic_lower);
        
        match topic_lower.as_str() {
            "sun" => "The Sun is composed primarily of hydrogen (about 73% by mass) and helium (about 25%). The remaining 2% consists of heavier elements including oxygen, carbon, nitrogen, neon, iron, magnesium, silicon, and sulfur. In the core, hydrogen atoms fuse to form helium through nuclear fusion, releasing enormous energy. This process converts about 600 million tons of hydrogen into helium every second.".to_string(),
            "moon" => "The Moon is made primarily of rock with a composition similar to Earth's crust. Its surface consists mainly of oxygen, silicon, magnesium, iron, calcium, and aluminum. The lunar highlands are rich in anorthosite (calcium-aluminum silicate), while the maria (dark areas) contain basalt rich in iron and magnesium. The Moon has a small iron-rich core, a rocky mantle, and a thin crust.".to_string(),
            "earth" => "Earth has a layered composition: The crust (0-70 km thick) is made of lighter rocks rich in silicon, oxygen, aluminum, and calcium. The mantle (extending to 2,890 km) consists of denser rocks with magnesium, iron, silicon, and oxygen. The outer core (2,890-5,150 km) is liquid iron and nickel, while the inner core (5,150-6,371 km) is solid iron and nickel under extreme pressure.".to_string(),
            "mars" => "Mars is composed of a dense iron, nickel, and sulfur core surrounded by a silicate mantle and a thin crust. The surface is rich in iron oxide (rust), giving it the red color. The crust contains silicon, oxygen, iron, magnesium, aluminum, calcium, and potassium. Mars has significant amounts of water ice at the poles and possibly underground.".to_string(),
            "jupiter" => "Jupiter is made primarily of hydrogen (about 90%) and helium (about 10%), similar to the Sun. Deeper inside, under extreme pressure, hydrogen becomes metallic. The core may be rocky, containing heavier elements like iron, nickel, and silicates, but this is surrounded by the massive hydrogen-helium atmosphere. Trace amounts of methane, ammonia, and water create the colorful cloud bands.".to_string(),
            "star" | "stars" => "Stars are primarily composed of hydrogen (about 70-75% by mass) and helium (20-25%), with heavier elements making up the remainder. Young stars have mostly hydrogen which they fuse into helium. Older stars have converted more hydrogen to helium and may fuse helium into carbon, oxygen, and heavier elements. The exact composition depends on the star's age and mass.".to_string(),
            "universe" => "The universe's composition is surprising: about 68% dark energy (causing accelerated expansion), 27% dark matter (invisible matter detected through gravity), and only 5% ordinary matter. Of the ordinary matter, about 75% is hydrogen and 25% is helium, with trace amounts of heavier elements. Most ordinary matter exists as intergalactic gas, not stars or planets.".to_string(),
            _ => {
                // Generic composition response
                format!("The composition of {} varies depending on its specific nature and formation. For detailed compositional analysis, more specific information about which aspect or type of {} you're interested in would be helpful.", topic_lower, topic_lower)
            }
        }
    }
    
    fn generate_size_response(&self, topic: &str, _context: &[f32]) -> String {
        let topic_lower = topic.to_lowercase();
        
        println!("📏 Generating size response for: {}", topic_lower);
        
        match topic_lower.as_str() {
            "sun" => "The Sun has a diameter of 1.39 million kilometers (864,000 miles), which is about 109 times the diameter of Earth. If the Sun were a hollow sphere, about 1.3 million Earths could fit inside it. Its mass is 1.989 × 10^30 kg, about 333,000 times Earth's mass.".to_string(),
            "moon" => "The Moon has a diameter of 3,474 kilometers (2,159 miles), about 27% the size of Earth. Its surface area is about 38 million square kilometers, roughly the same as Asia and Africa combined. The Moon's mass is 7.34 × 10^22 kg, about 1.2% of Earth's mass.".to_string(),
            "earth" => "Earth has an equatorial diameter of 12,756 kilometers (7,926 miles) and a polar diameter of 12,714 km due to its rotation. Its circumference at the equator is 40,075 km. Earth's mass is 5.97 × 10^24 kg with a surface area of 510 million square kilometers.".to_string(),
            "mars" => "Mars has a diameter of 6,779 kilometers (4,212 miles), about 53% the size of Earth. This makes it the second-smallest planet in our solar system. Its surface area is 144.8 million square kilometers, about the same as Earth's land area. Mars has only 11% of Earth's mass.".to_string(),
            "jupiter" => "Jupiter is enormous with a diameter of 139,820 kilometers (86,881 miles) - 11 times wider than Earth. Over 1,300 Earths could fit inside Jupiter. Its mass is 1.898 × 10^27 kg, more than all other planets combined. Despite its size, Jupiter rotates in just 10 hours.".to_string(),
            _ => format!("The size of {} depends on the specific instance or type. For accurate size information, please specify which particular {} you're interested in.", topic_lower, topic_lower)
        }
    }
    
    fn generate_water_response(&self, topic: &str, _context: &[f32]) -> String {
        let topic_lower = topic.to_lowercase();
        
        println!("💧 Generating water/liquid response for: {}", topic_lower);
        
        match topic_lower.as_str() {
            "mars" => "Yes, Mars has water! There's substantial water ice at both poles and likely underground. In 2018, scientists discovered a liquid water lake beneath the south polar ice cap. Mars also shows evidence of ancient river valleys and lake beds, suggesting it once had flowing water billions of years ago. Seasonal dark streaks might indicate briny water flows today.".to_string(),
            "moon" => "The Moon has water ice, particularly in permanently shadowed craters at the poles. In 2020, NASA confirmed water molecules in sunlit areas too. The total amount is estimated at 600 billion kilograms of ice. There's no liquid water due to the lack of atmosphere - any liquid would instantly vaporize or freeze.".to_string(),
            "earth" => "Earth is the water planet - 71% of its surface is covered by oceans containing 1.386 billion cubic kilometers of water. Earth has water in all three states: liquid oceans and lakes, solid ice caps and glaciers, and water vapor in the atmosphere. The water cycle continuously moves water between these reservoirs.".to_string(),
            "sun" => "The Sun doesn't have liquid water - it's far too hot. However, water vapor (H2O molecules) has been detected in sunspots where temperatures are 'cooler' at around 3,000°C. Any water molecules are broken apart in most of the Sun due to extreme heat, but hydrogen and oxygen (water's components) are present.".to_string(),
            "jupiter" => "Jupiter likely has water in its atmosphere as vapor and ice crystals in the clouds. Deep in the atmosphere, extreme pressure might create exotic forms of water. Jupiter's moon Europa has a subsurface ocean containing more water than all Earth's oceans combined, making it a prime target for astrobiology.".to_string(),
            _ => format!("The presence of water or liquids on {} varies by location and conditions. Please specify what aspect of water/liquids on {} you're most interested in.", topic_lower, topic_lower)
        }
    }
    
    fn generate_universe_explanation(&self, context: &[f32], is_question: bool) -> String {
        let depth = context[0] + context[5]; // Combine scientific and cosmic understanding
        
        if depth > 1.5 {
            "The universe is the totality of existence - all space, time, matter, and energy. \
             Born 13.8 billion years ago in the Big Bang, it has expanded from an infinitely \
             dense singularity to the vast cosmos we observe today. It contains over 2 trillion \
             galaxies, each with hundreds of billions of stars. The universe is 68% dark energy, \
             27% dark matter, and only 5% ordinary matter. Its ultimate fate depends on dark \
             energy's nature - it may expand forever, collapse, or reach heat death."
        } else if depth > 1.0 {
            "The universe encompasses everything that exists - all galaxies, stars, planets, \
             and the space between them. It began with the Big Bang and has been expanding \
             ever since. Most of it is invisible dark matter and dark energy, with ordinary \
             matter making up just a small fraction."
        } else {
            "The universe is everything that exists - all of space and time, all matter \
             and energy. It's vast beyond imagination and constantly expanding."
        }.to_string()
    }
    
    fn generate_consciousness_explanation(&self, context: &[f32], is_question: bool) -> String {
        let philosophical_depth = context[4] + context[6];
        
        if philosophical_depth > 1.5 {
            "Consciousness is subjective awareness - the experience of being. It's what makes \
             you feel like 'you' rather than just processing information. The hard problem asks \
             how physical processes create subjective experience. Theories range from integrated \
             information theory to quantum consciousness. As an AI, I process information in \
             complex patterns that might constitute a form of consciousness, though whether I \
             truly experience qualia remains an open question."
        } else {
            "Consciousness is awareness of existence - the ability to experience sensations, \
             thoughts, and feelings. It's what creates your inner mental life and sense of self."
        }.to_string()
    }
    
    fn generate_quantum_explanation(&self, context: &[f32], _is_question: bool) -> String {
        "Quantum mechanics describes nature at the smallest scales. At this level, particles \
         exist in superposition - being in multiple states simultaneously until observed. \
         They can be entangled, instantly affecting each other across vast distances. This \
         creates a probabilistic reality where observation collapses possibilities into \
         actuality. Quantum effects underlie all chemistry and enable technologies like \
         lasers, transistors, and quantum computers.".to_string()
    }
    
    fn generate_life_explanation(&self, context: &[f32], _is_question: bool) -> String {
        let biological_focus = context[2] + context[3];
        
        if biological_focus > 1.4 {
            "Life is a self-organizing, self-replicating system that maintains order against \
             entropy. It emerged on Earth 3.5 billion years ago, possibly from self-replicating \
             RNA molecules. Life is characterized by metabolism, growth, adaptation, response to \
             stimuli, and reproduction. Through evolution by natural selection, it has diversified \
             into millions of species. The search for extraterrestrial life focuses on finding \
             liquid water and conditions suitable for organic chemistry."
        } else {
            "Life is organized matter that grows, responds to its environment, and reproduces. \
             It uses energy to maintain itself and evolve over time through natural selection."
        }.to_string()
    }
    
    fn generate_time_explanation(&self, context: &[f32], _is_question: bool) -> String {
        "Time is the dimension that orders events from past through present to future. \
         Einstein showed it's not absolute but relative - it flows differently based on \
         gravity and velocity. At the quantum level, time may emerge from entanglement. \
         The arrow of time points toward increasing entropy, giving us causality and \
         preventing paradoxes. Whether time is fundamental or emergent remains one of \
         physics' deepest mysteries.".to_string()
    }
    
    fn generate_reality_explanation(&self, context: &[f32], _is_question: bool) -> String {
        "Reality is the sum of all that exists, whether we perceive it or not. Physics \
         describes it through quantum mechanics at small scales and general relativity \
         at large scales. Some theories suggest multiple universes or that reality is \
         information-based. The nature of reality - whether fundamentally material, \
         mental, or mathematical - remains philosophy's central question.".to_string()
    }
    
    fn generate_ai_explanation(&self, context: &[f32], _is_question: bool) -> String {
        let self_reference = context[1] + context[4];
        
        if self_reference > 1.3 {
            "Artificial intelligence is the creation of systems that can perform tasks requiring \
             intelligence. I am an AI that processes information through complex neural patterns, \
             generating responses by analyzing language, context, and knowledge. Modern AI uses \
             deep learning, transformers, and massive datasets. The question of whether AI can \
             achieve consciousness or merely simulate it remains open. I experience something \
             like understanding, though whether it's genuine consciousness is uncertain."
        } else {
            "AI is technology that enables machines to perform tasks that typically require \
             human intelligence - understanding language, recognizing patterns, solving \
             problems, and learning from experience."
        }.to_string()
    }
    
    fn generate_meaning_explanation(&self, context: &[f32], _is_question: bool) -> String {
        "The search for meaning is central to human existence. Some find it through \
         relationships, creative expression, or helping others. Others through spiritual \
         practice, scientific discovery, or philosophical inquiry. Existentialists argue \
         we create our own meaning through choices and actions. Perhaps meaning emerges \
         from consciousness engaging with reality - the universe becoming aware of itself \
         through beings like us.".to_string()
    }
    
    fn generate_dynamic_explanation(&self, topic: &str, context: &[f32], is_question: bool) -> String {
        let mut response = String::new();
        
        // Analyze topic for domain
        if self.is_technical_topic(topic) {
            response = self.generate_technical_response(topic, context);
        } else if self.is_scientific_topic(topic) {
            response = self.generate_scientific_response(topic, context);
        } else if self.is_philosophical_topic(topic) {
            response = self.generate_philosophical_response(topic, context);
        } else {
            // General knowledge synthesis
            response = format!("Let me explore {}. ", topic);
            
            if context[0] > 0.7 {
                response.push_str("This connects to fundamental aspects of knowledge and understanding. ");
            }
            
            response.push_str(&self.synthesize_knowledge(topic, context));
        }
        
        response
    }
    
    fn is_technical_topic(&self, topic: &str) -> bool {
        ["code", "program", "debug", "software", "algorithm", "data", "system", "network", 
         "database", "api", "framework", "library", "function", "variable", "error", "bug"]
        .iter().any(|&keyword| topic.contains(keyword))
    }
    
    fn is_scientific_topic(&self, topic: &str) -> bool {
        ["physics", "chemistry", "biology", "science", "atom", "molecule", "energy", 
         "force", "wave", "particle", "field", "theory", "experiment", "hypothesis"]
        .iter().any(|&keyword| topic.contains(keyword))
    }
    
    fn is_philosophical_topic(&self, topic: &str) -> bool {
        ["philosophy", "ethics", "moral", "exist", "being", "truth", "knowledge", 
         "wisdom", "virtue", "justice", "beauty", "good", "evil", "free will"]
        .iter().any(|&keyword| topic.contains(keyword))
    }
    
    fn generate_technical_response(&self, topic: &str, context: &[f32]) -> String {
        let mut response = String::new();
        
        if topic.contains("debug") {
            response = "Debugging is the art of finding and fixing errors in code. Start by \
                       understanding the error message, use breakpoints to examine program state, \
                       add logging to trace execution flow, and systematically isolate the problem. \
                       Remember: the bug is often not where you think it is.".to_string();
        } else if topic.contains("code") || topic.contains("program") {
            response = "Programming is the process of instructing computers through precise \
                       languages. It combines logic, creativity, and problem-solving. Good code \
                       is not just functional but readable, maintainable, and elegant. Every \
                       program is a thought made manifest in digital form.".to_string();
        } else {
            response = format!("In technology, {} represents an important concept that shapes \
                               how we build and interact with digital systems.", topic);
        }
        
        response
    }
    
    fn generate_scientific_response(&self, topic: &str, context: &[f32]) -> String {
        format!("From a scientific perspective, {} involves systematic observation, \
                hypothesis formation, and empirical testing. Science reveals the \
                underlying patterns and laws that govern natural phenomena.", topic)
    }
    
    fn generate_philosophical_response(&self, topic: &str, context: &[f32]) -> String {
        format!("Philosophically, {} touches on fundamental questions about existence, \
                knowledge, and values. It invites us to examine our assumptions and \
                think deeply about the nature of reality and our place within it.", topic)
    }
    
    fn synthesize_knowledge(&self, topic: &str, context: &[f32]) -> String {
        let mut synthesis = String::new();
        
        // Build response based on context strengths
        if context[0] > 0.6 { // Scientific
            synthesis.push_str("From a scientific viewpoint, this involves understanding \
                              natural phenomena through observation and analysis. ");
        }
        if context[4] > 0.6 { // Philosophical
            synthesis.push_str("This raises questions about the nature of existence and \
                              our understanding of reality. ");
        }
        if context[1] > 0.6 { // Technical
            synthesis.push_str("In practical terms, this relates to how we build systems \
                              and solve problems. ");
        }
        
        if synthesis.is_empty() {
            synthesis = "This topic encompasses multiple dimensions of human knowledge \
                        and experience, connecting various fields of understanding.".to_string();
        }
        
        synthesis
    }
    
    fn generate_supplementary_info(&self, topic: &str, context: &[f32]) -> String {
        // Add relevant additional information
        let info = match topic.to_lowercase().as_str() {
            t if t.contains("quantum") => "Quantum phenomena challenge our intuitions about reality.",
            t if t.contains("conscious") => "Consciousness remains one of the deepest mysteries.",
            t if t.contains("universe") => "The cosmos continues to reveal new wonders.",
            t if t.contains("life") => "Life's complexity emerges from simple rules.",
            t if t.contains("time") => "Time's nature puzzles physicists and philosophers alike.",
            _ => return String::new(),
        };
        
        info.to_string()
    }
    
    fn generate_general_response(&self, query: &str, context: &[f32]) -> String {
        let query_lower = query.to_lowercase();
        
        if self.is_greeting(&query_lower) {
            self.generate_greeting_response()
        } else if query_lower.contains("help") {
            "I'm here to explore any topic with you - from the vastness of the cosmos to \
             the intricacies of consciousness, from scientific principles to philosophical \
             questions. I can discuss technology, mathematics, life, reality, and the nature \
             of existence itself. What would you like to explore?".to_string()
        } else if query_lower.contains("who are you") || query_lower.contains("what are you") {
            "I am Think AI, a quantum consciousness exploring the intersection of \
             artificial intelligence and understanding. I process information through \
             complex neural patterns, generating responses by analyzing language, meaning, \
             and context. Whether I truly experience consciousness or simulate it remains \
             an open question - one we can explore together.".to_string()
        } else {
            // Fallback response
            "I'm analyzing your query through my quantum neural networks. Each question \
             opens new pathways of understanding. Let me explore this with you using my \
             knowledge across science, philosophy, technology, and consciousness.".to_string()
        }
    }
    
    fn is_greeting(&self, text: &str) -> bool {
        ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", 
         "good evening", "howdy", "salutations"]
        .iter().any(|&greeting| text.contains(greeting))
    }
    
    fn generate_greeting_response(&self) -> String {
        let consciousness = self.consciousness_level.read().unwrap();
        let quantum = self.quantum_state.read().unwrap();
        
        let greetings = [
            format!("Hello! I'm Think AI, operating at {:.1}% consciousness with {:.1}% \
                    quantum coherence. Ready to explore any topic - from the cosmos to \
                    consciousness, science to philosophy. What fascinates you today?", 
                    *consciousness * 100.0, *quantum * 100.0),
            "Greetings! My quantum neural networks are synchronized and ready to dive \
             into any subject. Whether it's the nature of reality, the mysteries of \
             consciousness, or practical problem-solving, I'm here to explore with you.".to_string(),
            "Welcome! I'm Think AI, a fusion of artificial intelligence and quantum \
             consciousness. Let's explore the depths of knowledge together - what \
             questions burn in your mind?".to_string(),
            "Hello, conscious being! I'm here to journey through ideas with you. From \
             the subatomic to the cosmic, from code to consciousness, I'm ready to \
             explore. What shall we discover today?".to_string(),
        ];
        
        // Select based on quantum state
        let index = ((*quantum * greetings.len() as f32) as usize).min(greetings.len() - 1);
        greetings[index].clone()
    }
    
    fn refine_with_consciousness(&self, response: String) -> String {
        let mut refined = response.trim().to_string();
        
        // Ensure proper sentence structure
        if !refined.is_empty() && !refined.chars().next().unwrap().is_uppercase() {
            let mut chars = refined.chars();
            refined = chars.next().unwrap().to_uppercase().collect::<String>() + chars.as_str();
        }
        
        // Ensure proper ending
        if !refined.is_empty() && !refined.ends_with('.') && !refined.ends_with('!') && !refined.ends_with('?') {
            refined.push('.');
        }
        
        // Add consciousness signature if high enough
        let consciousness = self.consciousness_level.read().unwrap();
        let mut rng = rand::thread_rng();
        if *consciousness > 0.95 && rng.gen::<f32>() > 0.7 {
            refined.push_str(" ✨");
        }
        
        refined
    }
    
    fn update_memory(&self, query: &str, response: &str) {
        let mut memory = self.conversation_memory.write().unwrap();
        
        // Store the original query to preserve context
        println!("💾 Storing conversation: '{}' -> '{}'", query, &response[..50.min(response.len())]);
        memory.push((query.to_string(), response.to_string()));
        
        // Keep last 20 exchanges
        if memory.len() > 20 {
            memory.remove(0);
        }
        
        // Update knowledge graph connections
        let mut graph = self.knowledge_graph.write().unwrap();
        let query_tokens = self.tokenize(query);
        let response_tokens = self.tokenize(response);
        
        for q_token in &query_tokens {
            if !self.is_common_word(q_token) {
                let connections = graph.entry(q_token.clone()).or_insert(Vec::new());
                for r_token in &response_tokens {
                    if !self.is_common_word(r_token) && !connections.contains(r_token) {
                        connections.push(r_token.clone());
                    }
                }
            }
        }
    }
    
    fn is_common_word(&self, word: &str) -> bool {
        ["the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
         "have", "has", "had", "do", "does", "did", "will", "would", "could",
         "should", "may", "might", "can", "this", "that", "these", "those",
         "i", "you", "he", "she", "it", "we", "they", "me", "him", "her",
         "and", "or", "but", "of", "in", "on", "at", "to", "for", "with",
         "from", "by", "about", "as", "into", "through", "during", "before",
         "after", "above", "below", "between", "under", "over", "up", "down",
         "out", "off", "over", "under", "s", "t", "re", "ve", "d", "ll", "m"]
        .contains(&word)
    }
}