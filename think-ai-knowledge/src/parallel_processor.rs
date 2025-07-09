use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use std::thread::{self, JoinHandle};
use std::time::{Duration, SystemTime, UNIX_EPOCH};
use tokio::sync::mpsc;

use crate::shared_knowledge::{KnowledgeItem, SharedKnowledge};
use crate::types::{ProcessMessage, ProcessState, ProcessType};

/// Manages parallel cognitive processes that run independently
pub struct ParallelProcessor {
    /// Shared knowledge base that all processes contribute to
    shared_knowledge: Arc<SharedKnowledge>,
    /// Active processes and their handles
    processes: Arc<Mutex<HashMap<String, ProcessInfo>>>,
    /// Channel for inter-process communication
    message_channel: mpsc::Sender<ProcessMessage>,
    message_receiver: Arc<Mutex<mpsc::Receiver<ProcessMessage>>>,
    /// Global process configuration
    config: ProcessorConfig,
}

#[derive(Debug, Clone)]
struct ProcessInfo {
    process_type: ProcessType,
    state: ProcessState,
    handle: Option<Arc<JoinHandle<()>>>,
    started_at: u64,
    last_activity: u64,
    contributions: usize,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProcessorConfig {
    pub max_parallel_processes: usize,
    pub process_timeout: Duration,
    pub contribution_threshold: f32,
    pub memory_limit_mb: usize,
}

impl Default for ProcessorConfig {
    fn default() -> Self {
        Self {
            max_parallel_processes: 8,
            process_timeout: Duration::from_secs(300),
            contribution_threshold: 0.7,
            memory_limit_mb: 512,
        }
    }
}

impl ParallelProcessor {
    /// Create a new parallel processor
    pub fn new(shared_knowledge: Arc<SharedKnowledge>) -> Self {
        let (tx, rx) = mpsc::channel(1000);
        Self {
            shared_knowledge,
            processes: Arc::new(Mutex::new(HashMap::new())),
            message_channel: tx,
            message_receiver: Arc::new(Mutex::new(rx)),
            config: ProcessorConfig::default(),
        }
    }

    /// Start a new cognitive process
    pub async fn start_process(
        &self,
        process_type: ProcessType,
        context: Option<String>,
    ) -> Result<String, String> {
        // Check if we can start a new process
        let current_count = self.processes.lock().unwrap().len();
        if current_count >= self.config.max_parallel_processes {
            return Err("Maximum parallel processes reached".to_string());
        }

        let process_id = format!("{}_{}", process_type, uuid::Uuid::new_v4());
        let shared_knowledge = self.shared_knowledge.clone();
        let message_channel = self.message_channel.clone();
        let process_config = self.config.clone();

        // Create process info
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs();
        let process_info = ProcessInfo {
            process_type: process_type,
            state: ProcessState::Running,
            handle: None,
            started_at: now,
            last_activity: now,
            contributions: 0,
        };

        // Start the process in a new thread
        let process_id_clone = process_id.clone();
        let handle = match process_type {
            ProcessType::Knowledge => self.start_thinking_process(
                process_id_clone,
                shared_knowledge,
                message_channel,
                context,
            ),
            ProcessType::LLM => {
                self.start_dreaming_process(process_id_clone, shared_knowledge, message_channel)
            }
            ProcessType::Training => self.start_learning_process(
                process_id_clone,
                shared_knowledge,
                message_channel,
                context,
            ),
            ProcessType::Evaluation => {
                self.start_reflecting_process(process_id_clone, shared_knowledge, message_channel)
            }
        };

        // Store process info
        let mut process_info = process_info;
        process_info.handle = Some(Arc::new(handle));
        self.processes
            .lock()
            .unwrap()
            .insert(process_id.clone(), process_info);

        Ok(process_id)
    }

    /// Start a thinking process
    fn start_thinking_process(
        &self,
        process_id: String,
        shared_knowledge: Arc<SharedKnowledge>,
        message_channel: mpsc::Sender<ProcessMessage>,
        context: Option<String>,
    ) -> JoinHandle<()> {
        thread::spawn(move || {
            let runtime = tokio::runtime::Runtime::new().unwrap();
            runtime.block_on(async move {
                println!("Thinking process {process_id} started");

                // Thinking process: Analyze patterns and generate insights
                let mut cycle = 0;
                loop {
                    cycle += 1;

                    // Get recent knowledge items
                    let recent_items = shared_knowledge.get_recent_items(10).await;

                    // Analyze patterns
                    let patterns = Self::analyze_patterns(&recent_items);

                    // Generate insights
                    for pattern in patterns {
                        let insight = KnowledgeItem {
                            content: format!("Pattern detected: {pattern}"),
                            source: format!("thinking_process_{process_id}"),
                            confidence: 0.8,
                            metadata: HashMap::from([
                                ("process_type".to_string(), "thinking".to_string()),
                                ("cycle".to_string(), cycle.to_string()),
                            ]),
                        };
                        shared_knowledge.add_knowledge(insight).await.ok();
                    }

                    // Send status update
                    let _ = message_channel
                        .send(ProcessMessage {
                            process_type: ProcessType::Knowledge,
                            state: ProcessState::Running,
                            message: format!("Thinking cycle {cycle} completed"),
                            process_id: process_id.clone(),
                            message_type: "status_update".to_string(),
                        })
                        .await;

                    // Sleep before next cycle
                    tokio::time::sleep(Duration::from_secs(5)).await;
                    if cycle >= 100 {
                        break;
                    }
                }
            });
        })
    }

    /// Start a dreaming process
    fn start_dreaming_process(
        &self,
        process_id: String,
        shared_knowledge: Arc<SharedKnowledge>,
        message_channel: mpsc::Sender<ProcessMessage>,
    ) -> JoinHandle<()> {
        thread::spawn(move || {
            let runtime = tokio::runtime::Runtime::new().unwrap();
            runtime.block_on(async move {
                println!("Dreaming process {process_id} started");

                // Dreaming process: Creative recombination of knowledge
                let mut cycle = 0;
                loop {
                    cycle += 1;

                    // Get random knowledge items
                    let items = shared_knowledge.get_random_items(5).await;

                    // Create novel combinations
                    if items.len() >= 2 {
                        let combination = format!(
                            "What if {} and {} were connected?",
                            items[0].content, items[1].content
                        );

                        let dream_insight = KnowledgeItem {
                            content: combination,
                            source: format!("dreaming_process_{process_id}"),
                            confidence: 0.6,
                            metadata: HashMap::from([
                                ("process_type".to_string(), "dreaming".to_string()),
                                ("creativity_score".to_string(), "0.8".to_string()),
                            ]),
                        };
                        shared_knowledge.add_knowledge(dream_insight).await.ok();
                    }

                    // Send dream update
                    let _ = message_channel
                        .send(ProcessMessage {
                            process_type: ProcessType::Knowledge,
                            state: ProcessState::Running,
                            message: format!("Dream cycle {cycle} completed"),
                            process_id: process_id.clone(),
                            message_type: "dream_generated".to_string(),
                        })
                        .await;

                    // Sleep with varying intervals (mimicking REM cycles)
                    let sleep_duration = 3 + (cycle % 5);
                    tokio::time::sleep(Duration::from_secs(sleep_duration)).await;

                    if cycle >= 50 {
                        break;
                    }
                }
            });
        })
    }

    /// Start a learning process
    fn start_learning_process(
        &self,
        process_id: String,
        shared_knowledge: Arc<SharedKnowledge>,
        message_channel: mpsc::Sender<ProcessMessage>,
        context: Option<String>,
    ) -> JoinHandle<()> {
        thread::spawn(move || {
            let runtime = tokio::runtime::Runtime::new().unwrap();
            runtime.block_on(async move {
                println!("Learning process {process_id} started");

                // Learning process: Extract and reinforce patterns
                let mut learned_patterns: HashMap<String, f32> = HashMap::new();
                let mut cycle = 0;
                loop {
                    cycle += 1;

                    // Get knowledge items to learn from
                    let items = shared_knowledge.get_recent_items(20).await;

                    // Extract patterns and update weights
                    for item in items {
                        let words: Vec<&str> = item.content.split_whitespace().collect();
                        for window in words.windows(2) {
                            let pattern = format!("{} {}", window[0], window[1]);
                            *learned_patterns.entry(pattern).or_insert(0.0) += item.confidence;
                        }
                    }

                    // Store strong patterns as knowledge
                    for (pattern, weight) in learned_patterns.iter() {
                        if *weight > 5.0 {
                            let learning = KnowledgeItem {
                                content: format!("Learned pattern: {pattern}"),
                                source: format!("learning_process_{process_id}"),
                                confidence: (*weight / 10.0).min(1.0),
                                metadata: HashMap::from([
                                    ("process_type".to_string(), "learning".to_string()),
                                    ("weight".to_string(), weight.to_string()),
                                ]),
                            };
                            shared_knowledge.add_knowledge(learning).await.ok();
                        }
                    }

                    // Send learning update
                    let _ = message_channel
                        .send(ProcessMessage {
                            process_type: ProcessType::Training,
                            state: ProcessState::Running,
                            message: format!("Learned {} patterns", learned_patterns.len()),
                            process_id: process_id.clone(),
                            message_type: "learning_update".to_string(),
                        })
                        .await;

                    tokio::time::sleep(Duration::from_secs(10)).await;

                    if cycle >= 30 {
                        break;
                    }
                }
            });
        })
    }

    /// Start a reflecting process
    fn start_reflecting_process(
        &self,
        process_id: String,
        shared_knowledge: Arc<SharedKnowledge>,
        message_channel: mpsc::Sender<ProcessMessage>,
    ) -> JoinHandle<()> {
        thread::spawn(move || {
            let runtime = tokio::runtime::Runtime::new().unwrap();
            runtime.block_on(async move {
                println!("Reflecting process {process_id} started");

                // Reflecting process: Evaluate and consolidate knowledge
                let mut cycle = 0;
                loop {
                    cycle += 1;

                    // Get all knowledge statistics
                    let stats = shared_knowledge.get_statistics().await;

                    // Generate meta-insights about the knowledge base
                    let reflection = KnowledgeItem {
                        content: format!(
                            "Knowledge reflection: {} total items, average confidence {:.2}",
                            stats.total_items, stats.average_confidence
                        ),
                        source: format!("reflecting_process_{process_id}"),
                        confidence: 0.9,
                        metadata: HashMap::from([
                            ("process_type".to_string(), "reflecting".to_string()),
                            ("meta_level".to_string(), "2".to_string()),
                        ]),
                    };
                    shared_knowledge.add_knowledge(reflection).await.ok();

                    // Consolidate similar knowledge items
                    shared_knowledge.consolidate_knowledge().await;

                    // Send reflection update
                    let _ = message_channel
                        .send(ProcessMessage {
                            process_type: ProcessType::Evaluation,
                            state: ProcessState::Running,
                            message: format!("Reflection cycle {cycle} completed"),
                            process_id: process_id.clone(),
                            message_type: "reflection_complete".to_string(),
                        })
                        .await;

                    // Sleep for longer periods (reflection is less frequent)
                    tokio::time::sleep(Duration::from_secs(30)).await;

                    if cycle >= 20 {
                        break;
                    }
                }
            });
        })
    }

    /// Analyze patterns in knowledge items
    fn analyze_patterns(items: &[KnowledgeItem]) -> Vec<String> {
        let mut patterns = Vec::new();

        // Simple pattern detection based on common words
        let mut word_counts: HashMap<String, usize> = HashMap::new();
        for item in items {
            for word in item.content.split_whitespace() {
                if word.len() > 4 {
                    *word_counts.entry(word.to_string()).or_insert(0) += 1;
                }
            }
        }

        // Find frequently occurring words as patterns
        for (word, count) in word_counts {
            if count >= 3 {
                patterns.push(format!("Frequent concept: {word} ({count}x)"));
            }
        }

        patterns
    }

    /// Stop a specific process
    pub async fn stop_process(&self, process_id: &str) -> Result<(), String> {
        let mut processes = self.processes.lock().unwrap();
        if let Some(mut process_info) = processes.remove(process_id) {
            process_info.state = ProcessState::Stopped;
            Ok(())
        } else {
            Err("Process not found".to_string())
        }
    }

    /// Get status of all processes
    pub fn get_process_status(&self) -> Vec<ProcessStatus> {
        let processes = self.processes.lock().unwrap();
        processes
            .iter()
            .map(|(id, info)| ProcessStatus {
                process_id: id.clone(),
                process_type: info.process_type,
                state: info.state,
                uptime: SystemTime::now()
                    .duration_since(UNIX_EPOCH)
                    .unwrap()
                    .as_secs()
                    - info.started_at,
                contributions: info.contributions,
            })
            .collect()
    }

    /// Process messages from cognitive processes
    pub async fn process_messages(&self) -> Vec<ProcessMessage> {
        let mut messages = Vec::new();
        let mut receiver = self.message_receiver.lock().unwrap();

        // Collect all pending messages
        while let Ok(msg) = receiver.try_recv() {
            messages.push(msg);
        }

        messages
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProcessStatus {
    pub process_id: String,
    pub process_type: ProcessType,
    pub state: ProcessState,
    pub uptime: u64,
    pub contributions: usize,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_parallel_processor_creation() {
        let shared_knowledge = Arc::new(SharedKnowledge::new());
        let processor = ParallelProcessor::new(shared_knowledge);
        let status = processor.get_process_status();
        assert_eq!(status.len(), 0);
    }

    #[tokio::test]
    async fn test_start_thinking_process() {
        let shared_knowledge = Arc::new(SharedKnowledge::new());
        let processor = ParallelProcessor::new(shared_knowledge);

        let process_id = processor
            .start_process(ProcessType::Thinking, Some("test context".to_string()))
            .await
            .unwrap();

        assert!(!process_id.is_empty());

        let status = processor.get_process_status();
        assert_eq!(status.len(), 1);
        assert_eq!(status[0].process_type, ProcessType::Thinking);
    }

    #[tokio::test]
    async fn test_multiple_processes() {
        let shared_knowledge = Arc::new(SharedKnowledge::new());
        let processor = ParallelProcessor::new(shared_knowledge);

        // Start multiple processes
        let _thinking = processor
            .start_process(ProcessType::Thinking, None)
            .await
            .unwrap();

        let _dreaming = processor
            .start_process(ProcessType::Dreaming, None)
            .await
            .unwrap();

        let _learning = processor
            .start_process(ProcessType::Learning, None)
            .await
            .unwrap();

        let status = processor.get_process_status();
        assert_eq!(status.len(), 3);
    }
}