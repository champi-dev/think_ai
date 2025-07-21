use std::sync::Arc;
use tokio::sync::broadcast;
use serde::{Deserialize, Serialize};

use think_ai_consciousness::ConsciousnessFramework;
use think_ai_core::O1Engine;
use think_ai_knowledge::KnowledgeEngine;
use think_ai_qwen::QwenClient;
use think_ai_storage::PersistentConversationMemory;
use think_ai_vector::O1VectorIndex;

use crate::audio_service::AudioService;
use crate::notifications::whatsapp::WhatsAppNotifier;
use crate::metrics::MetricsCollector;

// State for the application
#[derive(Clone)]
pub struct ThinkAIState {
    pub _core_engine: Arc<O1Engine>,
    pub knowledge_engine: Arc<KnowledgeEngine>,
    pub _vector_index: Arc<O1VectorIndex>,
    pub _consciousness_framework: Arc<ConsciousnessFramework>,
    pub persistent_memory: Arc<PersistentConversationMemory>,
    pub message_channel: broadcast::Sender<ChatMessage>,
    pub qwen_client: Arc<QwenClient>,
    pub audio_service: Option<Arc<AudioService>>,
    pub whatsapp_notifier: Option<Arc<WhatsAppNotifier>>,
    pub metrics_collector: Arc<MetricsCollector>,
}

#[derive(Clone, Serialize, Deserialize)]
pub struct ChatMessage {
    pub id: String,
    pub session_id: String,
    pub message: String,
    pub response: Option<String>,
    pub timestamp: u64,
}