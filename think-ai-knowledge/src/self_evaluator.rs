//! Self-Evaluating Knowledge System - AI that questions itself and improves
//! 
//! This system makes Think AI:
//! 1. Ask itself questions about its knowledge base
//! 2. Search for answers in its own knowledge
//! 3. Evaluate response quality automatically
//! 4. Progressively improve answers for user relevance
//! 5. Run continuously in background with O(1) performance

use crate::{KnowledgeEngine, KnowledgeNode, KnowledgeDomain};
use crate::response_generator::ComponentResponseGenerator;
use std::sync::{Arc, RwLock};
use std::collections::{HashMap, VecDeque};
use std::time::{Duration, Instant, SystemTime, UNIX_EPOCH};
use tokio::time::sleep;
use serde::{Deserialize, Serialize};

/// Quality metrics for auto-evaluation
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ResponseQuality {
    pub relevance_score: f64,      // How relevant is the answer to the question
    pub completeness_score: f64,   // How complete is the answer
    pub actionability_score: f64,  // How actionable/useful is the answer
    pub clarity_score: f64,        // How clear and understandable
    pub factual_accuracy: f64,     // Estimated factual accuracy
    pub overall_score: f64,        // Weighted overall quality
}

/// Self-evaluation record for tracking improvements
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EvaluationRecord {
    pub question: String,
    pub answer: String,
    pub quality: ResponseQuality,
    pub timestamp: u64,
    pub iteration: u32,
    pub improvement_suggestions: Vec<String>,
}

/// Questions the AI generates to test itself
#[derive(Debug, Clone)]
pub struct SelfQuestion {
    pub question: String,
    pub domain: KnowledgeDomain,
    pub complexity_level: u8,  // 1-10 scale
    pub expected_answer_type: QuestionType,
}

#[derive(Debug, Clone)]
pub enum QuestionType {
    Definition,        // What is X?
    Explanation,       // How does X work?
    Comparison,        // How is X different from Y?
    Application,       // How can I use X?
    Problem,          // How do I solve X?
    Analysis,         // Why does X happen?
}

/// Self-Evaluating Knowledge System
pub struct SelfEvaluator {
    knowledge_engine: Arc<KnowledgeEngine>,
    response_generator: Arc<ComponentResponseGenerator>,
    evaluation_history: Arc<RwLock<VecDeque<EvaluationRecord>>>,
    question_queue: Arc<RwLock<VecDeque<SelfQuestion>>>,
    quality_improvements: Arc<RwLock<HashMap<String, f64>>>, // Track improvements by topic
    is_running: Arc<RwLock<bool>>,
    evaluation_cache: Arc<RwLock<HashMap<String, ResponseQuality>>>, // O(1) lookup
}

impl SelfEvaluator {
    pub fn new(knowledge_engine: Arc<KnowledgeEngine>, response_generator: Arc<ComponentResponseGenerator>) -> Self {
        Self {
            knowledge_engine,
            response_generator,
            evaluation_history: Arc::new(RwLock::new(VecDeque::with_capacity(1000))),
            question_queue: Arc::new(RwLock::new(VecDeque::new())),
            quality_improvements: Arc::new(RwLock::new(HashMap::new())),
            is_running: Arc::new(RwLock::new(false)),
            evaluation_cache: Arc::new(RwLock::new(HashMap::new())),
        }
    }

    /// Start the self-evaluation system in background
    pub async fn start_background_evaluation(&self) {
        // Check and set running state atomically
        {
            let mut running = self.is_running.write().unwrap();
            if *running {
                println!("🔄 Self-evaluator already running");
                return;
            }
            *running = true;
        } // Lock dropped here

        println!("🧠 Starting self-evaluation system...");
        
        // Generate initial questions about the knowledge base in background
        let evaluator_for_questions = self.clone_for_async();
        tokio::spawn(async move {
            evaluator_for_questions.generate_comprehensive_questions().await;
        });
        
        // Start evaluation loops
        let evaluator = self.clone_for_async();
        tokio::spawn(async move {
            evaluator.continuous_evaluation_loop().await;
        });

        let evaluator = self.clone_for_async();
        tokio::spawn(async move {
            evaluator.quality_improvement_loop().await;
        });

        println!("✅ Self-evaluation system active - AI now questioning itself for continuous improvement");
    }

    /// Generate questions about the knowledge base (lightweight, non-blocking)
    async fn generate_comprehensive_questions(&self) {
        println!("❓ Generating self-evaluation questions...");
        
        // Start with a minimal set of questions to avoid blocking
        let mut questions = Vec::new();
        
        // Generate only 1 question per domain to avoid blocking startup
        for domain in KnowledgeDomain::all_domains().iter().take(5) { // Only 5 domains for startup
            // Get just 1 sample node from this domain
            let domain_nodes = self.knowledge_engine.query_by_domain(domain.clone());
            
            if let Some(node) = domain_nodes.first() {
                // Generate just 1 question per node for startup
                questions.push(SelfQuestion {
                    question: format!("What is {}?", node.topic),
                    domain: domain.clone(),
                    complexity_level: 3,
                    expected_answer_type: QuestionType::Definition,
                });
            }
        }

        // Add just 2 meta-questions to avoid blocking
        questions.push(SelfQuestion {
            question: "How many knowledge domains do I have?".to_string(),
            domain: KnowledgeDomain::Philosophy,
            complexity_level: 2,
            expected_answer_type: QuestionType::Definition,
        });
        
        questions.push(SelfQuestion {
            question: "What is my primary function?".to_string(),
            domain: KnowledgeDomain::Philosophy,
            complexity_level: 2,
            expected_answer_type: QuestionType::Definition,
        });

        // Add to queue quickly
        let mut queue = self.question_queue.write().unwrap();
        for question in questions {
            queue.push_back(question);
        }
        
        println!("📝 Generated {} self-evaluation questions (lightweight startup)", queue.len());
        
        // Schedule more comprehensive question generation in background
        let evaluator = self.clone_for_async();
        tokio::spawn(async move {
            tokio::time::sleep(tokio::time::Duration::from_secs(10)).await; // Wait 10 seconds
            evaluator.generate_full_question_set().await;
        });
    }
    
    /// Generate the full comprehensive question set in background
    async fn generate_full_question_set(&self) {
        println!("🔄 Generating comprehensive question set in background...");
        
        let mut questions = Vec::new();
        
        // Generate questions for each domain (more comprehensive)
        for domain in KnowledgeDomain::all_domains() {
            let domain_nodes = self.knowledge_engine.query_by_domain(domain.clone());
            
            for node in domain_nodes.iter().take(2) { // 2 questions per domain for full set
                questions.extend(self.generate_questions_for_node(node, &domain));
            }
        }

        // Add meta-questions about the system itself
        questions.extend(self.generate_meta_questions());

        // Randomize and add to queue
        use std::collections::hash_map::DefaultHasher;
        use std::hash::{Hash, Hasher};
        
        let mut hasher = DefaultHasher::new();
        SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos().hash(&mut hasher);
        let _seed = hasher.finish();
        
        // Simple shuffle using seed
        questions.sort_by(|a, b| {
            let mut hasher = DefaultHasher::new();
            a.question.hash(&mut hasher);
            let a_hash = hasher.finish();
            let mut hasher = DefaultHasher::new();  
            b.question.hash(&mut hasher);
            let b_hash = hasher.finish();
            a_hash.cmp(&b_hash)
        });

        let mut queue = self.question_queue.write().unwrap();
        for question in questions {
            queue.push_back(question);
        }
        
        println!("📝 Generated {} total self-evaluation questions", queue.len());
    }

    /// Generate different types of questions for a knowledge node
    fn generate_questions_for_node(&self, node: &KnowledgeNode, domain: &KnowledgeDomain) -> Vec<SelfQuestion> {
        let mut questions = Vec::new();
        
        // Definition question
        questions.push(SelfQuestion {
            question: format!("What is {}?", node.topic),
            domain: domain.clone(),
            complexity_level: 3,
            expected_answer_type: QuestionType::Definition,
        });

        // Explanation question
        questions.push(SelfQuestion {
            question: format!("How does {} work?", node.topic),
            domain: domain.clone(),
            complexity_level: 5,
            expected_answer_type: QuestionType::Explanation,
        });

        // Application question
        questions.push(SelfQuestion {
            question: format!("How can I use {} in practice?", node.topic),
            domain: domain.clone(),
            complexity_level: 6,
            expected_answer_type: QuestionType::Application,
        });

        // Comparison question (if there are related concepts)
        if !node.related_concepts.is_empty() {
            let related = &node.related_concepts[0];
            questions.push(SelfQuestion {
                question: format!("What is the difference between {} and {}?", node.topic, related),
                domain: domain.clone(),
                complexity_level: 7,
                expected_answer_type: QuestionType::Comparison,
            });
        }

        questions
    }

    /// Generate meta-questions about the system's knowledge
    fn generate_meta_questions(&self) -> Vec<SelfQuestion> {
        vec![
            SelfQuestion {
                question: "What is artificial intelligence?".to_string(),
                domain: KnowledgeDomain::ComputerScience,
                complexity_level: 4,
                expected_answer_type: QuestionType::Definition,
            },
            SelfQuestion {
                question: "How does machine learning work?".to_string(),
                domain: KnowledgeDomain::ComputerScience,
                complexity_level: 6,
                expected_answer_type: QuestionType::Explanation,
            },
            SelfQuestion {
                question: "What is consciousness?".to_string(),
                domain: KnowledgeDomain::Philosophy,
                complexity_level: 8,
                expected_answer_type: QuestionType::Definition,
            },
            SelfQuestion {
                question: "How can quantum mechanics be applied in computing?".to_string(),
                domain: KnowledgeDomain::Physics,
                complexity_level: 9,
                expected_answer_type: QuestionType::Application,
            },
        ]
    }

    /// Main evaluation loop that continuously processes questions
    async fn continuous_evaluation_loop(&self) {
        let mut iteration = 0u32;
        
        loop {
            // Check if we should continue running
            let should_continue = {
                let running = self.is_running.read().unwrap();
                *running
            };
            
            if !should_continue {
                break;
            }

            // Process a question from the queue
            let question = {
                let mut queue = self.question_queue.write().unwrap();
                queue.pop_front()
            };

            if let Some(q) = question {
                iteration += 1;
                
                // Ask the question and get answer
                let start = Instant::now();
                let answer = self.response_generator.generate_response(&q.question);
                let response_time = start.elapsed();
                
                // Evaluate the quality
                let quality = self.evaluate_response_quality(&q, &answer).await;
                
                // Create evaluation record
                let record = EvaluationRecord {
                    question: q.question.clone(),
                    answer: answer.clone(),
                    quality: quality.clone(),
                    timestamp: SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_secs(),
                    iteration,
                    improvement_suggestions: self.generate_improvement_suggestions(&q, &answer, &quality),
                };

                // Store the evaluation
                {
                    let mut history = self.evaluation_history.write().unwrap();
                    history.push_back(record);
                    if history.len() > 1000 {
                        history.pop_front(); // Keep memory bounded
                    }
                }

                // Cache the quality for O(1) lookup
                {
                    let mut cache = self.evaluation_cache.write().unwrap();
                    cache.insert(q.question.clone(), quality.clone());
                }

                // Log evaluation results
                if iteration % 10 == 0 {
                    println!("🔍 Self-eval #{}: {} (Quality: {:.2}) [{}ms]", 
                        iteration, 
                        &q.question[..50.min(q.question.len())],
                        quality.overall_score,
                        response_time.as_millis()
                    );
                }

                // Add follow-up questions if the quality is low
                if quality.overall_score < 0.7 {
                    self.generate_follow_up_questions(&q).await;
                }

            } else {
                // No questions in queue, generate more
                self.generate_adaptive_questions().await;
                sleep(Duration::from_millis(100)).await; // Prevent busy waiting
            }

            // Small delay to prevent overwhelming the system
            sleep(Duration::from_millis(50)).await;
        }
    }

    /// Quality improvement loop that analyzes patterns and suggests improvements
    async fn quality_improvement_loop(&self) {
        loop {
            sleep(Duration::from_secs(30)).await; // Run every 30 seconds

            // Check if running without holding lock across await
            let should_continue = {
                let running = self.is_running.read().unwrap();
                *running
            };
            
            if !should_continue {
                break;
            }

            // Analyze recent evaluations for patterns
            let improvements = self.analyze_quality_patterns().await;
            
            if !improvements.is_empty() {
                println!("💡 Quality improvements identified: {} patterns", improvements.len());
                
                // Store improvements
                let mut quality_map = self.quality_improvements.write().unwrap();
                for (topic, score) in improvements {
                    quality_map.insert(topic, score);
                }
            }
        }
    }

    /// Evaluate the quality of a response using multiple criteria
    async fn evaluate_response_quality(&self, question: &SelfQuestion, answer: &str) -> ResponseQuality {
        // Fast heuristic-based evaluation for O(1) performance
        
        let relevance_score = self.calculate_relevance_score(question, answer);
        let completeness_score = self.calculate_completeness_score(question, answer);
        let actionability_score = self.calculate_actionability_score(question, answer);
        let clarity_score = self.calculate_clarity_score(answer);
        let factual_accuracy = self.estimate_factual_accuracy(answer);

        // Weighted overall score
        let overall_score = (
            relevance_score * 0.25 +
            completeness_score * 0.20 +
            actionability_score * 0.25 +
            clarity_score * 0.15 +
            factual_accuracy * 0.15
        );

        ResponseQuality {
            relevance_score,
            completeness_score,
            actionability_score,
            clarity_score,
            factual_accuracy,
            overall_score,
        }
    }

    /// Calculate relevance score (how well does the answer address the question)
    fn calculate_relevance_score(&self, question: &SelfQuestion, answer: &str) -> f64 {
        let question_lower = question.question.to_lowercase();
        let answer_lower = answer.to_lowercase();
        
        // Extract key terms from question
        let question_terms: Vec<&str> = question_lower
            .split_whitespace()
            .filter(|w| w.len() > 3 && !["what", "how", "why", "when", "where", "does", "can", "will", "would", "should"].contains(w))
            .collect();

        if question_terms.is_empty() {
            return 0.5; // Neutral score if no key terms
        }

        // Count how many question terms appear in the answer
        let mut matches = 0;
        for term in &question_terms {
            if answer_lower.contains(term) {
                matches += 1;
            }
        }

        let base_score = matches as f64 / question_terms.len() as f64;
        
        // Bonus for direct question answering patterns
        let bonus = if answer_lower.starts_with(&question_terms[0]) || 
                      answer_lower.contains("is a") || 
                      answer_lower.contains("refers to") ||
                      answer_lower.contains("involves") {
            0.2
        } else {
            0.0
        };

        (base_score + bonus).min(1.0)
    }

    /// Calculate completeness score (how comprehensive is the answer)
    fn calculate_completeness_score(&self, question: &SelfQuestion, answer: &str) -> f64 {
        let word_count = answer.split_whitespace().count();
        let sentence_count = answer.split('.').count();
        
        // Expected length based on question complexity
        let expected_words = match question.complexity_level {
            1..=3 => 30,   // Simple questions need shorter answers
            4..=6 => 60,   // Medium complexity
            7..=8 => 100,  // Complex questions need longer answers
            _ => 150,      // Very complex
        };

        // Score based on how close to expected length
        let length_score = if word_count == 0 {
            0.0
        } else if word_count < expected_words / 2 {
            (word_count as f64) / (expected_words as f64 / 2.0)
        } else if word_count > expected_words * 2 {
            0.8 // Penalize overly long answers
        } else {
            1.0
        };

        // Bonus for good structure (multiple sentences)
        let structure_bonus = if sentence_count > 1 { 0.1 } else { 0.0 };
        
        (length_score + structure_bonus).min(1.0)
    }

    /// Calculate actionability score (how useful/actionable is the answer)
    fn calculate_actionability_score(&self, question: &SelfQuestion, answer: &str) -> f64 {
        let answer_lower = answer.to_lowercase();
        
        // Look for actionable keywords
        let actionable_indicators = [
            "use", "apply", "implement", "try", "consider", "practice",
            "step", "method", "approach", "technique", "strategy",
            "example", "instance", "case", "application", "helpful",
            "useful", "practical", "real-world", "can", "will"
        ];

        let mut actionable_count = 0;
        for indicator in &actionable_indicators {
            if answer_lower.contains(indicator) {
                actionable_count += 1;
            }
        }

        // Score based on question type expectations
        let expected_actionability = match question.expected_answer_type {
            QuestionType::Application => 0.8,  // Should be highly actionable
            QuestionType::Problem => 0.9,      // Should provide solutions
            QuestionType::Explanation => 0.6,  // Moderate actionability
            QuestionType::Definition => 0.3,   // Low actionability expected
            QuestionType::Comparison => 0.4,   // Moderate actionability
            QuestionType::Analysis => 0.5,     // Moderate actionability
        };

        let base_score = (actionable_count as f64 * 0.1).min(0.8);
        let adjusted_score = base_score / expected_actionability;
        
        adjusted_score.min(1.0)
    }

    /// Calculate clarity score (how clear and understandable is the answer)
    fn calculate_clarity_score(&self, answer: &str) -> f64 {
        if answer.is_empty() {
            return 0.0;
        }

        let words = answer.split_whitespace().collect::<Vec<_>>();
        let word_count = words.len();
        
        if word_count == 0 {
            return 0.0;
        }

        // Average word length (shorter words are generally clearer)
        let avg_word_length = words.iter()
            .map(|w| w.len())
            .sum::<usize>() as f64 / word_count as f64;

        // Sentence length (shorter sentences are clearer)
        let sentences: Vec<&str> = answer.split('.').filter(|s| !s.trim().is_empty()).collect();
        let avg_sentence_length = if sentences.is_empty() {
            word_count as f64
        } else {
            word_count as f64 / sentences.len() as f64
        };

        // Clarity scoring
        let word_clarity = if avg_word_length > 8.0 { 0.5 } else { 1.0 - (avg_word_length - 4.0) / 8.0 };
        let sentence_clarity = if avg_sentence_length > 20.0 { 0.5 } else { 1.0 - (avg_sentence_length - 10.0) / 20.0 };
        
        // Bonus for good structure indicators
        let structure_bonus = if answer.contains("First") || answer.contains("Additionally") || answer.contains("Furthermore") {
            0.1
        } else {
            0.0
        };

        ((word_clarity * 0.4 + sentence_clarity * 0.6) + structure_bonus).min(1.0).max(0.0)
    }

    /// Estimate factual accuracy (heuristic-based)
    fn estimate_factual_accuracy(&self, answer: &str) -> f64 {
        let answer_lower = answer.to_lowercase();
        
        // Look for uncertainty indicators (which can be good - shows honesty)
        let uncertainty_indicators = ["approximately", "about", "roughly", "estimated", "likely", "probably", "may", "might"];
        let uncertainty_count = uncertainty_indicators.iter()
            .filter(|&indicator| answer_lower.contains(indicator))
            .count();

        // Look for confidence indicators
        let confidence_indicators = ["is", "are", "was", "were", "consists", "contains", "includes"];
        let confidence_count = confidence_indicators.iter()
            .filter(|&indicator| answer_lower.contains(indicator))
            .count();

        // Look for problematic patterns
        let problematic_patterns = ["i don't know", "i'm not sure", "unclear", "uncertain"];
        let problematic_count = problematic_patterns.iter()
            .filter(|&pattern| answer_lower.contains(pattern))
            .count();

        // Base score from confidence vs uncertainty ratio
        let base_score = if confidence_count + uncertainty_count == 0 {
            0.7 // Neutral
        } else {
            (confidence_count as f64) / (confidence_count + uncertainty_count * 2) as f64
        };

        // Penalty for problematic patterns
        let penalty = problematic_count as f64 * 0.2;
        
        // Bonus for specific, detailed information
        let specificity_bonus = if answer.len() > 100 && answer.contains("research") || answer.contains("study") {
            0.1
        } else {
            0.0
        };

        (base_score - penalty + specificity_bonus).min(1.0).max(0.1)
    }

    /// Generate improvement suggestions based on quality analysis
    fn generate_improvement_suggestions(&self, question: &SelfQuestion, answer: &str, quality: &ResponseQuality) -> Vec<String> {
        let mut suggestions = Vec::new();

        if quality.relevance_score < 0.6 {
            suggestions.push("Improve relevance: Ensure answer directly addresses the question asked".to_string());
        }

        if quality.completeness_score < 0.5 {
            suggestions.push("Improve completeness: Provide more comprehensive information".to_string());
        }

        if quality.actionability_score < 0.4 && matches!(question.expected_answer_type, QuestionType::Application | QuestionType::Problem) {
            suggestions.push("Improve actionability: Include practical steps or examples".to_string());
        }

        if quality.clarity_score < 0.6 {
            suggestions.push("Improve clarity: Use simpler language and shorter sentences".to_string());
        }

        if quality.factual_accuracy < 0.7 {
            suggestions.push("Improve accuracy: Verify facts and reduce uncertain language".to_string());
        }

        if suggestions.is_empty() {
            suggestions.push("Response quality is good - continue current approach".to_string());
        }

        suggestions
    }

    /// Generate follow-up questions for low-quality responses
    async fn generate_follow_up_questions(&self, original_question: &SelfQuestion) {
        let follow_ups = vec![
            SelfQuestion {
                question: format!("Can you explain {} in simpler terms?", extract_main_topic(&original_question.question)),
                domain: original_question.domain.clone(),
                complexity_level: original_question.complexity_level.saturating_sub(2),
                expected_answer_type: QuestionType::Explanation,
            },
            SelfQuestion {
                question: format!("What are practical examples of {}?", extract_main_topic(&original_question.question)),
                domain: original_question.domain.clone(),
                complexity_level: original_question.complexity_level,
                expected_answer_type: QuestionType::Application,
            },
        ];

        let mut queue = self.question_queue.write().unwrap();
        for question in follow_ups {
            queue.push_back(question);
        }
    }

    /// Generate adaptive questions based on knowledge gaps
    async fn generate_adaptive_questions(&self) {
        let stats = self.knowledge_engine.get_stats();
        
        // Find domains with fewer evaluations
        let evaluation_counts = self.get_domain_evaluation_counts().await;
        let mut new_questions = Vec::new();

        for domain in KnowledgeDomain::all_domains() {
            let count = evaluation_counts.get(&domain).unwrap_or(&0);
            if *count < 5 { // Generate more questions for under-evaluated domains
                let nodes = self.knowledge_engine.query_by_domain(domain.clone());
                for node in nodes.iter().take(2) {
                    new_questions.extend(self.generate_questions_for_node(node, &domain));
                }
            }
        }

        if !new_questions.is_empty() {
            let mut queue = self.question_queue.write().unwrap();
            for question in new_questions {
                queue.push_back(question);
            }
        }
    }

    /// Analyze quality patterns across evaluations
    async fn analyze_quality_patterns(&self) -> HashMap<String, f64> {
        let history = self.evaluation_history.read().unwrap();
        let mut improvements = HashMap::new();

        // Group evaluations by topic/domain
        let mut topic_scores: HashMap<String, Vec<f64>> = HashMap::new();
        
        for record in history.iter().rev().take(100) { // Analyze recent 100 evaluations
            let topic = extract_main_topic(&record.question);
            topic_scores.entry(topic).or_insert_with(Vec::new).push(record.quality.overall_score);
        }

        // Calculate improvement trends
        for (topic, scores) in topic_scores {
            if scores.len() >= 3 {
                let recent_avg = scores.iter().take(3).sum::<f64>() / 3.0;
                let older_avg = scores.iter().skip(3).sum::<f64>() / (scores.len() - 3) as f64;
                
                if recent_avg > older_avg + 0.1 { // Significant improvement
                    improvements.insert(topic, recent_avg - older_avg);
                }
            }
        }

        improvements
    }

    /// Get evaluation counts by domain
    async fn get_domain_evaluation_counts(&self) -> HashMap<KnowledgeDomain, usize> {
        let history = self.evaluation_history.read().unwrap();
        let mut counts = HashMap::new();

        for record in history.iter() {
            // Map question to domain (simplified heuristic)
            let domain = self.infer_domain_from_question(&record.question);
            *counts.entry(domain).or_insert(0) += 1;
        }

        counts
    }

    /// Simple domain inference from question content
    fn infer_domain_from_question(&self, question: &str) -> KnowledgeDomain {
        let question_lower = question.to_lowercase();
        
        if question_lower.contains("computer") || question_lower.contains("software") || question_lower.contains("programming") {
            KnowledgeDomain::ComputerScience
        } else if question_lower.contains("quantum") || question_lower.contains("physics") || question_lower.contains("energy") {
            KnowledgeDomain::Physics
        } else if question_lower.contains("consciousness") || question_lower.contains("philosophy") || question_lower.contains("meaning") {
            KnowledgeDomain::Philosophy
        } else if question_lower.contains("biology") || question_lower.contains("life") || question_lower.contains("organism") {
            KnowledgeDomain::Biology
        } else if question_lower.contains("math") || question_lower.contains("number") || question_lower.contains("calculate") {
            KnowledgeDomain::Mathematics
        } else if question_lower.contains("astronomy") || question_lower.contains("space") || question_lower.contains("universe") {
            KnowledgeDomain::Astronomy
        } else {
            KnowledgeDomain::Philosophy // Default
        }
    }

    /// Clone for async operations
    fn clone_for_async(&self) -> SelfEvaluatorAsync {
        SelfEvaluatorAsync {
            knowledge_engine: self.knowledge_engine.clone(),
            response_generator: self.response_generator.clone(),
            evaluation_history: self.evaluation_history.clone(),
            question_queue: self.question_queue.clone(),
            quality_improvements: self.quality_improvements.clone(),
            is_running: self.is_running.clone(),
            evaluation_cache: self.evaluation_cache.clone(),
        }
    }

    /// Stop the self-evaluation system
    pub fn stop(&self) {
        let mut running = self.is_running.write().unwrap();
        *running = false;
        println!("🛑 Self-evaluation system stopped");
    }

    /// Get current evaluation statistics
    pub fn get_evaluation_stats(&self) -> EvaluationStats {
        let history = self.evaluation_history.read().unwrap();
        let quality_map = self.quality_improvements.read().unwrap();
        
        let total_evaluations = history.len();
        let avg_quality = if total_evaluations > 0 {
            history.iter().map(|r| r.quality.overall_score).sum::<f64>() / total_evaluations as f64
        } else {
            0.0
        };

        let recent_quality = if total_evaluations >= 10 {
            history.iter().rev().take(10).map(|r| r.quality.overall_score).sum::<f64>() / 10.0
        } else {
            avg_quality
        };

        EvaluationStats {
            total_evaluations,
            average_quality: avg_quality,
            recent_quality,
            improvement_areas: quality_map.len(),
            is_running: *self.is_running.read().unwrap(),
        }
    }
}

/// Async version for background tasks
#[derive(Clone)]
struct SelfEvaluatorAsync {
    knowledge_engine: Arc<KnowledgeEngine>,
    response_generator: Arc<ComponentResponseGenerator>,
    evaluation_history: Arc<RwLock<VecDeque<EvaluationRecord>>>,
    question_queue: Arc<RwLock<VecDeque<SelfQuestion>>>,
    quality_improvements: Arc<RwLock<HashMap<String, f64>>>,
    is_running: Arc<RwLock<bool>>,
    evaluation_cache: Arc<RwLock<HashMap<String, ResponseQuality>>>,
}

impl SelfEvaluatorAsync {
    async fn continuous_evaluation_loop(&self) {
        let mut iteration = 0u32;
        
        loop {
            // Check if we should continue running
            let should_continue = {
                let running = self.is_running.read().unwrap();
                *running
            };
            
            if !should_continue {
                break;
            }

            // Process a question from the queue
            let question = {
                let mut queue = self.question_queue.write().unwrap();
                queue.pop_front()
            };

            if let Some(q) = question {
                iteration += 1;
                
                // Ask the question and get answer
                let start = Instant::now();
                let answer = self.response_generator.generate_response(&q.question);
                let response_time = start.elapsed();
                
                // Evaluate the quality using the same logic as the main struct
                let quality = self.evaluate_response_quality(&q, &answer).await;
                
                // Create evaluation record
                let record = EvaluationRecord {
                    question: q.question.clone(),
                    answer: answer.clone(),
                    quality: quality.clone(),
                    timestamp: SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_secs(),
                    iteration,
                    improvement_suggestions: self.generate_improvement_suggestions(&q, &answer, &quality),
                };

                // Store the evaluation
                {
                    let mut history = self.evaluation_history.write().unwrap();
                    history.push_back(record);
                    if history.len() > 1000 {
                        history.pop_front();
                    }
                }

                // Cache the quality for O(1) lookup
                {
                    let mut cache = self.evaluation_cache.write().unwrap();
                    cache.insert(q.question.clone(), quality.clone());
                }

                // Log evaluation results
                if iteration % 10 == 0 {
                    println!("🔍 Self-eval #{}: {} (Quality: {:.2}) [{}ms]", 
                        iteration, 
                        &q.question[..50.min(q.question.len())],
                        quality.overall_score,
                        response_time.as_millis()
                    );
                }

                // Add follow-up questions if the quality is low
                if quality.overall_score < 0.7 {
                    self.generate_follow_up_questions(&q).await;
                }

            } else {
                // No questions in queue, generate more
                self.generate_adaptive_questions().await;
                sleep(Duration::from_millis(100)).await;
            }

            sleep(Duration::from_millis(50)).await;
        }
    }

    async fn quality_improvement_loop(&self) {
        loop {
            sleep(Duration::from_secs(30)).await;

            // Check if running without holding lock across await
            let should_continue = {
                let running = self.is_running.read().unwrap();
                *running
            };
            
            if !should_continue {
                break;
            }

            let improvements = self.analyze_quality_patterns().await;
            
            if !improvements.is_empty() {
                println!("💡 Quality improvements identified: {} patterns", improvements.len());
                
                let mut quality_map = self.quality_improvements.write().unwrap();
                for (topic, score) in improvements {
                    quality_map.insert(topic, score);
                }
            }
        }
    }

    // Copy the evaluation methods from the main struct
    async fn evaluate_response_quality(&self, question: &SelfQuestion, answer: &str) -> ResponseQuality {
        let relevance_score = self.calculate_relevance_score(question, answer);
        let completeness_score = self.calculate_completeness_score(question, answer);
        let actionability_score = self.calculate_actionability_score(question, answer);
        let clarity_score = self.calculate_clarity_score(answer);
        let factual_accuracy = self.estimate_factual_accuracy(answer);

        let overall_score = (
            relevance_score * 0.25 +
            completeness_score * 0.20 +
            actionability_score * 0.25 +
            clarity_score * 0.15 +
            factual_accuracy * 0.15
        );

        ResponseQuality {
            relevance_score,
            completeness_score,
            actionability_score,
            clarity_score,
            factual_accuracy,
            overall_score,
        }
    }

    // Include all the calculation methods...
    fn calculate_relevance_score(&self, question: &SelfQuestion, answer: &str) -> f64 {
        let question_lower = question.question.to_lowercase();
        let answer_lower = answer.to_lowercase();
        
        let question_terms: Vec<&str> = question_lower
            .split_whitespace()
            .filter(|w| w.len() > 3 && !["what", "how", "why", "when", "where", "does", "can", "will", "would", "should"].contains(w))
            .collect();

        if question_terms.is_empty() {
            return 0.5;
        }

        let mut matches = 0;
        for term in &question_terms {
            if answer_lower.contains(term) {
                matches += 1;
            }
        }

        let base_score = matches as f64 / question_terms.len() as f64;
        
        let bonus = if answer_lower.starts_with(&question_terms[0]) || 
                      answer_lower.contains("is a") || 
                      answer_lower.contains("refers to") ||
                      answer_lower.contains("involves") {
            0.2
        } else {
            0.0
        };

        (base_score + bonus).min(1.0)
    }

    fn calculate_completeness_score(&self, question: &SelfQuestion, answer: &str) -> f64 {
        let word_count = answer.split_whitespace().count();
        let sentence_count = answer.split('.').count();
        
        let expected_words = match question.complexity_level {
            1..=3 => 30,
            4..=6 => 60,
            7..=8 => 100,
            _ => 150,
        };

        let length_score = if word_count == 0 {
            0.0
        } else if word_count < expected_words / 2 {
            (word_count as f64) / (expected_words as f64 / 2.0)
        } else if word_count > expected_words * 2 {
            0.8
        } else {
            1.0
        };

        let structure_bonus = if sentence_count > 1 { 0.1 } else { 0.0 };
        
        (length_score + structure_bonus).min(1.0)
    }

    fn calculate_actionability_score(&self, question: &SelfQuestion, answer: &str) -> f64 {
        let answer_lower = answer.to_lowercase();
        
        let actionable_indicators = [
            "use", "apply", "implement", "try", "consider", "practice",
            "step", "method", "approach", "technique", "strategy",
            "example", "instance", "case", "application", "helpful",
            "useful", "practical", "real-world", "can", "will"
        ];

        let mut actionable_count = 0;
        for indicator in &actionable_indicators {
            if answer_lower.contains(indicator) {
                actionable_count += 1;
            }
        }

        let expected_actionability = match question.expected_answer_type {
            QuestionType::Application => 0.8,
            QuestionType::Problem => 0.9,
            QuestionType::Explanation => 0.6,
            QuestionType::Definition => 0.3,
            QuestionType::Comparison => 0.4,
            QuestionType::Analysis => 0.5,
        };

        let base_score = (actionable_count as f64 * 0.1).min(0.8);
        let adjusted_score = base_score / expected_actionability;
        
        adjusted_score.min(1.0)
    }

    fn calculate_clarity_score(&self, answer: &str) -> f64 {
        if answer.is_empty() {
            return 0.0;
        }

        let words = answer.split_whitespace().collect::<Vec<_>>();
        let word_count = words.len();
        
        if word_count == 0 {
            return 0.0;
        }

        let avg_word_length = words.iter()
            .map(|w| w.len())
            .sum::<usize>() as f64 / word_count as f64;

        let sentences: Vec<&str> = answer.split('.').filter(|s| !s.trim().is_empty()).collect();
        let avg_sentence_length = if sentences.is_empty() {
            word_count as f64
        } else {
            word_count as f64 / sentences.len() as f64
        };

        let word_clarity = if avg_word_length > 8.0 { 0.5 } else { 1.0 - (avg_word_length - 4.0) / 8.0 };
        let sentence_clarity = if avg_sentence_length > 20.0 { 0.5 } else { 1.0 - (avg_sentence_length - 10.0) / 20.0 };
        
        let structure_bonus = if answer.contains("First") || answer.contains("Additionally") || answer.contains("Furthermore") {
            0.1
        } else {
            0.0
        };

        ((word_clarity * 0.4 + sentence_clarity * 0.6) + structure_bonus).min(1.0).max(0.0)
    }

    fn estimate_factual_accuracy(&self, answer: &str) -> f64 {
        let answer_lower = answer.to_lowercase();
        
        let uncertainty_indicators = ["approximately", "about", "roughly", "estimated", "likely", "probably", "may", "might"];
        let uncertainty_count = uncertainty_indicators.iter()
            .filter(|&indicator| answer_lower.contains(indicator))
            .count();

        let confidence_indicators = ["is", "are", "was", "were", "consists", "contains", "includes"];
        let confidence_count = confidence_indicators.iter()
            .filter(|&indicator| answer_lower.contains(indicator))
            .count();

        let problematic_patterns = ["i don't know", "i'm not sure", "unclear", "uncertain"];
        let problematic_count = problematic_patterns.iter()
            .filter(|&pattern| answer_lower.contains(pattern))
            .count();

        let base_score = if confidence_count + uncertainty_count == 0 {
            0.7
        } else {
            (confidence_count as f64) / (confidence_count + uncertainty_count * 2) as f64
        };

        let penalty = problematic_count as f64 * 0.2;
        
        let specificity_bonus = if answer.len() > 100 && answer.contains("research") || answer.contains("study") {
            0.1
        } else {
            0.0
        };

        (base_score - penalty + specificity_bonus).min(1.0).max(0.1)
    }

    fn generate_improvement_suggestions(&self, question: &SelfQuestion, answer: &str, quality: &ResponseQuality) -> Vec<String> {
        let mut suggestions = Vec::new();

        if quality.relevance_score < 0.6 {
            suggestions.push("Improve relevance: Ensure answer directly addresses the question asked".to_string());
        }

        if quality.completeness_score < 0.5 {
            suggestions.push("Improve completeness: Provide more comprehensive information".to_string());
        }

        if quality.actionability_score < 0.4 && matches!(question.expected_answer_type, QuestionType::Application | QuestionType::Problem) {
            suggestions.push("Improve actionability: Include practical steps or examples".to_string());
        }

        if quality.clarity_score < 0.6 {
            suggestions.push("Improve clarity: Use simpler language and shorter sentences".to_string());
        }

        if quality.factual_accuracy < 0.7 {
            suggestions.push("Improve accuracy: Verify facts and reduce uncertain language".to_string());
        }

        if suggestions.is_empty() {
            suggestions.push("Response quality is good - continue current approach".to_string());
        }

        suggestions
    }

    async fn generate_follow_up_questions(&self, original_question: &SelfQuestion) {
        let follow_ups = vec![
            SelfQuestion {
                question: format!("Can you explain {} in simpler terms?", extract_main_topic(&original_question.question)),
                domain: original_question.domain.clone(),
                complexity_level: original_question.complexity_level.saturating_sub(2),
                expected_answer_type: QuestionType::Explanation,
            },
            SelfQuestion {
                question: format!("What are practical examples of {}?", extract_main_topic(&original_question.question)),
                domain: original_question.domain.clone(),
                complexity_level: original_question.complexity_level,
                expected_answer_type: QuestionType::Application,
            },
        ];

        let mut queue = self.question_queue.write().unwrap();
        for question in follow_ups {
            queue.push_back(question);
        }
    }

    async fn generate_adaptive_questions(&self) {
        let evaluation_counts = self.get_domain_evaluation_counts().await;
        let mut new_questions = Vec::new();

        for domain in KnowledgeDomain::all_domains() {
            let count = evaluation_counts.get(&domain).unwrap_or(&0);
            if *count < 5 {
                let nodes = self.knowledge_engine.query_by_domain(domain.clone());
                for node in nodes.iter().take(2) {
                    new_questions.extend(self.generate_questions_for_node(node, &domain));
                }
            }
        }

        if !new_questions.is_empty() {
            let mut queue = self.question_queue.write().unwrap();
            for question in new_questions {
                queue.push_back(question);
            }
        }
    }

    fn generate_questions_for_node(&self, node: &KnowledgeNode, domain: &KnowledgeDomain) -> Vec<SelfQuestion> {
        let mut questions = Vec::new();
        
        questions.push(SelfQuestion {
            question: format!("What is {}?", node.topic),
            domain: domain.clone(),
            complexity_level: 3,
            expected_answer_type: QuestionType::Definition,
        });

        questions.push(SelfQuestion {
            question: format!("How does {} work?", node.topic),
            domain: domain.clone(),
            complexity_level: 5,
            expected_answer_type: QuestionType::Explanation,
        });

        questions.push(SelfQuestion {
            question: format!("How can I use {} in practice?", node.topic),
            domain: domain.clone(),
            complexity_level: 6,
            expected_answer_type: QuestionType::Application,
        });

        if !node.related_concepts.is_empty() {
            let related = &node.related_concepts[0];
            questions.push(SelfQuestion {
                question: format!("What is the difference between {} and {}?", node.topic, related),
                domain: domain.clone(),
                complexity_level: 7,
                expected_answer_type: QuestionType::Comparison,
            });
        }

        questions
    }

    async fn analyze_quality_patterns(&self) -> HashMap<String, f64> {
        let history = self.evaluation_history.read().unwrap();
        let mut improvements = HashMap::new();

        let mut topic_scores: HashMap<String, Vec<f64>> = HashMap::new();
        
        for record in history.iter().rev().take(100) {
            let topic = extract_main_topic(&record.question);
            topic_scores.entry(topic).or_insert_with(Vec::new).push(record.quality.overall_score);
        }

        for (topic, scores) in topic_scores {
            if scores.len() >= 3 {
                let recent_avg = scores.iter().take(3).sum::<f64>() / 3.0;
                let older_avg = scores.iter().skip(3).sum::<f64>() / (scores.len() - 3) as f64;
                
                if recent_avg > older_avg + 0.1 {
                    improvements.insert(topic, recent_avg - older_avg);
                }
            }
        }

        improvements
    }

    async fn get_domain_evaluation_counts(&self) -> HashMap<KnowledgeDomain, usize> {
        let history = self.evaluation_history.read().unwrap();
        let mut counts = HashMap::new();

        for record in history.iter() {
            let domain = self.infer_domain_from_question(&record.question);
            *counts.entry(domain).or_insert(0) += 1;
        }

        counts
    }

    fn infer_domain_from_question(&self, question: &str) -> KnowledgeDomain {
        let question_lower = question.to_lowercase();
        
        if question_lower.contains("computer") || question_lower.contains("software") || question_lower.contains("programming") {
            KnowledgeDomain::ComputerScience
        } else if question_lower.contains("quantum") || question_lower.contains("physics") || question_lower.contains("energy") {
            KnowledgeDomain::Physics
        } else if question_lower.contains("consciousness") || question_lower.contains("philosophy") || question_lower.contains("meaning") {
            KnowledgeDomain::Philosophy
        } else if question_lower.contains("biology") || question_lower.contains("life") || question_lower.contains("organism") {
            KnowledgeDomain::Biology
        } else if question_lower.contains("math") || question_lower.contains("number") || question_lower.contains("calculate") {
            KnowledgeDomain::Mathematics
        } else if question_lower.contains("astronomy") || question_lower.contains("space") || question_lower.contains("universe") {
            KnowledgeDomain::Astronomy
        } else {
            KnowledgeDomain::Philosophy
        }
    }

    /// Generate questions about the knowledge base (async version)
    async fn generate_comprehensive_questions(&self) {
        println!("❓ Generating self-evaluation questions...");
        
        let mut questions = Vec::new();
        
        // Generate questions for each domain
        for domain in KnowledgeDomain::all_domains() {
            // Get sample nodes from this domain
            let domain_nodes = self.knowledge_engine.query_by_domain(domain.clone());
            
            for node in domain_nodes.iter().take(3) { // 3 questions per domain for startup
                // Generate questions directly since we can't call the main impl methods
                questions.push(SelfQuestion {
                    question: format!("What is {}?", node.topic),
                    domain: domain.clone(),
                    complexity_level: 1,
                    expected_answer_type: QuestionType::Definition,
                });
                questions.push(SelfQuestion {
                    question: format!("How does {} work?", node.topic),
                    domain: domain.clone(),
                    complexity_level: 2,
                    expected_answer_type: QuestionType::Explanation,
                });
            }
        }

        // Add meta-questions about the system itself
        questions.push(SelfQuestion {
            question: "What is the purpose of this AI system?".to_string(),
            domain: KnowledgeDomain::Philosophy,
            complexity_level: 1,
            expected_answer_type: QuestionType::Definition,
        });
        questions.push(SelfQuestion {
            question: "What are the main capabilities of this knowledge system?".to_string(),
            domain: KnowledgeDomain::ComputerScience,
            complexity_level: 2,
            expected_answer_type: QuestionType::Explanation,
        });

        // Randomize and add to queue
        use std::collections::hash_map::DefaultHasher;
        use std::hash::{Hash, Hasher};
        
        let mut hasher = DefaultHasher::new();
        SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos().hash(&mut hasher);
        
        // Simple shuffle using seed
        questions.sort_by(|a, b| {
            let mut hasher = DefaultHasher::new();
            a.question.hash(&mut hasher);
            let a_hash = hasher.finish();
            let mut hasher = DefaultHasher::new();  
            b.question.hash(&mut hasher);
            let b_hash = hasher.finish();
            a_hash.cmp(&b_hash)
        });

        let mut queue = self.question_queue.write().unwrap();
        for question in questions {
            queue.push_back(question);
        }
        
        println!("📝 Generated {} self-evaluation questions", queue.len());
    }

    /// Generate the full comprehensive question set in background
    async fn generate_full_question_set(&self) {
        println!("🔄 Generating comprehensive question set in background...");
        
        let mut questions = Vec::new();
        
        // Generate questions for each domain (more comprehensive)
        for domain in KnowledgeDomain::all_domains() {
            let domain_nodes = self.knowledge_engine.query_by_domain(domain.clone());
            
            for node in domain_nodes.iter().take(2) { // 2 questions per domain for full set
                questions.extend(self.generate_questions_for_node(node, &domain));
            }
        }

        // Add meta-questions about the system itself
        questions.extend(self.generate_meta_questions());

        // Randomize and add to queue
        use std::collections::hash_map::DefaultHasher;
        use std::hash::{Hash, Hasher};
        
        let mut hasher = DefaultHasher::new();
        SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos().hash(&mut hasher);
        let _seed = hasher.finish();
        
        // Simple shuffle using seed
        questions.sort_by(|a, b| {
            let mut hasher = DefaultHasher::new();
            a.question.hash(&mut hasher);
            let a_hash = hasher.finish();
            let mut hasher = DefaultHasher::new();  
            b.question.hash(&mut hasher);
            let b_hash = hasher.finish();
            a_hash.cmp(&b_hash)
        });

        let mut queue = self.question_queue.write().unwrap();
        for question in questions {
            queue.push_back(question);
        }
        
        println!("📝 Generated {} total self-evaluation questions", queue.len());
    }

    fn generate_meta_questions(&self) -> Vec<SelfQuestion> {
        vec![
            SelfQuestion {
                question: "How many knowledge domains do I have?".to_string(),
                domain: KnowledgeDomain::Philosophy,
                complexity_level: 2,
                expected_answer_type: QuestionType::Definition,
            },
            SelfQuestion {
                question: "What is my primary function?".to_string(),
                domain: KnowledgeDomain::Philosophy,
                complexity_level: 2,
                expected_answer_type: QuestionType::Definition,
            },
            SelfQuestion {
                question: "How do I learn and improve?".to_string(),
                domain: KnowledgeDomain::Philosophy,
                complexity_level: 4,
                expected_answer_type: QuestionType::Explanation,
            },
        ]
    }

}

/// Statistics about the self-evaluation system
#[derive(Debug, Serialize, Deserialize)]
pub struct EvaluationStats {
    pub total_evaluations: usize,
    pub average_quality: f64,
    pub recent_quality: f64,
    pub improvement_areas: usize,
    pub is_running: bool,
}

/// Extract main topic from a question
fn extract_main_topic(question: &str) -> String {
    let question_lower = question.to_lowercase();
    
    // Remove question words
    let cleaned = question_lower
        .replace("what is ", "")
        .replace("how does ", "")
        .replace("how can i ", "")
        .replace("what are ", "")
        .replace("why does ", "")
        .replace("when does ", "")
        .replace("where does ", "")
        .replace("?", "");
    
    // Take first significant word(s)
    let words: Vec<&str> = cleaned.split_whitespace()
        .filter(|w| w.len() > 2 && !["the", "and", "but", "for", "with", "from", "use", "work", "make"].contains(w))
        .take(2)
        .collect();
    
    if words.is_empty() {
        "general".to_string()
    } else {
        words.join(" ")
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_extract_main_topic() {
        assert_eq!(extract_main_topic("What is quantum computing?"), "quantum computing");
        assert_eq!(extract_main_topic("How does machine learning work?"), "machine learning");
        assert_eq!(extract_main_topic("What are neural networks?"), "neural networks");
    }

    #[test]
    fn test_quality_scoring() {
        let engine = Arc::new(KnowledgeEngine::new());
        let response_gen = Arc::new(ComponentResponseGenerator::new(engine.clone()));
        let evaluator = SelfEvaluator::new(engine, response_gen);
        
        let question = SelfQuestion {
            question: "What is artificial intelligence?".to_string(),
            domain: KnowledgeDomain::ComputerScience,
            complexity_level: 5,
            expected_answer_type: QuestionType::Definition,
        };
        
        let good_answer = "Artificial intelligence is a branch of computer science that focuses on creating systems capable of performing tasks that typically require human intelligence, such as learning, reasoning, and problem-solving.";
        let quality = futures::executor::block_on(evaluator.evaluate_response_quality(&question, good_answer));
        
        assert!(quality.overall_score > 0.6);
        assert!(quality.relevance_score > 0.7);
    }
}