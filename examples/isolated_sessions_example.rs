use std::sync::Arc;
use think_ai_knowledge::{
    isolated_session::IsolatedSession,
    parallel_processor::{ParallelProcessor, ProcessType},
    shared_knowledge::SharedKnowledge,
    types::Message,
};

/// Example showing how to integrate the new isolated sessions architecture
/// into your Think AI application
pub struct IsolatedSessionsExample;
impl IsolatedSessionsExample {
    /// Initialize the system with shared knowledge and background processes
    pub async fn initialize() -> (Arc<SharedKnowledge>, Arc<ParallelProcessor>) {
        // Create the shared knowledge base
        let shared_knowledge = Arc::new(SharedKnowledge::new());
        // Create the parallel processor for background tasks
        let processor = Arc::new(ParallelProcessor::new(shared_knowledge.clone()));
        // Start background cognitive processes
        let _ = processor.start_process(ProcessType::Thinking, None).await;
        let _ = processor.start_process(ProcessType::Learning, None).await;
        let _ = processor.start_process(ProcessType::Dreaming, None).await;
        let _ = processor.start_process(ProcessType::Reflecting, None).await;
        println!("✅ Initialized isolated sessions architecture");
        (shared_knowledge, processor)
    }
    /// Create a new chat session for a user
    pub fn create_user_session(shared_knowledge: Arc<SharedKnowledge>) -> IsolatedSession {
        let session = IsolatedSession::new(shared_knowledge);
        println!("📱 Created new session: {}", session.session_id);
        session
    /// Process a user message in their isolated session
    pub async fn process_user_message(
        session: &mut IsolatedSession,
        content: String,
    ) -> Result<String, String> {
        let message = Message {
            role: "user".to_string(),
            content,
            timestamp: std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_secs(),
        };
        let response = session.process_message(message).await?;
        Ok(response.content)
    /// Example HTTP handler for chat endpoints
    pub async fn chat_handler(
        shared_knowledge: Arc<SharedKnowledge>,
        session_id: Option<String>,
        message: String,
    ) -> Result<(String, String), String> {
        // Load or create session
        let mut session = if let Some(id) = session_id {
            // In production, you'd load this from a session store
            println!("Loading existing session: {}", id);
            IsolatedSession::new(shared_knowledge)
        } else {
            Self::create_user_session(shared_knowledge)
        // Process the message
        let response = Self::process_user_message(&mut session, message).await?;
        // Return session ID and response
        Ok((session.session_id.clone(), response))
}
/// Example integration with the existing Think AI HTTP server
pub mod integration {
    use super::*;
    use std::sync::Arc;
    pub struct SessionManager {
        processor: Arc<ParallelProcessor>,
        // In production, add a session store here
    impl SessionManager {
        pub async fn new() -> Self {
            let (shared_knowledge, processor) = IsolatedSessionsExample::initialize().await;
            Self {
                shared_knowledge,
                processor,
            }
        }
        /// Handle a chat request
        pub async fn handle_chat(
            &self,
            session_id: Option<String>,
            message: String,
        ) -> Result<serde_json::Value, String> {
            let (session_id, response) = IsolatedSessionsExample::chat_handler(
                self.shared_knowledge.clone(),
                session_id,
                message,
            ).await?;
            Ok(serde_json::json!({
                "session_id": session_id,
                "response": response,
                "timestamp": std::time::SystemTime::now()
                    .duration_since(std::time::UNIX_EPOCH)
                    .unwrap()
                    .as_secs(),
            }))
        /// Get system status
        pub async fn get_status(&self) -> serde_json::Value {
            let process_status = self.processor.get_process_status();
            let knowledge_stats = self.shared_knowledge.get_statistics().await;
            serde_json::json!({
                "processes": process_status.len(),
                "knowledge_items": knowledge_stats.total_items,
                "average_confidence": knowledge_stats.average_confidence,
                "sources": knowledge_stats.total_sources,
            })
#[cfg(test)]
mod tests {
    #[tokio::test]
    async fn test_isolated_sessions_example() {
        // Initialize system
        let (shared_knowledge, _processor) = IsolatedSessionsExample::initialize().await;
        // Create a session
        let mut session = IsolatedSessionsExample::create_user_session(shared_knowledge);
        // Process a message
        let response = IsolatedSessionsExample::process_user_message(
            &mut session,
            "Hello, how are you?".to_string(),
        ).await.unwrap();
        assert!(!response.is_empty());
        assert_eq!(session.context.messages.len(), 2); // User message + response
    async fn test_session_manager() {
        let manager = integration::SessionManager::new().await;
        // First message (creates new session)
        let result1 = manager.handle_chat(
            None,
            "What is Rust?".to_string(),
        let session_id = result1["session_id"].as_str().unwrap();
        assert!(!session_id.is_empty());
        // Second message (uses existing session)
        let result2 = manager.handle_chat(
            Some(session_id.to_string()),
            "Tell me more".to_string(),
        assert_eq!(result2["session_id"], session_id);
