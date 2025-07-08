//! Intelligent Response Selector - LLaMA decides between its own response, Think AI's response, or a combination
//! Ensures accurate, realistic, useful, and relevant data for users

use crate::{KnowledgeEngine, response_generator::ComponentResponseGenerator};
use think_ai_qwen::client::QwenClient;
use std::sync::Arc;
use tokio::sync::RwLock;
use std::time::Instant;

#[derive(Debug, Clone)]
pub struct ResponseCandidate {
    pub source: ResponseSource,
    pub content: String,
    pub confidence: f32,
    pub relevance_score: f32,
    pub response_time_ms: f64,
    pub metadata: ResponseMetadata,
}

#[derive(Debug, Clone)]
pub enum ResponseSource {
    ThinkAIKnowledge,  // From knowledge base
    LLaMAGenerated,    // From O(1) generator
    Combined,          // Merged response
}

#[derive(Debug, Clone)]
pub struct ResponseMetadata {
    pub has_specific_facts: bool,
    pub covers_topic_fully: bool,
    pub is_actionable: bool,
    pub contains_examples: bool,
    pub technical_accuracy: f32,
}

pub struct IntelligentResponseSelector {
    knowledge_engine: Arc<KnowledgeEngine>,
    response_generator: Arc<ComponentResponseGenerator>,
    qwen_client: Arc<QwenClient>,
    decision_history: Arc<RwLock<Vec<DecisionRecord>>>,
}

#[derive(Debug, Clone)]
struct DecisionRecord {
    query: String,
    selected_source: ResponseSource,
    reason: String,
    timestamp: u64,
}

impl IntelligentResponseSelector {
    pub fn new(
        knowledge_engine: Arc<KnowledgeEngine>,
        response_generator: Arc<ComponentResponseGenerator>,
    ) -> Self {
        Self {
            knowledge_engine,
            response_generator,
            qwen_client: Arc::new(QwenClient::new_with_defaults()),
            decision_history: Arc::new(RwLock::new(Vec::new())),
        }
    }
    
    /// Generate responses in parallel, always combine them, and refine with TinyLlama
    pub async fn get_best_response(&self, query: &str) -> (String, ResponseSource, f64) {
        let start = Instant::now();
        
        // Generate both responses in parallel
        let (llama_response, thinkai_response) = tokio::join!(
            self.generate_llama_response(query),
            self.generate_thinkai_response(query)
        );
        
        // Always combine both responses intelligently
        let combined_response = self.intelligent_combine(
            &llama_response.content,
            &thinkai_response.content,
            query,
            thinkai_response.metadata.has_specific_facts
        ).await;
        
        // Use Qwen for final relevancy and usefulness transformation
        let refined_response = self.qwen_client.generate_simple(
            &format!("Refine this response for relevance and usefulness to the query '{}': {}", query, combined_response),
            None
        ).await.unwrap_or(combined_response.clone());
        
        let elapsed = start.elapsed().as_secs_f64() * 1000.0;
        
        // Source is always Combined since we're merging both
        (refined_response, ResponseSource::Combined, elapsed)
    }
    
    /// Generate response using Qwen
    async fn generate_llama_response(&self, query: &str) -> ResponseCandidate {
        let start = Instant::now();
        let content = self.qwen_client.generate_simple(query, None)
            .await
            .unwrap_or_else(|_| "I encountered an error generating a response.".to_string());
        let response_time = start.elapsed().as_secs_f64() * 1000.0;
        
        ResponseCandidate {
            source: ResponseSource::LLaMAGenerated,
            content,
            confidence: 0.8, // Base confidence for O(1) generated
            relevance_score: 0.0, // Will be calculated
            response_time_ms: response_time,
            metadata: ResponseMetadata {
                has_specific_facts: false,
                covers_topic_fully: false,
                is_actionable: false,
                contains_examples: false,
                technical_accuracy: 0.7,
            },
        }
    }
    
    /// Generate response using Think AI knowledge system
    async fn generate_thinkai_response(&self, query: &str) -> ResponseCandidate {
        let start = Instant::now();
        let content = self.response_generator.generate_response(query);
        let response_time = start.elapsed().as_secs_f64() * 1000.0;
        
        // Better knowledge detection - check if we have relevant nodes with high match scores
        let query_lower = query.to_lowercase();
        let query_tokens: Vec<String> = query_lower
            .split_whitespace()
            .filter(|w| w.len() > 2 && !["what", "is", "the", "a", "an"].contains(w))
            .map(|s| s.to_string())
            .collect();
            
        let mut has_knowledge = false;
        let mut knowledge_confidence = 0.6;
        
        // Check multiple ways to find knowledge
        // 1. Direct query match
        if self.knowledge_engine.fast_query(&query).is_some() {
            has_knowledge = true;
            knowledge_confidence = 0.95;
        }
        
        // 2. Check for any key token matches
        if !has_knowledge {
            for token in &query_tokens {
                if let Some(results) = self.knowledge_engine.fast_query(token) {
                    if !results.is_empty() {
                        // Check if any result has high relevance to our query
                        for node in results {
                            let topic_lower = node.topic.to_lowercase();
                            if topic_lower == *token || topic_lower.split_whitespace().any(|w| w == token) {
                                has_knowledge = true;
                                knowledge_confidence = 0.9;
                                break;
                            }
                        }
                    }
                }
                if has_knowledge { break; }
            }
        }
        
        // 3. Check if response contains actual knowledge (not fallback)
        if !content.starts_with("I don't have specific information") && 
           !content.contains("Could you tell me more") &&
           !content.contains("I'd be happy to help") &&
           content.len() > 100 {
            has_knowledge = true;
            if knowledge_confidence < 0.8 {
                knowledge_confidence = 0.8;
            }
        }
        
        ResponseCandidate {
            source: ResponseSource::ThinkAIKnowledge,
            content: content.clone(),
            confidence: knowledge_confidence,
            relevance_score: 0.0, // Will be calculated
            response_time_ms: response_time,
            metadata: ResponseMetadata {
                has_specific_facts: has_knowledge,
                covers_topic_fully: has_knowledge,
                is_actionable: true,
                contains_examples: content.contains("example") || content.contains("such as") || content.contains("for instance"),
                technical_accuracy: if has_knowledge { 0.9 } else { 0.6 },
            },
        }
    }
    
    /// Analyze response quality and relevance
    async fn analyze_response(&self, response: &ResponseCandidate, query: &str) -> ResponseAnalysis {
        let query_tokens = self.tokenize(query);
        let response_tokens = self.tokenize(&response.content);
        
        // Calculate relevance score
        let mut relevance_score = 0.0;
        let mut matching_tokens = 0;
        
        for q_token in &query_tokens {
            if response_tokens.iter().any(|r| r.contains(q_token) || q_token.contains(r)) {
                matching_tokens += 1;
            }
        }
        
        if !query_tokens.is_empty() {
            relevance_score = matching_tokens as f32 / query_tokens.len() as f32;
        }
        
        // Check response quality indicators
        let has_structure = response.content.contains(". ") || response.content.contains(", ");
        let has_detail = response.content.len() > 100;
        let has_technical_terms = self.contains_technical_terms(&response.content);
        let is_complete = response.content.ends_with('.') || response.content.ends_with('!');
        
        ResponseAnalysis {
            relevance_score,
            has_structure,
            has_detail,
            has_technical_terms,
            is_complete,
            word_count: response_tokens.len(),
            readability_score: self.calculate_readability(&response.content),
        }
    }
    
    /// Intelligently combine responses based on their strengths
    async fn intelligent_combine(
        &self,
        llama_content: &str,
        thinkai_content: &str,
        query: &str,
        has_knowledge: bool,
    ) -> String {
        let query_lower = query.to_lowercase();
        let mut combined = String::new();
        
        // Extract key query tokens for relevance checking
        let query_tokens: Vec<String> = query_lower
            .split_whitespace()
            .filter(|w| w.len() > 3 && !["what", "how", "why", "when", "where", "which", "does", "this", "that", "the"].contains(w))
            .map(|s| s.to_string())
            .collect();
        
        // Parse both responses into sentences
        let thinkai_sentences: Vec<&str> = thinkai_content.split(". ")
            .filter(|s| !s.is_empty())
            .collect();
        let llama_sentences: Vec<&str> = llama_content.split(". ")
            .filter(|s| !s.is_empty())
            .collect();
        
        // If Think AI has knowledge, start with that as the foundation
        if has_knowledge && !thinkai_sentences.is_empty() {
            // Take the first 2 sentences from Think AI knowledge
            for (i, sentence) in thinkai_sentences.iter().take(2).enumerate() {
                if i == 0 {
                    combined.push_str(sentence);
                } else {
                    combined.push_str(". ");
                    combined.push_str(sentence);
                }
            }
            
            // Add valuable insights from LLaMA that are relevant to the query
            for sentence in llama_sentences.iter() {
                let sentence_lower = sentence.to_lowercase();
                
                // Check if this sentence is actually relevant to the query
                let is_relevant = query_tokens.iter().any(|token| {
                    token.len() > 3 && sentence_lower.contains(token)
                });
                
                if is_relevant &&
                   !self.is_redundant(sentence, &vec![combined.clone()]) && 
                   sentence.len() > 30 &&
                   !sentence_lower.contains("understanding") &&
                   !sentence_lower.contains("requires examining") &&
                   !sentence_lower.contains("what is") { // Avoid questions in responses
                    combined.push_str(". Additionally, ");
                    combined.push_str(&sentence_lower);
                    break; // Just add one complementary insight
                }
            }
        } else {
            // No specific knowledge, blend both responses
            // Start with LLaMA's opening
            if !llama_sentences.is_empty() {
                combined.push_str(llama_sentences[0]);
            }
            
            // Add Think AI's perspective if different
            if !thinkai_sentences.is_empty() && 
               !self.is_redundant(thinkai_sentences[0], &vec![combined.clone()]) {
                combined.push_str(". From another perspective, ");
                let sentence_lower = thinkai_sentences[0].to_lowercase();
                combined.push_str(&sentence_lower);
            }
            
            // Add any unique insights from either
            let mut sentences_added = 1;
            for sentence in llama_sentences.iter().skip(1).chain(thinkai_sentences.iter().skip(1)) {
                if sentences_added >= 3 { break; } // Keep it concise
                
                if !self.is_redundant(sentence, &vec![combined.clone()]) && 
                   sentence.len() > 30 {
                    combined.push_str(". ");
                    combined.push_str(sentence);
                    sentences_added += 1;
                }
            }
        }
        
        // Clean up
        combined = combined.replace(". .", ".");
        combined = combined.replace("  ", " ");
        combined = combined.trim().to_string();
        
        // Ensure proper ending
        if !combined.ends_with('.') && !combined.ends_with('!') && !combined.ends_with('?') {
            combined.push('.');
        }
        
        combined
    }
    
    /// Calculate overall quality score
    fn calculate_overall_score(&self, response: &ResponseCandidate, analysis: &ResponseAnalysis) -> f32 {
        let mut score = 0.0;
        
        // Weighted factors - prioritize knowledge-based responses
        score += response.relevance_score * 25.0;
        score += response.confidence * 35.0;  // Increased weight for confidence
        score += response.metadata.technical_accuracy * 20.0;
        
        // Bonus for actual knowledge
        if response.metadata.has_specific_facts {
            score += 15.0;  // Significant bonus for knowledge-based responses
        }
        
        if analysis.has_structure { score += 5.0; }
        if analysis.has_detail { score += 3.0; }
        if analysis.is_complete { score += 3.0; }
        if analysis.has_technical_terms { score += 4.0; }
        
        // Additional bonus for Think AI knowledge responses with high relevance
        if matches!(response.source, ResponseSource::ThinkAIKnowledge) && response.relevance_score > 0.7 {
            score += 10.0;
        }
        
        // Normalize
        score / 100.0
    }
    
    /// Determine if responses should be combined
    fn should_combine(
        &self,
        llama: &ResponseCandidate,
        thinkai: &ResponseCandidate,
        llama_analysis: &ResponseAnalysis,
        thinkai_analysis: &ResponseAnalysis,
    ) -> bool {
        // Combine if both have good but different strengths
        let llama_has_context = llama_analysis.has_structure && llama_analysis.readability_score > 0.7;
        let thinkai_has_facts = thinkai.metadata.has_specific_facts;
        
        // Don't combine if one is much worse
        let quality_difference = (llama.confidence - thinkai.confidence).abs();
        
        llama_has_context && thinkai_has_facts && quality_difference < 0.3
    }
    
    /// Intelligently combine two responses
    async fn combine_responses(&self, llama: &str, thinkai: &str, query: &str) -> String {
        // Extract the best parts of each response
        let query_lower = query.to_lowercase();
        
        // Start with Think AI if it has specific facts
        let mut combined = String::new();
        
        // Use Think AI's opening if it's more specific
        let thinkai_sentences: Vec<&str> = thinkai.split(". ").collect();
        let llama_sentences: Vec<&str> = llama.split(". ").collect();
        
        // Take the more specific opening
        if thinkai_sentences[0].len() > 50 && thinkai_sentences[0].contains(&query_lower) {
            combined.push_str(thinkai_sentences[0]);
            combined.push_str(". ");
        } else {
            combined.push_str(llama_sentences[0]);
            combined.push_str(". ");
        }
        
        // Add unique valuable content from both
        let mut added_content = vec![combined.clone()];
        
        // Add Think AI specifics if not redundant
        for sentence in thinkai_sentences.iter().skip(1) {
            if !self.is_redundant(sentence, &added_content) && sentence.len() > 20 {
                combined.push_str(sentence);
                combined.push_str(". ");
                added_content.push(sentence.to_string());
                break; // Limit length
            }
        }
        
        // Add LLaMA insights if not redundant
        for sentence in llama_sentences.iter().skip(1).take(2) {
            if !self.is_redundant(sentence, &added_content) && sentence.len() > 20 {
                combined.push_str(sentence);
                combined.push_str(". ");
                added_content.push(sentence.to_string());
            }
        }
        
        // Clean up
        combined = combined.replace(". .", ".");
        combined.trim().to_string()
    }
    
    /// Check if content is redundant
    fn is_redundant(&self, sentence: &str, existing: &[String]) -> bool {
        let tokens = self.tokenize(sentence);
        
        for existing_sentence in existing {
            let existing_tokens = self.tokenize(existing_sentence);
            let mut matches = 0;
            
            for token in &tokens {
                if existing_tokens.contains(token) {
                    matches += 1;
                }
            }
            
            // If more than 60% tokens match, consider redundant
            if tokens.len() > 0 && matches as f32 / tokens.len() as f32 > 0.6 {
                return true;
            }
        }
        
        false
    }
    
    /// Record decision for learning
    async fn record_decision(&self, query: &str, source: ResponseSource, reason: &str) {
        let mut history = self.decision_history.write().await;
        history.push(DecisionRecord {
            query: query.to_string(),
            selected_source: source,
            reason: reason.to_string(),
            timestamp: std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_secs(),
        });
        
        // Keep only last 100 decisions
        if history.len() > 100 {
            history.remove(0);
        }
    }
    
    /// Tokenize text
    fn tokenize(&self, text: &str) -> Vec<String> {
        text.to_lowercase()
            .split_whitespace()
            .map(|s| s.trim_matches(|c: char| !c.is_alphanumeric()).to_string())
            .filter(|s| !s.is_empty() && s.len() > 2)
            .collect()
    }
    
    /// Check for technical terms
    fn contains_technical_terms(&self, text: &str) -> bool {
        let technical_indicators = [
            "algorithm", "process", "system", "function", "structure",
            "mechanism", "principle", "theory", "model", "framework",
            "component", "element", "factor", "variable", "parameter"
        ];
        
        let text_lower = text.to_lowercase();
        technical_indicators.iter().any(|&term| text_lower.contains(term))
    }
    
    /// Calculate readability score
    fn calculate_readability(&self, text: &str) -> f32 {
        let sentences = text.matches(". ").count() + 1;
        let words = text.split_whitespace().count();
        
        if sentences == 0 || words == 0 {
            return 0.5;
        }
        
        let avg_sentence_length = words as f32 / sentences as f32;
        
        // Simple readability: shorter sentences are more readable
        if avg_sentence_length < 10.0 {
            0.9
        } else if avg_sentence_length < 20.0 {
            0.8
        } else if avg_sentence_length < 30.0 {
            0.6
        } else {
            0.4
        }
    }
}

#[derive(Debug)]
struct ResponseAnalysis {
    relevance_score: f32,
    has_structure: bool,
    has_detail: bool,
    has_technical_terms: bool,
    is_complete: bool,
    word_count: usize,
    readability_score: f32,
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[tokio::test]
    async fn test_response_selection() {
        // Test that selector picks the best response
        // Implementation would include mock responses and verification
    }
}