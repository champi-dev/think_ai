use axum::test_helpers::*;
use futures_util::{SinkExt, StreamExt};
use serde_json::{json, Value};
use think_ai_full::*;
use tokio::time::{sleep, Duration};

#[cfg(test)]
mod integration_tests {
    use super::*;

    #[tokio::test]
    async fn test_full_conversation_flow() {
        let client = TestClient::new(create_app()).await;
        let session_id = "integration-test-session";

        // Initial greeting
        let response = client
            .post("/api/chat")
            .json(&json!({
                "message": "Hello! My name is TestUser.",
                "session_id": session_id
            }))
            .send()
            .await;

        assert_eq!(response.status(), 200);
        let json: Value = response.json().await;
        assert!(
            json["response"].as_str().unwrap().contains("Hello")
                || json["response"].as_str().unwrap().contains("Hi")
        );

        // Follow-up question
        let response = client
            .post("/api/chat")
            .json(&json!({
                "message": "What's my name?",
                "session_id": session_id
            }))
            .send()
            .await;

        assert_eq!(response.status(), 200);
        let json: Value = response.json().await;
        assert!(json["response"].as_str().unwrap().contains("TestUser"));

        // Technical question
        let response = client
            .post("/api/chat")
            .json(&json!({
                "message": "Explain O(1) complexity",
                "session_id": session_id
            }))
            .send()
            .await;

        assert_eq!(response.status(), 200);
        let json: Value = response.json().await;
        assert!(json["response"].as_str().unwrap().contains("constant"));
    }

    #[tokio::test]
    async fn test_code_mode_conversation() {
        let client = TestClient::new(create_app()).await;
        let session_id = "code-mode-test";

        let response = client
            .post("/api/chat")
            .json(&json!({
                "message": "Write a fibonacci function in Python",
                "session_id": session_id,
                "mode": "code"
            }))
            .send()
            .await;

        assert_eq!(response.status(), 200);
        let json: Value = response.json().await;
        let response_text = json["response"].as_str().unwrap();

        assert!(response_text.contains("def") || response_text.contains("fibonacci"));
        assert!(response_text.contains("return"));
    }

    #[tokio::test]
    async fn test_streaming_endpoint() {
        let client = TestClient::new(create_app()).await;

        let mut stream = client
            .post("/api/chat/stream")
            .json(&json!({
                "message": "Count from 1 to 5",
                "session_id": "stream-test"
            }))
            .stream()
            .await;

        let mut chunks = Vec::new();
        let mut done = false;

        while let Some(chunk) = stream.next().await {
            let chunk = chunk.unwrap();
            let data = String::from_utf8(chunk.to_vec()).unwrap();

            if data.contains("done") {
                let json: Value = serde_json::from_str(&data).unwrap();
                if json["done"].as_bool().unwrap() {
                    done = true;
                    break;
                }
            }

            chunks.push(data);
        }

        assert!(done);
        assert!(!chunks.is_empty());
    }

    #[tokio::test]
    async fn test_websocket_connection() {
        let client = TestClient::new(create_app()).await;

        let ws = client.ws("/ws/chat").handshake().await.unwrap();

        let (mut tx, mut rx) = ws.split();

        // Send message
        tx.send(Message::Text(
            json!({
                "type": "message",
                "content": "Hello WebSocket!"
            })
            .to_string(),
        ))
        .await
        .unwrap();

        // Receive echo
        let msg = rx.next().await.unwrap().unwrap();
        assert!(matches!(msg, Message::Text(_)));

        // Close connection
        tx.close().await.unwrap();
    }

    #[tokio::test]
    async fn test_session_persistence() {
        let client = TestClient::new(create_app()).await;
        let session_id = "persistence-test";

        // Create messages
        for i in 0..5 {
            let response = client
                .post("/api/chat")
                .json(&json!({
                    "message": format!("Message {}", i),
                    "session_id": session_id
                }))
                .send()
                .await;

            assert_eq!(response.status(), 200);
        }

        // Retrieve session
        let response = client
            .get(&format!("/api/chat/sessions/{}", session_id))
            .send()
            .await;

        assert_eq!(response.status(), 200);
        let session: Value = response.json().await;

        assert_eq!(session["messages"].as_array().unwrap().len(), 10); // 5 user + 5 assistant
    }

    #[tokio::test]
    async fn test_knowledge_engine_integration() {
        let client = TestClient::new(create_app()).await;

        // Ask about something in the knowledge base
        let response = client
            .post("/api/chat")
            .json(&json!({
                "message": "What are O(1) algorithms?",
                "session_id": "knowledge-test"
            }))
            .send()
            .await;

        assert_eq!(response.status(), 200);
        let json: Value = response.json().await;

        // Should contain info from knowledge base
        assert!(json["response"].as_str().unwrap().contains("constant time"));
        assert!(json["response"].as_str().unwrap().contains("hash"));
    }

    #[tokio::test]
    async fn test_consciousness_metrics() {
        let client = TestClient::new(create_app()).await;

        // Multiple interactions to affect consciousness metrics
        for i in 0..3 {
            let response = client
                .post("/api/chat")
                .json(&json!({
                    "message": format!("Deep philosophical question {}", i),
                    "session_id": "consciousness-test"
                }))
                .send()
                .await;

            assert_eq!(response.status(), 200);
        }

        // Check consciousness level
        let response = client.get("/api/consciousness/level").send().await;

        assert_eq!(response.status(), 200);
        let level: Value = response.json().await;
        assert!(level["level"].is_string());

        // Check thoughts
        let response = client.get("/api/consciousness/thoughts").send().await;

        assert_eq!(response.status(), 200);
        let thoughts: Value = response.json().await;
        assert!(thoughts["thoughts"].is_array());
    }

    #[tokio::test]
    async fn test_search_functionality() {
        let client = TestClient::new(create_app()).await;

        // Test with web search enabled
        let response = client
            .post("/api/chat")
            .json(&json!({
                "message": "What's the weather today?",
                "session_id": "search-test",
                "use_web_search": true
            }))
            .send()
            .await;

        assert_eq!(response.status(), 200);
        let json: Value = response.json().await;
        assert!(json["response"].is_string());
    }

    #[tokio::test]
    async fn test_fact_checking() {
        let client = TestClient::new(create_app()).await;

        // Test fact checking
        let response = client
            .post("/api/chat")
            .json(&json!({
                "message": "The sun revolves around the earth",
                "session_id": "fact-check-test",
                "fact_check": true
            }))
            .send()
            .await;

        assert_eq!(response.status(), 200);
        let json: Value = response.json().await;
        let response_text = json["response"].as_str().unwrap().to_lowercase();

        assert!(
            response_text.contains("incorrect")
                || response_text.contains("false")
                || response_text.contains("earth revolves around the sun")
        );
    }

    #[tokio::test]
    async fn test_rate_limiting() {
        let client = TestClient::new(create_app()).await;
        let session_id = "rate-limit-test";

        // Send many requests rapidly
        let mut handles = vec![];
        for i in 0..20 {
            let client_clone = client.clone();
            let session_id_clone = session_id.to_string();

            let handle = tokio::spawn(async move {
                client_clone
                    .post("/api/chat")
                    .json(&json!({
                        "message": format!("Rapid message {}", i),
                        "session_id": session_id_clone
                    }))
                    .send()
                    .await
            });

            handles.push(handle);
        }

        // All should complete successfully (system should handle load)
        for handle in handles {
            let response = handle.await.unwrap();
            assert!(response.status() == 200 || response.status() == 429);
        }
    }

    #[tokio::test]
    async fn test_error_recovery() {
        let client = TestClient::new(create_app()).await;

        // Send malformed requests
        let response = client
            .post("/api/chat")
            .header("content-type", "application/json")
            .body("{invalid json}")
            .send()
            .await;

        assert_eq!(response.status(), 400);

        // System should still work after error
        let response = client
            .post("/api/chat")
            .json(&json!({
                "message": "Still working?",
                "session_id": "recovery-test"
            }))
            .send()
            .await;

        assert_eq!(response.status(), 200);
    }

    #[tokio::test]
    async fn test_long_conversation_context() {
        let client = TestClient::new(create_app()).await;
        let session_id = "long-context-test";

        // Build up conversation history
        let facts = vec![
            "My favorite color is blue",
            "I live in San Francisco",
            "I work as a software engineer",
            "I have a dog named Max",
            "I enjoy hiking on weekends",
        ];

        for fact in &facts {
            let response = client
                .post("/api/chat")
                .json(&json!({
                    "message": fact,
                    "session_id": session_id
                }))
                .send()
                .await;

            assert_eq!(response.status(), 200);
        }

        // Test recall
        let response = client
            .post("/api/chat")
            .json(&json!({
                "message": "What do you remember about me?",
                "session_id": session_id
            }))
            .send()
            .await;

        assert_eq!(response.status(), 200);
        let json: Value = response.json().await;
        let response_text = json["response"].as_str().unwrap().to_lowercase();

        // Should remember at least some facts
        let remembered_facts = facts
            .iter()
            .filter(|fact| response_text.contains(&fact.to_lowercase()))
            .count();

        assert!(remembered_facts >= 2);
    }

    #[tokio::test]
    async fn test_static_asset_caching() {
        let client = TestClient::new(create_app()).await;

        // First request
        let response1 = client.get("/").send().await;
        assert_eq!(response1.status(), 200);
        let etag1 = response1.headers().get("etag").cloned();

        // Second request with If-None-Match
        let mut request = client.get("/");
        if let Some(etag) = etag1 {
            request = request.header("if-none-match", etag);
        }

        let response2 = request.send().await;
        // Should be 200 (OK) since we don't implement caching in test
        assert!(response2.status() == 200 || response2.status() == 304);
    }

    #[tokio::test]
    async fn test_concurrent_different_sessions() {
        let client = TestClient::new(create_app()).await;

        let mut handles = vec![];

        for i in 0..5 {
            let client_clone = client.clone();

            let handle = tokio::spawn(async move {
                let session_id = format!("concurrent-session-{}", i);

                // Each session has different conversation
                for j in 0..3 {
                    let response = client_clone
                        .post("/api/chat")
                        .json(&json!({
                            "message": format!("Session {} Message {}", i, j),
                            "session_id": session_id
                        }))
                        .send()
                        .await;

                    assert_eq!(response.status(), 200);
                }

                // Verify session isolation
                let response = client_clone
                    .get(&format!("/api/chat/sessions/{}", session_id))
                    .send()
                    .await;

                assert_eq!(response.status(), 200);
                let session: Value = response.json().await;
                assert_eq!(session["messages"].as_array().unwrap().len(), 6);
            });

            handles.push(handle);
        }

        for handle in handles {
            handle.await.unwrap();
        }
    }

    #[tokio::test]
    async fn test_system_stats_accuracy() {
        let client = TestClient::new(create_app()).await;

        // Get initial stats
        let response = client.get("/api/knowledge/stats").send().await;
        assert_eq!(response.status(), 200);
        let initial_stats: Value = response.json().await;
        let initial_sessions = initial_stats["active_sessions"].as_u64().unwrap();

        // Create new sessions
        for i in 0..3 {
            client
                .post("/api/chat")
                .json(&json!({
                    "message": "New session",
                    "session_id": format!("stats-test-{}", i)
                }))
                .send()
                .await;
        }

        // Get updated stats
        let response = client.get("/api/knowledge/stats").send().await;
        assert_eq!(response.status(), 200);
        let updated_stats: Value = response.json().await;
        let updated_sessions = updated_stats["active_sessions"].as_u64().unwrap();

        assert_eq!(updated_sessions, initial_sessions + 3);
    }
}
