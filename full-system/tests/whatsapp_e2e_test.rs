#[cfg(test)]
mod whatsapp_e2e_tests {
    use reqwest::Client;
    use serde_json::json;
    use std::collections::HashMap;

    const BASE_URL: &str = "http://localhost:7777";

    #[tokio::test]
    async fn test_whatsapp_help_command() {
        let client = Client::new();
        
        // Simulate WhatsApp webhook from Twilio
        let mut form_data = HashMap::new();
        form_data.insert("Body", "help");
        form_data.insert("From", "whatsapp:+573026132990");
        form_data.insert("To", "whatsapp:+14155238886");
        form_data.insert("MessageSid", "SM12345");
        form_data.insert("AccountSid", "test_account_sid");
        
        let response = client
            .post(&format!("{}/webhooks/whatsapp", BASE_URL))
            .form(&form_data)
            .send()
            .await
            .expect("Failed to send webhook");
        
        assert_eq!(response.status(), 200);
        
        let body = response.text().await.unwrap();
        assert!(body.contains("ThinkAI WhatsApp Assistant"));
        assert!(body.contains("/help"));
        assert!(body.contains("/status"));
    }

    #[tokio::test]
    async fn test_whatsapp_chat_interaction() {
        let client = Client::new();
        
        // Test regular chat
        let mut form_data = HashMap::new();
        form_data.insert("Body", "What is artificial intelligence?");
        form_data.insert("From", "whatsapp:+573026132990");
        form_data.insert("To", "whatsapp:+14155238886");
        form_data.insert("MessageSid", "SM12346");
        form_data.insert("AccountSid", "test_account_sid");
        
        let response = client
            .post(&format!("{}/webhooks/whatsapp", BASE_URL))
            .form(&form_data)
            .send()
            .await
            .expect("Failed to send webhook");
        
        assert_eq!(response.status(), 200);
        
        let body = response.text().await.unwrap();
        assert!(body.contains("<Response>"));
        assert!(body.contains("<Message>"));
        assert!(body.contains("AI") || body.contains("artificial") || body.contains("intelligence"));
    }

    #[tokio::test]
    async fn test_whatsapp_status_command() {
        let client = Client::new();
        
        let mut form_data = HashMap::new();
        form_data.insert("Body", "/status");
        form_data.insert("From", "whatsapp:+573026132990");
        form_data.insert("To", "whatsapp:+14155238886");
        form_data.insert("MessageSid", "SM12347");
        form_data.insert("AccountSid", "test_account_sid");
        
        let response = client
            .post(&format!("{}/webhooks/whatsapp", BASE_URL))
            .form(&form_data)
            .send()
            .await
            .expect("Failed to send webhook");
        
        assert_eq!(response.status(), 200);
        
        let body = response.text().await.unwrap();
        assert!(body.contains("System Status"));
        assert!(body.contains("Online"));
        assert!(body.contains("https://thinkai.lat"));
    }

    #[tokio::test]
    async fn test_whatsapp_conversation_flow() {
        let client = Client::new();
        let phone = "whatsapp:+573026132990";
        
        // Message 1: Introduction
        let mut form_data = HashMap::new();
        form_data.insert("Body", "Hello, my name is TestUser");
        form_data.insert("From", phone);
        form_data.insert("To", "whatsapp:+14155238886");
        form_data.insert("MessageSid", "SM12348");
        form_data.insert("AccountSid", "test_account_sid");
        
        let response = client
            .post(&format!("{}/webhooks/whatsapp", BASE_URL))
            .form(&form_data)
            .send()
            .await
            .unwrap();
        
        assert_eq!(response.status(), 200);
        
        // Message 2: Follow-up
        form_data.insert("Body", "What's my name?");
        form_data.insert("MessageSid", "SM12349");
        
        let response = client
            .post(&format!("{}/webhooks/whatsapp", BASE_URL))
            .form(&form_data)
            .send()
            .await
            .unwrap();
        
        assert_eq!(response.status(), 200);
        let body = response.text().await.unwrap();
        assert!(body.contains("TestUser") || body.contains("name"));
    }

    #[tokio::test]
    async fn test_whatsapp_clear_command() {
        let client = Client::new();
        
        let mut form_data = HashMap::new();
        form_data.insert("Body", "/clear");
        form_data.insert("From", "whatsapp:+573026132990");
        form_data.insert("To", "whatsapp:+14155238886");
        form_data.insert("MessageSid", "SM12350");
        form_data.insert("AccountSid", "test_account_sid");
        
        let response = client
            .post(&format!("{}/webhooks/whatsapp", BASE_URL))
            .form(&form_data)
            .send()
            .await
            .unwrap();
        
        assert_eq!(response.status(), 200);
        let body = response.text().await.unwrap();
        assert!(body.contains("cleared"));
    }

    #[tokio::test]
    async fn test_whatsapp_code_request() {
        let client = Client::new();
        
        let mut form_data = HashMap::new();
        form_data.insert("Body", "Write a Python function to calculate fibonacci");
        form_data.insert("From", "whatsapp:+573026132990");
        form_data.insert("To", "whatsapp:+14155238886");
        form_data.insert("MessageSid", "SM12351");
        form_data.insert("AccountSid", "test_account_sid");
        
        let response = client
            .post(&format!("{}/webhooks/whatsapp", BASE_URL))
            .form(&form_data)
            .send()
            .await
            .unwrap();
        
        assert_eq!(response.status(), 200);
        let body = response.text().await.unwrap();
        assert!(body.contains("def") || body.contains("fibonacci") || body.contains("Python"));
    }

    #[tokio::test]
    async fn test_whatsapp_concurrent_users() {
        let client = Client::new();
        let mut handles = vec![];
        
        for i in 0..5 {
            let client_clone = client.clone();
            let handle = tokio::spawn(async move {
                let mut form_data = HashMap::new();
                form_data.insert("Body", format!("User {} message", i));
                form_data.insert("From", &format!("whatsapp:+57302613{}", 2990 + i));
                form_data.insert("To", "whatsapp:+14155238886");
                form_data.insert("MessageSid", &format!("SM1235{}", i));
                form_data.insert("AccountSid", "test_account_sid");
                
                let response = client_clone
                    .post(&format!("{}/webhooks/whatsapp", BASE_URL))
                    .form(&form_data)
                    .send()
                    .await
                    .unwrap();
                
                assert_eq!(response.status(), 200);
            });
            handles.push(handle);
        }
        
        for handle in handles {
            handle.await.unwrap();
        }
    }

    #[tokio::test]
    async fn test_whatsapp_error_handling() {
        let client = Client::new();
        
        // Test with malformed data
        let response = client
            .post(&format!("{}/webhooks/whatsapp", BASE_URL))
            .json(&json!({"invalid": "data"}))
            .send()
            .await;
        
        // Should handle gracefully
        assert!(response.is_ok());
    }

    #[tokio::test]
    async fn test_whatsapp_long_message() {
        let client = Client::new();
        
        let long_message = "Tell me about ".to_string() + &"artificial intelligence ".repeat(100);
        
        let mut form_data = HashMap::new();
        form_data.insert("Body", &long_message);
        form_data.insert("From", "whatsapp:+573026132990");
        form_data.insert("To", "whatsapp:+14155238886");
        form_data.insert("MessageSid", "SM12352");
        form_data.insert("AccountSid", "test_account_sid");
        
        let response = client
            .post(&format!("{}/webhooks/whatsapp", BASE_URL))
            .form(&form_data)
            .send()
            .await
            .unwrap();
        
        assert_eq!(response.status(), 200);
        let body = response.text().await.unwrap();
        
        // Response should be truncated for WhatsApp
        assert!(body.len() < 2000); // TwiML wrapper + 1500 char limit
    }
}