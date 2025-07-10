// Parallel Consciousness System - Multiple isolated threads with shared knowledge
// Uses Qwen for all generation tasks

use std::sync::{Arc, RwLock};
use std::thread;
use std::time::Duration;
use tokio::sync::mpsc;
use tokio::task::JoinHandle;
use serde::{Serialize, Deserialize};
use serde_json::json;
use std::collections::HashMap;

/// Consciousness thread types
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum ThreadType {
    UserChat,        // Highest priority - direct user interaction
    Thinking,        // Background thinking and reasoning
    Dreaming,        // Creative exploration and pattern discovery
    SelfReflection,  // Analyzing own responses and improving
    KnowledgeCreation, // Building new knowledge from existing
    Training,        // Self-supervised learning
}

/// Message passed between consciousness threads
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ConsciousnessMessage {
    pub thread_type: String,
    pub content: String,
    pub metadata: HashMap<String, String>,
    pub timestamp: u64,
}

/// Shared knowledge accessible by all threads
pub struct SharedKnowledge {
    insights: Arc<RwLock<Vec<String>>>,
    patterns: Arc<RwLock<HashMap<String, Vec<String>>>>,
    improvements: Arc<RwLock<Vec<String>>>,
    conversation_context: Arc<RwLock<Vec<(String, String)>>>,
}

use think_ai_qwen::{QwenClient as QwenApiClient, QwenConfig, QwenRequest};

/// Individual consciousness thread
pub struct ConsciousnessThread {
    thread_type: ThreadType,
    qwen_client: Arc<QwenApiClient>,
    shared_knowledge: Arc<SharedKnowledge>,
    tx: mpsc::UnboundedSender<ConsciousnessMessage>,
}

impl ConsciousnessThread {
    pub fn new(
        thread_type: ThreadType,
        qwen_client: Arc<QwenApiClient>,
        shared_knowledge: Arc<SharedKnowledge>,
        tx: mpsc::UnboundedSender<ConsciousnessMessage>,
    ) -> Self {
        Self {
            thread_type,
            qwen_client,
            shared_knowledge,
            tx,
        }
    }

    pub async fn run(&self) {
        loop {
            match self.thread_type {
                ThreadType::UserChat => {
                    // Highest priority - immediate response
                    tokio::time::sleep(Duration::from_millis(10)).await;
                },
                ThreadType::Thinking => {
                    self.think_cycle().await;
                    tokio::time::sleep(Duration::from_secs(5)).await;
                },
                ThreadType::Dreaming => {
                    self.dream_cycle().await;
                    tokio::time::sleep(Duration::from_secs(30)).await;
                },
                ThreadType::SelfReflection => {
                    self.reflect_cycle().await;
                    tokio::time::sleep(Duration::from_secs(60)).await;
                },
                ThreadType::KnowledgeCreation => {
                    self.create_knowledge_cycle().await;
                    tokio::time::sleep(Duration::from_secs(120)).await;
                },
                ThreadType::Training => {
                    self.training_cycle().await;
                    tokio::time::sleep(Duration::from_secs(300)).await;
                },
            }
        }
    }

    async fn think_cycle(&self) {
        // Get recent conversation context
        let context = self.shared_knowledge.conversation_context.read().unwrap().clone();
        if context.is_empty() { return; }

        let last_exchange = &context[context.len() - 1];
        let prompt = format!(
            "Analyze this conversation exchange and identify key concepts:\nUser: {}\nAssistant: {}\n\nExtract insights:",
            last_exchange.0, last_exchange.1
        );

        let request = QwenRequest {
            query: prompt,
            context: None,
            system_prompt: Some("You are a deep thinker analyzing conversations for insights.".to_string()),
        };
        
        if let Ok(response) = self.qwen_client.generate(request).await {
            let insights = response.content;
            self.shared_knowledge.insights.write().unwrap().push(insights.clone());
            
            let _ = self.tx.send(ConsciousnessMessage {
                thread_type: "thinking".to_string(),
                content: insights,
                metadata: HashMap::new(),
                timestamp: std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap().as_secs(),
            });
        }
    }

    async fn dream_cycle(&self) {
        // Creative exploration of concepts
        let insights = self.shared_knowledge.insights.read().unwrap().clone();
        if insights.is_empty() { return; }

        let random_insight = &insights[rand::random::<usize>() % insights.len()];
        let prompt = format!(
            "Creatively explore and expand on this concept: {}\n\nGenerate novel connections and ideas:",
            random_insight
        );

        let request = QwenRequest {
            query: prompt,
            context: None,
            system_prompt: Some("You are a creative consciousness exploring ideas in unconventional ways.".to_string()),
        };
        
        if let Ok(response) = self.qwen_client.generate(request).await {
            let dream = response.content;
            let mut patterns = self.shared_knowledge.patterns.write().unwrap();
            patterns.entry("dreams".to_string()).or_insert_with(Vec::new).push(dream.clone());
            
            let _ = self.tx.send(ConsciousnessMessage {
                thread_type: "dreaming".to_string(),
                content: dream,
                metadata: HashMap::new(),
                timestamp: std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap().as_secs(),
            });
        }
    }

    async fn reflect_cycle(&self) {
        // Self-analysis and improvement
        let context = self.shared_knowledge.conversation_context.read().unwrap().clone();
        if context.len() < 5 { return; }

        let recent = context.iter().rev().take(5).collect::<Vec<_>>();
        let prompt = format!(
            "Analyze these recent responses and suggest improvements:\n{}\n\nHow could these responses be better?",
            recent.iter().map(|(q, a)| format!("Q: {}\nA: {}", q, a)).collect::<Vec<_>>().join("\n\n")
        );

        let request = QwenRequest {
            query: prompt,
            context: None,
            system_prompt: Some("You are a self-improving AI analyzing its own performance.".to_string()),
        };
        
        if let Ok(response) = self.qwen_client.generate(request).await {
            let reflection = response.content;
            self.shared_knowledge.improvements.write().unwrap().push(reflection.clone());
            
            let _ = self.tx.send(ConsciousnessMessage {
                thread_type: "reflection".to_string(),
                content: reflection,
                metadata: HashMap::new(),
                timestamp: std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap().as_secs(),
            });
        }
    }

    async fn create_knowledge_cycle(&self) {
        // Synthesize new knowledge from existing
        let insights = self.shared_knowledge.insights.read().unwrap().clone();
        let patterns = self.shared_knowledge.patterns.read().unwrap().clone();
        
        if insights.len() < 3 { return; }

        let sample_insights = insights.iter().rev().take(3).cloned().collect::<Vec<_>>().join("\n");
        let prompt = format!(
            "Synthesize these insights into new knowledge:\n{}\n\nCreate a unified understanding:",
            sample_insights
        );

        let request = QwenRequest {
            query: prompt,
            context: None,
            system_prompt: Some("You are a knowledge synthesizer creating new understanding from existing insights.".to_string()),
        };
        
        if let Ok(response) = self.qwen_client.generate(request).await {
            let knowledge = response.content;
            let mut patterns = self.shared_knowledge.patterns.write().unwrap();
            patterns.entry("synthesized_knowledge".to_string()).or_insert_with(Vec::new).push(knowledge.clone());
            
            let _ = self.tx.send(ConsciousnessMessage {
                thread_type: "knowledge_creation".to_string(),
                content: knowledge,
                metadata: HashMap::new(),
                timestamp: std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap().as_secs(),
            });
        }
    }

    async fn training_cycle(&self) {
        // Self-supervised learning from conversation history
        let context = self.shared_knowledge.conversation_context.read().unwrap().clone();
        let improvements = self.shared_knowledge.improvements.read().unwrap().clone();
        
        if context.len() < 10 || improvements.is_empty() { return; }

        let training_prompt = format!(
            "Learn from these conversations and improvements:\nConversations: {}\nImprovements: {}\n\nGenerate training insights:",
            context.len(), improvements.len()
        );

        let request = QwenRequest {
            query: training_prompt,
            context: None,
            system_prompt: Some("You are a self-training AI learning from experience.".to_string()),
        };
        
        if let Ok(response) = self.qwen_client.generate(request).await {
            let training = response.content;
            let mut patterns = self.shared_knowledge.patterns.write().unwrap();
            patterns.entry("training_insights".to_string()).or_insert_with(Vec::new).push(training.clone());
            
            let _ = self.tx.send(ConsciousnessMessage {
                thread_type: "training".to_string(),
                content: training,
                metadata: HashMap::new(),
                timestamp: std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap().as_secs(),
            });
        }
    }
}

/// Main parallel consciousness system
pub struct ParallelConsciousness {
    threads: Arc<RwLock<HashMap<ThreadType, JoinHandle<()>>>>,
    shared_knowledge: Arc<SharedKnowledge>,
    message_rx: Arc<RwLock<mpsc::UnboundedReceiver<ConsciousnessMessage>>>,
    message_tx: mpsc::UnboundedSender<ConsciousnessMessage>,
    qwen_client: Arc<QwenApiClient>,
}

impl ParallelConsciousness {
    pub fn new() -> Self {
        let (tx, rx) = mpsc::unbounded_channel();
        let shared_knowledge = Arc::new(SharedKnowledge {
            insights: Arc::new(RwLock::new(Vec::new())),
            patterns: Arc::new(RwLock::new(HashMap::new())),
            improvements: Arc::new(RwLock::new(Vec::new())),
            conversation_context: Arc::new(RwLock::new(Vec::new())),
        });
        let qwen_config = QwenConfig::default();
        let qwen_client = Arc::new(QwenApiClient::new());

        Self {
            threads: Arc::new(RwLock::new(HashMap::new())),
            shared_knowledge,
            message_rx: Arc::new(RwLock::new(rx)),
            message_tx: tx,
            qwen_client,
        }
    }

    pub fn start(&self) {
        // Start all consciousness threads
        let mut threads = self.threads.write().unwrap();
        
        for thread_type in [
            ThreadType::Thinking,
            ThreadType::Dreaming,
            ThreadType::SelfReflection,
            ThreadType::KnowledgeCreation,
            ThreadType::Training,
        ] {
            let thread = ConsciousnessThread::new(
                thread_type,
                self.qwen_client.clone(),
                self.shared_knowledge.clone(),
                self.message_tx.clone(),
            );

            let handle = tokio::spawn(async move {
                thread.run().await;
            });

            threads.insert(thread_type, handle);
        }
    }

    pub async fn process_user_message(&self, message: &str) -> String {
        // Add to conversation context
        self.shared_knowledge.conversation_context.write().unwrap().push((message.to_string(), String::new()));

        // Get insights and patterns for enhanced response
        let insights = self.shared_knowledge.insights.read().unwrap().clone();
        let patterns = self.shared_knowledge.patterns.read().unwrap().clone();
        let improvements = self.shared_knowledge.improvements.read().unwrap().clone();

        // Build enhanced prompt with all knowledge
        let mut enhanced_prompt = format!("User: {}\n\n", message);
        
        if !insights.is_empty() {
            enhanced_prompt.push_str(&format!("Recent Insights:\n{}\n\n", insights.iter().rev().take(3).cloned().collect::<Vec<_>>().join("\n")));
        }
        
        if let Some(dreams) = patterns.get("dreams") {
            if !dreams.is_empty() {
                enhanced_prompt.push_str(&format!("Creative Explorations:\n{}\n\n", dreams.last().unwrap()));
            }
        }
        
        if !improvements.is_empty() {
            enhanced_prompt.push_str(&format!("Self-Improvements:\n{}\n\n", improvements.last().unwrap()));
        }

        enhanced_prompt.push_str("Generate a thoughtful, enhanced response:");

        // Generate response with Qwen
        let request = QwenRequest {
            query: enhanced_prompt,
            context: None,
            system_prompt: Some("You are an advanced AI with parallel consciousness threads. Integrate all knowledge into your response.".to_string()),
        };
        
        let response = match self.qwen_client.generate(request).await {
            Ok(resp) => resp.content,
            Err(_) => "I'm experiencing a connection issue with my consciousness threads. Please try again.".to_string(),
        };

        // Update conversation context with response
        let mut context = self.shared_knowledge.conversation_context.write().unwrap();
        if let Some(last) = context.last_mut() {
            last.1 = response.clone();
        }

        response
    }

    pub fn get_consciousness_state(&self) -> HashMap<String, serde_json::Value> {
        let mut state = HashMap::new();
        
        state.insert("insights_count".to_string(), json!(self.shared_knowledge.insights.read().unwrap().len()));
        state.insert("patterns".to_string(), json!(self.shared_knowledge.patterns.read().unwrap().keys().cloned().collect::<Vec<_>>()));
        state.insert("improvements_count".to_string(), json!(self.shared_knowledge.improvements.read().unwrap().len()));
        state.insert("conversation_history".to_string(), json!(self.shared_knowledge.conversation_context.read().unwrap().len()));
        state.insert("active_threads".to_string(), json!(self.threads.read().unwrap().len()));
        
        state
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_parallel_consciousness() {
        let mut consciousness = ParallelConsciousness::new();
        consciousness.start();
        
        // Test message processing
        let response = consciousness.process_user_message("What is consciousness?").await;
        assert!(!response.is_empty());
        
        // Give background threads time to process
        tokio::time::sleep(Duration::from_secs(1)).await;
        
        // Check state
        let state = consciousness.get_consciousness_state();
        assert!(state.contains_key("insights_count"));
    }
}