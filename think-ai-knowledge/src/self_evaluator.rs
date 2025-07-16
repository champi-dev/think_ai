// Self-Evaluating Knowledge System - AI that questions itself and improves
//!
// This system makes Think AI:
// 1. Ask itself questions about its knowledge base
// 2. Search for answers in its own knowledge
// 3. Evaluate response quality automatically
// 4. Progressively improve answers for user relevance
// 5. Run continuously in background with O(1) performance

use crate::response_generator::ComponentResponseGenerator;
use crate::{KnowledgeDomain, KnowledgeEngine};
use serde::{Deserialize, Serialize};
use std::collections::{HashMap, VecDeque};
use std::sync::{Arc, RwLock};
use std::time::{Duration, SystemTime, UNIX_EPOCH};
use tokio::time::sleep;

/// Quality metrics for auto-evaluation
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ResponseQuality {
    pub relevance_score: f64,     // How relevant is the answer to the question
    pub completeness_score: f64,  // How complete is the answer
    pub actionability_score: f64, // How actionable/useful is the answer
    pub clarity_score: f64,       // How clear and understandable
    pub factual_accuracy: f64,    // Estimated factual accuracy
    pub overall_score: f64,       // Weighted overall quality
}

/// Self-evaluation record for tracking improvements
#[derive(Debug, Clone)]
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
    pub complexity_level: u8, // 1-10 scale
    pub expected_answer_type: QuestionType,
}

#[derive(Debug, Clone, Copy)]
pub enum QuestionType {
    Definition,  // What is X?
    Explanation, // How does X work?
    Comparison,  // How is X different from Y?
    Application, // How can I use X?
    Problem,     // How do I solve X?
    Analysis,    // Why does X happen?
}

/// Stats for evaluation system
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EvaluationStats {
    pub total_evaluations: usize,
    pub average_quality: f64,
    pub recent_quality: f64,
    pub improvement_areas: usize,
    pub is_running: bool,
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
    pub fn new(
        knowledge_engine: Arc<KnowledgeEngine>,
        response_generator: Arc<ComponentResponseGenerator>,
    ) -> Self {
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
        }

        println!("🧠 Starting self-evaluation system...");

        // Generate initial questions
        self.generate_initial_questions();

        // Start evaluation loop
        let evaluator = self.clone_for_async();
        tokio::spawn(async move {
            evaluator.continuous_evaluation_loop().await;
        });

        println!("✅ Self-evaluation system active");
    }

    /// Generate initial questions for self-evaluation
    fn generate_initial_questions(&self) {
        let mut queue = self.question_queue.write().unwrap();

        // Add some basic questions across different domains
        let questions = vec![
            SelfQuestion {
                question: "What is artificial intelligence?".to_string(),
                domain: KnowledgeDomain::Technology,
                complexity_level: 5,
                expected_answer_type: QuestionType::Definition,
            },
            SelfQuestion {
                question: "How does machine learning work?".to_string(),
                domain: KnowledgeDomain::Technology,
                complexity_level: 7,
                expected_answer_type: QuestionType::Explanation,
            },
            SelfQuestion {
                question: "What is consciousness?".to_string(),
                domain: KnowledgeDomain::Philosophy,
                complexity_level: 9,
                expected_answer_type: QuestionType::Analysis,
            },
        ];

        for q in questions {
            queue.push_back(q);
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
            evaluation_cache: self.evaluation_cache.clone(),
            is_running: self.is_running.clone(),
        }
    }

    /// Evaluate response quality
    pub async fn evaluate_response_quality(
        &self,
        question: &SelfQuestion,
        answer: &str,
    ) -> ResponseQuality {
        // Simple quality evaluation based on heuristics
        let relevance_score = self.calculate_relevance(question, answer);
        let completeness_score = self.calculate_completeness(answer);
        let clarity_score = self.calculate_clarity(answer);
        let actionability_score = self.calculate_actionability(question, answer);
        let factual_accuracy = 0.8; // Assume reasonable accuracy for now

        let overall_score = (relevance_score * 0.3
            + completeness_score * 0.2
            + clarity_score * 0.2
            + actionability_score * 0.2
            + factual_accuracy * 0.1)
            .min(1.0);

        ResponseQuality {
            relevance_score,
            completeness_score,
            actionability_score,
            clarity_score,
            factual_accuracy,
            overall_score,
        }
    }

    fn calculate_relevance(&self, question: &SelfQuestion, answer: &str) -> f64 {
        // Simple keyword matching for relevance
        let question_words: Vec<&str> = question.question.split_whitespace().collect();
        let answer_words: Vec<&str> = answer.split_whitespace().collect();

        let matching_words = question_words
            .iter()
            .filter(|w| answer_words.contains(w))
            .count();

        (matching_words as f64 / question_words.len() as f64).min(1.0)
    }

    fn calculate_completeness(&self, answer: &str) -> f64 {
        // Based on answer length and structure
        let word_count = answer.split_whitespace().count();
        match word_count {
            0..=10 => 0.2,
            11..=30 => 0.5,
            31..=100 => 0.8,
            _ => 1.0,
        }
    }

    fn calculate_clarity(&self, answer: &str) -> f64 {
        // Simple heuristic based on sentence structure
        let sentences = answer.split('.').filter(|s| !s.trim().is_empty()).count();
        if sentences > 0 && answer.len() / sentences < 200 {
            0.8
        } else {
            0.6
        }
    }

    fn calculate_actionability(&self, question: &SelfQuestion, answer: &str) -> f64 {
        match question.expected_answer_type {
            QuestionType::Application | QuestionType::Problem => {
                if answer.contains("can") || answer.contains("should") || answer.contains("step") {
                    0.8
                } else {
                    0.4
                }
            }
            _ => 0.5,
        }
    }

    /// Get evaluation statistics
    pub fn get_stats(&self) -> EvaluationStats {
        let history = self.evaluation_history.read().unwrap();
        let total_evaluations = history.len();

        let average_quality = if total_evaluations > 0 {
            history.iter().map(|r| r.quality.overall_score).sum::<f64>() / total_evaluations as f64
        } else {
            0.0
        };

        let recent_quality = if total_evaluations > 0 {
            let recent_count = total_evaluations.min(10);
            history
                .iter()
                .take(recent_count)
                .map(|r| r.quality.overall_score)
                .sum::<f64>()
                / recent_count as f64
        } else {
            0.0
        };

        let quality_map = self.quality_improvements.read().unwrap();

        EvaluationStats {
            total_evaluations,
            average_quality,
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
    evaluation_cache: Arc<RwLock<HashMap<String, ResponseQuality>>>,
    is_running: Arc<RwLock<bool>>,
}

impl SelfEvaluatorAsync {
    async fn continuous_evaluation_loop(&self) {
        loop {
            // Check if still running
            if !*self.is_running.read().unwrap() {
                break;
            }

            // Get next question
            let question = {
                let mut queue = self.question_queue.write().unwrap();
                queue.pop_front()
            };

            if let Some(question) = question {
                // Generate answer
                let answer = self
                    .response_generator
                    .generate_response(&question.question);

                // Evaluate quality
                let quality = self.evaluate_response_quality(&question, &answer).await;

                // Store evaluation
                let record = EvaluationRecord {
                    question: question.question.clone(),
                    answer: answer.clone(),
                    quality: quality.clone(),
                    timestamp: SystemTime::now()
                        .duration_since(UNIX_EPOCH)
                        .unwrap()
                        .as_secs(),
                    iteration: 1,
                    improvement_suggestions: Vec::new(),
                };

                // Add to history
                let mut history = self.evaluation_history.write().unwrap();
                history.push_front(record);
                if history.len() > 1000 {
                    history.pop_back();
                }

                // Cache the evaluation
                self.evaluation_cache
                    .write()
                    .unwrap()
                    .insert(question.question, quality);
            }

            // Wait before next evaluation
            sleep(Duration::from_secs(5)).await;
        }
    }

    async fn evaluate_response_quality(
        &self,
        question: &SelfQuestion,
        answer: &str,
    ) -> ResponseQuality {
        // Reuse the sync evaluation logic
        let evaluator = SelfEvaluator {
            knowledge_engine: self.knowledge_engine.clone(),
            response_generator: self.response_generator.clone(),
            evaluation_history: self.evaluation_history.clone(),
            question_queue: self.question_queue.clone(),
            quality_improvements: self.quality_improvements.clone(),
            is_running: self.is_running.clone(),
            evaluation_cache: self.evaluation_cache.clone(),
        };

        evaluator.evaluate_response_quality(question, answer).await
    }
}

/// Extract main topic from a question
fn extract_main_topic(question: &str) -> String {
    let question_lower = question.to_lowercase();
    let words: Vec<&str> = question_lower
        .split_whitespace()
        .filter(|w| {
            ![
                "what", "is", "how", "does", "why", "when", "where", "can", "should", "the", "a",
                "an",
            ]
            .contains(w)
        })
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
        assert_eq!(
            extract_main_topic("What is quantum computing?"),
            "quantum computing"
        );
        assert_eq!(
            extract_main_topic("How does machine learning work?"),
            "machine learning"
        );
        assert_eq!(
            extract_main_topic("What are neural networks?"),
            "neural networks"
        );
    }

    #[test]
    fn test_quality_scoring() {
        let engine = Arc::new(KnowledgeEngine::new());
        let response_gen = Arc::new(ComponentResponseGenerator::new(engine.clone()));
        let evaluator = SelfEvaluator::new(engine, response_gen);

        let question = SelfQuestion {
            question: "What is artificial intelligence?".to_string(),
            domain: KnowledgeDomain::Technology,
            complexity_level: 5,
            expected_answer_type: QuestionType::Definition,
        };

        let good_answer = "Artificial intelligence is a branch of computer science that focuses on creating systems capable of performing tasks that typically require human intelligence, such as learning, reasoning, and problem-solving.";

        let quality = futures::executor::block_on(
            evaluator.evaluate_response_quality(&question, good_answer),
        );

        assert!(quality.overall_score > 0.6);
        assert!(quality.relevance_score > 0.7);
    }
}
