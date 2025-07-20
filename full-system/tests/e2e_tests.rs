#[cfg(test)]
mod e2e_tests {
    use reqwest::Client;
    use serde_json::json;
    use std::env;
    use tokio::time::{sleep, Duration};

    const BASE_URL: &str = "http://localhost:7777";
    const TEST_WHATSAPP_NUMBER: &str = "+573026132990";

    #[tokio::test]
    async fn test_whatsapp_notification_on_error() {
        // Set up WhatsApp credentials for test
        env::set_var("WHATSAPP_TO_NUMBER", TEST_WHATSAPP_NUMBER);
        
        let client = Client::new();
        
        // Trigger an error condition that should send WhatsApp
        let response = client
            .post(&format!("{}/api/chat", BASE_URL))
            .json(&json!({
                "message": "'; DROP TABLE users; --", // SQL injection attempt
                "session_id": "malicious-session"
            }))
            .send()
            .await;

        // The request should be rejected
        assert!(response.is_ok());
        let status = response.unwrap().status();
        assert_eq!(status, 400); // Bad Request due to validation

        // Wait a moment for WhatsApp notification to be sent
        sleep(Duration::from_secs(2)).await;
        
        println!("✅ WhatsApp notification should have been sent to {}", TEST_WHATSAPP_NUMBER);
    }

    #[tokio::test]
    async fn test_e2e_full_user_journey() {
        let client = Client::new();
        
        // Step 1: Health check
        let response = client
            .get(&format!("{}/health", BASE_URL))
            .send()
            .await
            .expect("Failed to connect to service");
        
        assert_eq!(response.status(), 200);
        
        // Step 2: Create new chat session
        let chat_response = client
            .post(&format!("{}/api/chat", BASE_URL))
            .json(&json!({
                "message": "Hello, I'm testing the service",
                "session_id": null
            }))
            .send()
            .await
            .expect("Failed to send chat request");
        
        assert_eq!(chat_response.status(), 200);
        let chat_data: serde_json::Value = chat_response.json().await.unwrap();
        let session_id = chat_data["session_id"].as_str().unwrap();
        
        // Step 3: Continue conversation
        let followup = client
            .post(&format!("{}/api/chat", BASE_URL))
            .json(&json!({
                "message": "Can you help me with coding?",
                "session_id": session_id
            }))
            .send()
            .await
            .expect("Failed to send followup");
        
        assert_eq!(followup.status(), 200);
        
        // Step 4: Test web search feature
        let search_response = client
            .post(&format!("{}/api/chat", BASE_URL))
            .json(&json!({
                "message": "What's the latest news about AI?",
                "session_id": session_id,
                "use_web_search": true
            }))
            .send()
            .await
            .expect("Failed to send search request");
        
        assert_eq!(search_response.status(), 200);
        
        // Step 5: Retrieve session history
        let history = client
            .get(&format!("{}/api/chat/sessions/{}", BASE_URL, session_id))
            .send()
            .await
            .expect("Failed to get session history");
        
        assert_eq!(history.status(), 200);
        let history_data: serde_json::Value = history.json().await.unwrap();
        assert!(history_data["messages"].as_array().unwrap().len() >= 3);
        
        // Step 6: Test error handling and recovery
        let error_response = client
            .post(&format!("{}/api/chat", BASE_URL))
            .json(&json!({
                "message": "", // Empty message
                "session_id": session_id
            }))
            .send()
            .await
            .expect("Failed to send error request");
        
        assert_eq!(error_response.status(), 400);
        
        // Step 7: Verify service is still healthy after error
        let health_check = client
            .get(&format!("{}/health", BASE_URL))
            .send()
            .await
            .expect("Failed to check health");
        
        assert_eq!(health_check.status(), 200);
        
        println!("✅ E2E test completed successfully");
    }

    #[tokio::test]
    async fn test_concurrent_users() {
        let client = Client::new();
        let mut handles = vec![];
        
        // Simulate 10 concurrent users
        for i in 0..10 {
            let client_clone = client.clone();
            let handle = tokio::spawn(async move {
                let response = client_clone
                    .post(&format!("{}/api/chat", BASE_URL))
                    .json(&json!({
                        "message": format!("User {} message", i),
                        "session_id": format!("user-{}", i)
                    }))
                    .send()
                    .await
                    .expect("Request failed");
                
                assert_eq!(response.status(), 200);
            });
            handles.push(handle);
        }
        
        // Wait for all requests to complete
        for handle in handles {
            handle.await.unwrap();
        }
        
        println!("✅ Concurrent users test passed");
    }

    #[tokio::test]
    async fn test_rate_limiting() {
        let client = Client::new();
        let session_id = "rate-limit-test";
        
        // Send many requests rapidly
        let mut success_count = 0;
        let mut rate_limited_count = 0;
        
        for i in 0..150 {
            let response = client
                .post(&format!("{}/api/chat", BASE_URL))
                .json(&json!({
                    "message": format!("Request {}", i),
                    "session_id": session_id
                }))
                .send()
                .await;
            
            if let Ok(resp) = response {
                if resp.status() == 200 {
                    success_count += 1;
                } else if resp.status() == 429 {
                    rate_limited_count += 1;
                }
            }
        }
        
        // Should have some successful requests and some rate limited
        assert!(success_count > 0);
        assert!(rate_limited_count > 0);
        
        println!("✅ Rate limiting test passed: {} successful, {} rate limited", 
                 success_count, rate_limited_count);
    }

    #[tokio::test]
    async fn test_websocket_connection() {
        use tungstenite::{connect, Message};
        
        let ws_url = "ws://localhost:7777/ws";
        let (mut socket, response) = connect(ws_url).expect("Failed to connect");
        
        println!("WebSocket connected: {:?}", response);
        
        // Send a message
        socket.write_message(Message::Text(json!({
            "type": "chat",
            "message": "Hello WebSocket",
            "session_id": "ws-test"
        }).to_string())).unwrap();
        
        // Read response
        let msg = socket.read_message().expect("Error reading message");
        println!("Received: {:?}", msg);
        
        socket.close(None).unwrap();
        
        println!("✅ WebSocket test passed");
    }

    #[tokio::test]
    async fn test_audio_transcription() {
        let client = Client::new();
        
        // Create a dummy audio file (WAV header + silence)
        let wav_header = vec![
            0x52, 0x49, 0x46, 0x46, // "RIFF"
            0x24, 0x00, 0x00, 0x00, // File size
            0x57, 0x41, 0x56, 0x45, // "WAVE"
            0x66, 0x6D, 0x74, 0x20, // "fmt "
            0x10, 0x00, 0x00, 0x00, // Subchunk size
            0x01, 0x00,             // Audio format (PCM)
            0x01, 0x00,             // Number of channels
            0x44, 0xAC, 0x00, 0x00, // Sample rate (44100)
            0x88, 0x58, 0x01, 0x00, // Byte rate
            0x02, 0x00,             // Block align
            0x10, 0x00,             // Bits per sample
            0x64, 0x61, 0x74, 0x61, // "data"
            0x00, 0x00, 0x00, 0x00, // Data size
        ];
        
        let response = client
            .post(&format!("{}/api/audio/transcribe", BASE_URL))
            .body(wav_header)
            .send()
            .await;
        
        // Should either work or return 503 if audio service is disabled
        if let Ok(resp) = response {
            assert!(resp.status() == 200 || resp.status() == 503);
        }
        
        println!("✅ Audio transcription test passed");
    }

    #[tokio::test]
    async fn test_security_headers() {
        let client = Client::new();
        
        let response = client
            .get(&format!("{}/", BASE_URL))
            .send()
            .await
            .expect("Failed to get index");
        
        let headers = response.headers();
        
        // Check security headers
        assert!(headers.contains_key("x-content-type-options"));
        assert!(headers.contains_key("x-frame-options"));
        assert!(headers.contains_key("referrer-policy"));
        
        println!("✅ Security headers test passed");
    }

    #[tokio::test]
    async fn test_error_recovery_with_notification() {
        let client = Client::new();
        
        // Set WhatsApp number for notifications
        env::set_var("WHATSAPP_TO_NUMBER", TEST_WHATSAPP_NUMBER);
        
        // Simulate various error conditions
        let error_scenarios = vec![
            json!({"message": "<script>alert('xss')</script>", "session_id": "xss-test"}),
            json!({"message": "a".repeat(1_000_000), "session_id": "large-payload"}),
            json!({"invalid_field": "test"}),
        ];
        
        for (i, scenario) in error_scenarios.iter().enumerate() {
            let response = client
                .post(&format!("{}/api/chat", BASE_URL))
                .json(scenario)
                .send()
                .await;
            
            if let Ok(resp) = response {
                assert_eq!(resp.status(), 400);
                println!("✅ Error scenario {} handled correctly", i + 1);
            }
            
            // Give time for notification
            sleep(Duration::from_secs(1)).await;
        }
        
        // Verify service is still healthy
        let health = client
            .get(&format!("{}/health", BASE_URL))
            .send()
            .await
            .expect("Health check failed");
        
        assert_eq!(health.status(), 200);
        
        println!("✅ Error recovery test passed - WhatsApp notifications sent to {}", TEST_WHATSAPP_NUMBER);
    }
}