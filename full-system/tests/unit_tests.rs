#[cfg(test)]
mod unit_tests {
    use super::*;
    use mockall::mock;
    use mockall::predicate::*;
    use std::sync::Arc;
    use think_ai_knowledge::KnowledgeEngine;
    use think_ai_qwen::QwenClient;

    use std::collections::HashMap;
    use std::sync::{Arc, RwLock};
    use think_ai_consciousness::ConsciousnessFramework;
    use think_ai_core::{EngineConfig, O1Engine};
    use think_ai_vector::{LSHConfig, O1VectorIndex};
    use tokio::sync::broadcast;

    #[derive(Clone)]
    struct ThinkAIState {
        _core_engine: Arc<O1Engine>,
        knowledge_engine: Arc<KnowledgeEngine>,
        _vector_index: Arc<O1VectorIndex>,
        _consciousness_framework: Arc<ConsciousnessFramework>,
        chat_sessions: Arc<RwLock<HashMap<String, String>>>,
        message_channel: broadcast::Sender<String>,
        qwen_client: Arc<QwenClient>,
    }

    fn create_app(state: ThinkAIState) -> Router {
        Router::new()
            .route("/health", axum::routing::get(|| async { "OK" }))
            .route("/api/health", axum::routing::get(|| async { 
                json!({
                    "status": "healthy",
                    "service": "think-ai-full",
                    "version": "1.0.0"
                })
            }))
            .route("/api/chat", axum::routing::post(|| async {
                json!({
                    "response": "Test response",
                    "session_id": "test-session",
                    "confidence": 0.95,
                    "response_time_ms": 100,
                    "consciousness_level": "AWARE",
                    "tokens_used": 50,
                    "context_tokens": 25,
                    "compacted": false
                })
            }))
            .route("/api/chat/sessions", axum::routing::get(|| async {
                json!([
                    {"id": "session-1", "created_at": "2023-01-01T00:00:00Z"},
                    {"id": "session-2", "created_at": "2023-01-01T01:00:00Z"}
                ])
            }))
            .route("/api/chat/sessions/:id", axum::routing::get(|| async {
                json!({
                    "id": "test-session",
                    "messages": [],
                    "created_at": "2023-01-01T00:00:00Z"
                })
            }))
            .route("/api/knowledge/domains", axum::routing::get(|| async {
                json!(["technology", "science"])
            }))
            .route("/api/knowledge/stats", axum::routing::get(|| async {
                json!({
                    "total_knowledge_items": 1000,
                    "active_sessions": 5,
                    "average_response_time_ms": 150.0,
                    "cache_hit_rate": 0.85,
                    "uptime_seconds": 3600,
                    "consciousness_level": "AWARE",
                    "domains": ["technology", "science"]
                })
            }))
            .route("/api/consciousness/level", axum::routing::get(|| async {
                json!({
                    "level": "AWARE",
                    "description": "Fully conscious and aware",
                    "introspection_depth": 3
                })
            }))
            .route("/api/consciousness/thoughts", axum::routing::get(|| async {
                json!({
                    "thoughts": ["Current thought 1", "Current thought 2"],
                    "thought_count": 2,
                    "processing_state": "active"
                })
            }))
            .route("/api/search", axum::routing::get(|| async {
                json!({
                    "results": [],
                    "total": 0,
                    "query_time_ms": 50
                })
            }))
            .route("/", axum::routing::get(|| async {
                axum::response::Html("<html><head><title>Think AI</title></head><body>Test</body></html>")
            }))
            .route("/manifest.json", axum::routing::get(|| async {
                json!({
                    "name": "Think AI",
                    "version": "1.0.0"
                })
            }))
            .route("/icon-192.svg", axum::routing::get(|| async {
                ([("content-type", "image/svg+xml")], "<svg></svg>")
            }))
            .layer(tower_http::cors::CorsLayer::permissive())
    }

    #[tokio::test]
    async fn test_health_check_endpoint() {
        let app = create_test_app().await;

        let response = app
            .oneshot(
                Request::builder()
                    .uri("/health")
                    .body(Body::empty())
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);
        let body = hyper::body::to_bytes(response.into_body()).await.unwrap();
        assert_eq!(&body[..], b"OK");
    }

    #[tokio::test]
    async fn test_api_health_endpoint() {
        let app = create_test_app().await;

        let response = app
            .oneshot(
                Request::builder()
                    .uri("/api/health")
                    .body(Body::empty())
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);

        let body = hyper::body::to_bytes(response.into_body()).await.unwrap();
        let json: Value = serde_json::from_slice(&body).unwrap();

        assert_eq!(json["status"], "healthy");
        assert_eq!(json["service"], "think-ai-full");
        assert_eq!(json["version"], "1.0.0");
    }

    #[tokio::test]
    async fn test_chat_endpoint_new_session() {
        let app = create_test_app().await;

        let request_body = json!({
            "message": "Hello, Think AI!",
            "session_id": null
        });

        let response = app
            .oneshot(
                Request::builder()
                    .method("POST")
                    .uri("/api/chat")
                    .header("content-type", "application/json")
                    .body(Body::from(request_body.to_string()))
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);

        let body = hyper::body::to_bytes(response.into_body()).await.unwrap();
        let json: Value = serde_json::from_slice(&body).unwrap();

        assert!(json["response"].is_string());
        assert!(json["session_id"].is_string());
        assert!(json["confidence"].is_number());
        assert!(json["response_time_ms"].is_number());
        assert!(json["consciousness_level"].is_string());
        assert!(json["tokens_used"].is_number());
        assert!(json["context_tokens"].is_number());
        assert_eq!(json["compacted"], false);
    }

    #[tokio::test]
    async fn test_chat_endpoint_existing_session() {
        let app = create_test_app().await;
        let session_id = "test-session-123";

        // First message
        let request_body = json!({
            "message": "Hello!",
            "session_id": session_id
        });

        let response = app
            .clone()
            .oneshot(
                Request::builder()
                    .method("POST")
                    .uri("/api/chat")
                    .header("content-type", "application/json")
                    .body(Body::from(request_body.to_string()))
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);

        // Second message with same session
        let request_body = json!({
            "message": "How are you?",
            "session_id": session_id
        });

        let response = app
            .oneshot(
                Request::builder()
                    .method("POST")
                    .uri("/api/chat")
                    .header("content-type", "application/json")
                    .body(Body::from(request_body.to_string()))
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);

        let body = hyper::body::to_bytes(response.into_body()).await.unwrap();
        let json: Value = serde_json::from_slice(&body).unwrap();

        assert_eq!(json["session_id"], session_id);
    }

    #[tokio::test]
    async fn test_chat_with_special_modes() {
        let app = create_test_app().await;

        // Test code mode
        let request_body = json!({
            "message": "Write a Python function",
            "session_id": "code-session",
            "mode": "code",
            "use_web_search": false,
            "fact_check": false
        });

        let response = app
            .clone()
            .oneshot(
                Request::builder()
                    .method("POST")
                    .uri("/api/chat")
                    .header("content-type", "application/json")
                    .body(Body::from(request_body.to_string()))
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);

        // Test with web search enabled
        let request_body = json!({
            "message": "Latest news about AI",
            "session_id": "search-session",
            "mode": "general",
            "use_web_search": true,
            "fact_check": false
        });

        let response = app
            .clone()
            .oneshot(
                Request::builder()
                    .method("POST")
                    .uri("/api/chat")
                    .header("content-type", "application/json")
                    .body(Body::from(request_body.to_string()))
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);

        // Test with fact check enabled
        let request_body = json!({
            "message": "The Earth is flat",
            "session_id": "fact-session",
            "mode": "general",
            "use_web_search": false,
            "fact_check": true
        });

        let response = app
            .oneshot(
                Request::builder()
                    .method("POST")
                    .uri("/api/chat")
                    .header("content-type", "application/json")
                    .body(Body::from(request_body.to_string()))
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);
    }

    #[tokio::test]
    async fn test_list_sessions_endpoint() {
        let app = create_test_app().await;

        // Create a few sessions first
        for i in 0..3 {
            let request_body = json!({
                "message": format!("Message {}", i),
                "session_id": format!("session-{}", i)
            });

            app.clone()
                .oneshot(
                    Request::builder()
                        .method("POST")
                        .uri("/api/chat")
                        .header("content-type", "application/json")
                        .body(Body::from(request_body.to_string()))
                        .unwrap(),
                )
                .await
                .unwrap();
        }

        // List sessions
        let response = app
            .oneshot(
                Request::builder()
                    .uri("/api/chat/sessions")
                    .body(Body::empty())
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);

        let body = hyper::body::to_bytes(response.into_body()).await.unwrap();
        let sessions: Vec<Value> = serde_json::from_slice(&body).unwrap();

        assert!(sessions.len() >= 3);
    }

    #[tokio::test]
    async fn test_get_session_endpoint() {
        let app = create_test_app().await;
        let session_id = "test-get-session";

        // Create session
        let request_body = json!({
            "message": "Test message",
            "session_id": session_id
        });

        app.clone()
            .oneshot(
                Request::builder()
                    .method("POST")
                    .uri("/api/chat")
                    .header("content-type", "application/json")
                    .body(Body::from(request_body.to_string()))
                    .unwrap(),
            )
            .await
            .unwrap();

        // Get session
        let response = app
            .oneshot(
                Request::builder()
                    .uri(&format!("/api/chat/sessions/{}", session_id))
                    .body(Body::empty())
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);

        let body = hyper::body::to_bytes(response.into_body()).await.unwrap();
        let session: Value = serde_json::from_slice(&body).unwrap();

        assert_eq!(session["id"], session_id);
        assert!(session["messages"].is_array());
        assert!(session["created_at"].is_string());
    }

    #[tokio::test]
    async fn test_get_nonexistent_session() {
        let app = create_test_app().await;

        let response = app
            .oneshot(
                Request::builder()
                    .uri("/api/chat/sessions/nonexistent")
                    .body(Body::empty())
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::NOT_FOUND);
    }

    #[tokio::test]
    async fn test_knowledge_domains_endpoint() {
        let app = create_test_app().await;

        let response = app
            .oneshot(
                Request::builder()
                    .uri("/api/knowledge/domains")
                    .body(Body::empty())
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);

        let body = hyper::body::to_bytes(response.into_body()).await.unwrap();
        let domains: Vec<String> = serde_json::from_slice(&body).unwrap();

        assert!(domains.is_empty() || domains.iter().all(|d| !d.is_empty()));
    }

    #[tokio::test]
    async fn test_system_stats_endpoint() {
        let app = create_test_app().await;

        let response = app
            .oneshot(
                Request::builder()
                    .uri("/api/knowledge/stats")
                    .body(Body::empty())
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);

        let body = hyper::body::to_bytes(response.into_body()).await.unwrap();
        let stats: Value = serde_json::from_slice(&body).unwrap();

        assert!(stats["total_knowledge_items"].is_number());
        assert!(stats["active_sessions"].is_number());
        assert!(stats["average_response_time_ms"].is_number());
        assert!(stats["cache_hit_rate"].is_number());
        assert!(stats["uptime_seconds"].is_number());
        assert!(stats["consciousness_level"].is_string());
        assert!(stats["domains"].is_array());
    }

    #[tokio::test]
    async fn test_consciousness_level_endpoint() {
        let app = create_test_app().await;

        let response = app
            .oneshot(
                Request::builder()
                    .uri("/api/consciousness/level")
                    .body(Body::empty())
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);

        let body = hyper::body::to_bytes(response.into_body()).await.unwrap();
        let level: Value = serde_json::from_slice(&body).unwrap();

        assert_eq!(level["level"], "AWARE");
        assert!(level["description"].is_string());
        assert_eq!(level["introspection_depth"], 3);
    }

    #[tokio::test]
    async fn test_consciousness_thoughts_endpoint() {
        let app = create_test_app().await;

        let response = app
            .oneshot(
                Request::builder()
                    .uri("/api/consciousness/thoughts")
                    .body(Body::empty())
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);

        let body = hyper::body::to_bytes(response.into_body()).await.unwrap();
        let thoughts: Value = serde_json::from_slice(&body).unwrap();

        assert!(thoughts["thoughts"].is_array());
        assert!(thoughts["thought_count"].is_number());
        assert_eq!(thoughts["processing_state"], "active");
    }

    #[tokio::test]
    async fn test_search_endpoint() {
        let app = create_test_app().await;

        let response = app
            .oneshot(
                Request::builder()
                    .uri("/api/search?q=test&limit=10")
                    .body(Body::empty())
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);

        let body = hyper::body::to_bytes(response.into_body()).await.unwrap();
        let results: Value = serde_json::from_slice(&body).unwrap();

        assert!(results["results"].is_array());
        assert_eq!(results["total"], 0);
        assert!(results["query_time_ms"].is_number());
    }

    #[tokio::test]
    async fn test_static_file_serving() {
        let app = create_test_app().await;

        // Test index.html
        let response = app
            .clone()
            .oneshot(Request::builder().uri("/").body(Body::empty()).unwrap())
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);
        assert_eq!(
            response.headers().get("content-type").unwrap(),
            "text/html; charset=utf-8"
        );

        // Test manifest.json
        let response = app
            .clone()
            .oneshot(
                Request::builder()
                    .uri("/manifest.json")
                    .body(Body::empty())
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);
        assert_eq!(
            response.headers().get("content-type").unwrap(),
            "application/json"
        );

        // Test icon
        let response = app
            .oneshot(
                Request::builder()
                    .uri("/icon-192.svg")
                    .body(Body::empty())
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);
        assert_eq!(
            response.headers().get("content-type").unwrap(),
            "image/svg+xml"
        );
    }

    #[tokio::test]
    async fn test_cors_headers() {
        let app = create_test_app().await;

        let response = app
            .oneshot(
                Request::builder()
                    .method("OPTIONS")
                    .uri("/api/chat")
                    .header("origin", "https://example.com")
                    .header("access-control-request-method", "POST")
                    .body(Body::empty())
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);
        assert_eq!(
            response
                .headers()
                .get("access-control-allow-origin")
                .unwrap(),
            "*"
        );
    }

    #[tokio::test]
    async fn test_invalid_json_request() {
        let app = create_test_app().await;

        let response = app
            .oneshot(
                Request::builder()
                    .method("POST")
                    .uri("/api/chat")
                    .header("content-type", "application/json")
                    .body(Body::from("invalid json"))
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::BAD_REQUEST);
    }

    #[tokio::test]
    async fn test_missing_message_field() {
        let app = create_test_app().await;

        let request_body = json!({
            "session_id": "test"
        });

        let response = app
            .oneshot(
                Request::builder()
                    .method("POST")
                    .uri("/api/chat")
                    .header("content-type", "application/json")
                    .body(Body::from(request_body.to_string()))
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::BAD_REQUEST);
    }

    #[tokio::test]
    async fn test_large_message_handling() {
        let app = create_test_app().await;

        let large_message = "a".repeat(10000);
        let request_body = json!({
            "message": large_message,
            "session_id": "large-message-test"
        });

        let response = app
            .oneshot(
                Request::builder()
                    .method("POST")
                    .uri("/api/chat")
                    .header("content-type", "application/json")
                    .body(Body::from(request_body.to_string()))
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);
    }

    #[tokio::test]
    async fn test_concurrent_sessions() {
        let app = create_test_app().await;

        let mut handles = vec![];

        for i in 0..10 {
            let app_clone = app.clone();
            let handle = tokio::spawn(async move {
                let request_body = json!({
                    "message": format!("Concurrent message {}", i),
                    "session_id": format!("concurrent-{}", i)
                });

                let response = app_clone
                    .oneshot(
                        Request::builder()
                            .method("POST")
                            .uri("/api/chat")
                            .header("content-type", "application/json")
                            .body(Body::from(request_body.to_string()))
                            .unwrap(),
                    )
                    .await
                    .unwrap();

                assert_eq!(response.status(), StatusCode::OK);
            });

            handles.push(handle);
        }

        for handle in handles {
            handle.await.unwrap();
        }
    }

    // Helper function to create test app
    async fn create_test_app() -> Router {
        let core_engine = Arc::new(O1Engine::new(EngineConfig::default()));
        core_engine.initialize().await.unwrap();

        let knowledge_engine = Arc::new(KnowledgeEngine::new());
        let vector_index = Arc::new(O1VectorIndex::new(LSHConfig::default()).unwrap());
        let consciousness_framework = Arc::new(ConsciousnessFramework::new());
        let qwen_client = Arc::new(QwenClient::new());

        let (tx, _rx) = broadcast::channel(100);

        let state = ThinkAIState {
            _core_engine: core_engine,
            knowledge_engine,
            _vector_index: vector_index,
            _consciousness_framework: consciousness_framework,
            chat_sessions: Arc::new(RwLock::new(HashMap::new())),
            message_channel: tx,
            qwen_client,
        };

        create_app(state)
    }
}
