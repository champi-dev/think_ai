#!/bin/bash

echo "Adding persistent storage to Think AI server..."

# Create patch file
cat > /tmp/persistence.patch << 'EOF'
--- a/full-system/src/main.rs
+++ b/full-system/src/main.rs
@@ -13,6 +13,7 @@
     collections::HashMap,
     env,
     sync::{Arc, RwLock},
+    path::Path,
 };
 use tokio::sync::broadcast;
 use tower_http::{
@@ -29,6 +30,7 @@
 use think_ai_knowledge::{KnowledgeDomain, KnowledgeEngine, KnowledgeNode};
 use think_ai_qwen::{QwenClient, QwenRequest};
 use think_ai_vector::{LSHConfig, O1VectorIndex};
+use think_ai_storage::{PersistentConversationMemory, SledStorage};
 
 // State for the application
 #[derive(Clone)]
@@ -38,6 +40,7 @@ struct ThinkAIState {
     vector_index: Arc<O1VectorIndex>,
     consciousness_framework: Arc<ConsciousnessFramework>,
     chat_sessions: Arc<RwLock<HashMap<String, ChatSession>>>,
+    persistent_memory: Arc<PersistentConversationMemory>,
     message_channel: broadcast::Sender<ChatMessage>,
     qwen_client: Arc<QwenClient>,
 }
@@ -281,7 +284,20 @@ async fn chat_handler(
     // Get or create session
     let session_id = req.session_id.unwrap_or_else(|| Uuid::new_v4().to_string());
 
-    // Process with consciousness framework
+    // Check if user wants to delete history
+    let message_lower = req.message.to_lowercase();
+    if message_lower.contains("delete") && 
+       (message_lower.contains("chat history") || 
+        message_lower.contains("conversation history") || 
+        message_lower.contains("my history")) {
+        // Delete from persistent storage
+        let _ = state.persistent_memory.delete_session(&session_id).await;
+        return (StatusCode::OK, Json(ChatResponse {
+            response: "Your chat history has been deleted successfully. Starting fresh!".to_string(),
+            session_id: Uuid::new_v4().to_string(),
+            error: None,
+        }));
+    }
+
     // Note: ConsciousnessFramework doesn't have process_thought method
     let consciousness_state = serde_json::json!({
         "state": "aware",
@@ -289,28 +305,26 @@ async fn chat_handler(
     });
     
     // Get conversation history for context
-    let conversation_context = {
-        let sessions = state.chat_sessions.read().unwrap();
-        sessions.get(&session_id)
-            .map(|session| {
-                session.messages.iter()
-                    .map(|msg| format!("{}: {}", msg.role, msg.content))
-                    .collect::<Vec<_>>()
-                    .join("\n")
-            })
-            .unwrap_or_default()
-    };
+    let conversation_context = state.persistent_memory
+        .get_conversation_context(&session_id, 20)
+        .await
+        .map(|messages| {
+            messages.iter()
+                .map(|(role, content)| format!("{}: {}", role, content))
+                .collect::<Vec<_>>()
+                .join("\n")
+        })
+        .unwrap_or_default();
 
     // Generate response using knowledge engine
     let response = generate_ai_response(&req.message, &state, &conversation_context).await;
 
     let response_time_ms = start.elapsed().as_micros() as f64 / 1000.0;
 
-    // Store message
-    let user_msg = ChatMessage {
-        id: Uuid::new_v4().to_string(),
+    // Add to persistent memory
+    let _ = state.persistent_memory.add_message(
         session_id: session_id.clone(),
         role: "user".to_string(),
         content: req.message,
-        timestamp: chrono::Utc::now(),
-        response_time_ms: 0.0,
-    };
+    ).await;
 
-    let ai_msg = ChatMessage {
-        id: Uuid::new_v4().to_string(),
+    let _ = state.persistent_memory.add_message(
         session_id: session_id.clone(),
         role: "assistant".to_string(),
         content: response.clone(),
-        timestamp: chrono::Utc::now(),
-        response_time_ms,
-    };
-
-    // Update session
-    {
-        let mut sessions = state.chat_sessions.write().unwrap();
-        let session = sessions.entry(session_id.clone()).or_insert(ChatSession {
-            id: session_id.clone(),
-            messages: Vec::new(),
-            created_at: chrono::Utc::now(),
-        });
-        session.messages.push(user_msg.clone());
-        session.messages.push(ai_msg.clone());
-    }
+    ).await;
 
     // Broadcast message
-    let _ = state.message_channel.send(ai_msg);
+    let _ = state.message_channel.send(ChatMessage {
+        id: Uuid::new_v4().to_string(),
+        session_id: session_id.clone(),
+        role: "assistant".to_string(),
+        content: response.clone(),
+        timestamp: chrono::Utc::now(),
+        response_time_ms,
+    });
 
     (
         StatusCode::OK,
@@ -509,6 +515,14 @@ async fn main() {
     let consciousness_framework = Arc::new(ConsciousnessFramework::new());
 
     // Initialize Qwen client
     let qwen_client = Arc::new(QwenClient::new());
+    
+    // Initialize persistent memory
+    let db_path = env::var("THINK_AI_DB_PATH").unwrap_or_else(|_| "./think_ai_sessions.db".to_string());
+    let persistent_memory = Arc::new(
+        PersistentConversationMemory::new(&db_path)
+            .await
+            .expect("Failed to initialize persistent memory")
+    );
 
     // Create shared state
     let (tx, _rx) = broadcast::channel(100);
@@ -518,6 +532,7 @@ async fn main() {
         vector_index,
         consciousness_framework,
         chat_sessions: Arc::new(RwLock::new(HashMap::new())),
+        persistent_memory,
         message_channel: tx,
         qwen_client,
     };
EOF

echo "Patch file created. The changes will:"
echo "1. Add persistent storage using SledDB"
echo "2. Store all conversations permanently"
echo "3. Support 'delete chat history' command"
echo "4. Sessions persist across server restarts"
echo ""
echo "To apply: cd /home/administrator/think_ai && patch -p1 < /tmp/persistence.patch"