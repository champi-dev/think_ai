use axum::{body::Body, http::{Request, StatusCode}, response::Response};
use serde_json::json;
use think_ai_full_production::{create_app, ChatRequest, ChatResponse};
use tower::ServiceExt;

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_chat_handler_valid_request() {
        let app = create_app().await;
        
        let request = Request::builder()
            .method("POST")
            .uri("/api/chat")
            .header("content-type", "application/json")
            .body(Body::from(
                json!({
                    "message": "What is artificial intelligence?",
                    "session_id": "test-session-123"
                })
                .to_string(),
            ))
            .unwrap();

        let response: Response = app.oneshot(request).await.unwrap();
        
        assert_eq!(response.status(), StatusCode::OK);
        
        let body = hyper::body::to_bytes(response.into_body()).await.unwrap();
        let chat_response: ChatResponse = serde_json::from_slice(&body).unwrap();
        
        assert!(!chat_response.response.is_empty());
        assert_eq!(chat_response.session_id, "test-session-123");
        assert!(chat_response.confidence > 0.0);
        assert!(chat_response.response_time_ms > 0);
    }

    #[tokio::test]
    async fn test_chat_handler_empty_message() {
        let app = create_app().await;
        
        let request = Request::builder()
            .method("POST")
            .uri("/api/chat")
            .header("content-type", "application/json")
            .body(Body::from(
                json!({
                    "message": "",
                    "session_id": "test-session-456"
                })
                .to_string(),
            ))
            .unwrap();

        let response: Response = app.oneshot(request).await.unwrap();
        
        assert_eq!(response.status(), StatusCode::BAD_REQUEST);
    }

    #[tokio::test]
    async fn test_chat_handler_injection_attack() {
        let app = create_app().await;
        
        let request = Request::builder()
            .method("POST")
            .uri("/api/chat")
            .header("content-type", "application/json")
            .body(Body::from(
                json!({
                    "message": "<script>alert('xss')</script>",
                    "session_id": "test-session-789"
                })
                .to_string(),
            ))
            .unwrap();

        let response: Response = app.oneshot(request).await.unwrap();
        
        assert_eq!(response.status(), StatusCode::BAD_REQUEST);
    }

    #[tokio::test]
    async fn test_chat_handler_sql_injection() {
        let app = create_app().await;
        
        let request = Request::builder()
            .method("POST")
            .uri("/api/chat")
            .header("content-type", "application/json")
            .body(Body::from(
                json!({
                    "message": "'; DROP TABLE users; --",
                    "session_id": "test-session-sql"
                })
                .to_string(),
            ))
            .unwrap();

        let response: Response = app.oneshot(request).await.unwrap();
        
        assert_eq!(response.status(), StatusCode::BAD_REQUEST);
    }

    #[tokio::test]
    async fn test_chat_handler_new_session() {
        let app = create_app().await;
        
        let request = Request::builder()
            .method("POST")
            .uri("/api/chat")
            .header("content-type", "application/json")
            .body(Body::from(
                json!({
                    "message": "Hello, I'm a new user"
                })
                .to_string(),
            ))
            .unwrap();

        let response: Response = app.oneshot(request).await.unwrap();
        
        assert_eq!(response.status(), StatusCode::OK);
        
        let body = hyper::body::to_bytes(response.into_body()).await.unwrap();
        let chat_response: ChatResponse = serde_json::from_slice(&body).unwrap();
        
        // Should generate a new session ID
        assert!(!chat_response.session_id.is_empty());
        assert!(uuid::Uuid::parse_str(&chat_response.session_id).is_ok());
    }

    #[tokio::test]
    async fn test_chat_handler_modes() {
        let app = create_app().await;
        
        // Test code mode
        let request = Request::builder()
            .method("POST")
            .uri("/api/chat")
            .header("content-type", "application/json")
            .body(Body::from(
                json!({
                    "message": "Write a Python function to calculate fibonacci",
                    "mode": "code"
                })
                .to_string(),
            ))
            .unwrap();

        let response: Response = app.oneshot(request).await.unwrap();
        assert_eq!(response.status(), StatusCode::OK);
    }

    #[tokio::test]
    async fn test_chat_handler_web_search() {
        let app = create_app().await;
        
        let request = Request::builder()
            .method("POST")
            .uri("/api/chat")
            .header("content-type", "application/json")
            .body(Body::from(
                json!({
                    "message": "What's the latest news about AI?",
                    "use_web_search": true
                })
                .to_string(),
            ))
            .unwrap();

        let response: Response = app.oneshot(request).await.unwrap();
        assert_eq!(response.status(), StatusCode::OK);
    }

    #[tokio::test]
    async fn test_concurrent_requests() {
        let app = create_app().await;
        
        let mut handles = vec![];
        
        for i in 0..10 {
            let app_clone = app.clone();
            let handle = tokio::spawn(async move {
                let request = Request::builder()
                    .method("POST")
                    .uri("/api/chat")
                    .header("content-type", "application/json")
                    .body(Body::from(
                        json!({
                            "message": format!("Concurrent request {}", i),
                            "session_id": format!("concurrent-{}", i)
                        })
                        .to_string(),
                    ))
                    .unwrap();

                let response: Response = app_clone.oneshot(request).await.unwrap();
                assert_eq!(response.status(), StatusCode::OK);
            });
            handles.push(handle);
        }
        
        for handle in handles {
            handle.await.unwrap();
        }
    }
}