use std::time::{Duration, Instant};
use think_ai_qwen::{QwenClient, QwenConfig, QwenRequest};

#[tokio::test]
async fn test_qwen_basic_response() {
    let client = QwenClient::new();
    let request = QwenRequest {
        query: "What is 2+2?".to_string(),
        context: None,
        system_prompt: None,
    };

    let start = Instant::now();
    let result = client.generate(request).await;
    let elapsed = start.elapsed();

    assert!(
        result.is_ok(),
        "Failed to generate response: {:?}",
        result.err()
    );
    assert!(
        elapsed < Duration::from_secs(35),
        "Response took too long: {:?}",
        elapsed
    );

    let response = result.unwrap();
    assert!(!response.content.is_empty());
    assert!(response.usage.total_tokens > 0);
}

#[tokio::test]
async fn test_gemini_fallback_when_ollama_down() {
    // This test requires GEMINI_API_KEY to be set
    if std::env::var("GEMINI_API_KEY").is_err() {
        eprintln!("Skipping Gemini fallback test - GEMINI_API_KEY not set");
        return;
    }

    // Use a config that points to a non-existent Ollama instance
    let mut config = QwenConfig::default();
    config.base_url = "http://localhost:99999".to_string(); // Invalid port

    let client = QwenClient::new_with_config(config);
    let request = QwenRequest {
        query: "Hello".to_string(),
        context: None,
        system_prompt: None,
    };

    let start = Instant::now();
    let result = client.generate(request).await;
    let elapsed = start.elapsed();

    assert!(result.is_ok(), "Gemini fallback failed: {:?}", result.err());
    assert!(
        elapsed < Duration::from_secs(1),
        "Fallback took too long: {:?}",
        elapsed
    );

    let response = result.unwrap();
    assert!(!response.content.is_empty());
}

#[tokio::test]
async fn test_response_within_timeout() {
    let client = QwenClient::new();

    // Test 5 concurrent requests
    let mut handles = vec![];

    for i in 0..5 {
        let client_clone = QwenClient::new();
        let handle = tokio::spawn(async move {
            let request = QwenRequest {
                query: format!("Test request {}", i),
                context: None,
                system_prompt: None,
            };

            let start = Instant::now();
            let result = client_clone.generate(request).await;
            let elapsed = start.elapsed();

            (result, elapsed)
        });
        handles.push(handle);
    }

    // Wait for all requests
    let mut all_success = true;
    for handle in handles {
        let (result, elapsed) = handle.await.unwrap();
        if result.is_err() || elapsed >= Duration::from_secs(35) {
            all_success = false;
            eprintln!(
                "Request failed or took too long: {:?}, elapsed: {:?}",
                result.err(),
                elapsed
            );
        }
    }

    assert!(all_success, "Not all requests completed within 35 seconds");
}

#[tokio::test]
async fn test_streaming_response() {
    let client = QwenClient::new_streaming();
    let request = QwenRequest {
        query: "Count to 3".to_string(),
        context: None,
        system_prompt: None,
    };

    let start = Instant::now();
    let result = client.generate_stream(request).await;

    assert!(
        result.is_ok(),
        "Failed to create stream: {:?}",
        result.err()
    );

    let mut receiver = result.unwrap();
    let mut chunks = vec![];

    while let Some(chunk_result) = receiver.recv().await {
        if let Ok(chunk) = chunk_result {
            chunks.push(chunk);
        }

        // Ensure we're not waiting too long
        if start.elapsed() > Duration::from_secs(2) {
            break;
        }
    }

    assert!(!chunks.is_empty(), "No chunks received from stream");
}

#[tokio::test]
async fn test_context_handling() {
    let client = QwenClient::new();
    let request = QwenRequest {
        query: "What did I just ask?".to_string(),
        context: Some("User asked: What is the capital of France?".to_string()),
        system_prompt: Some("You are a helpful assistant.".to_string()),
    };

    let result = client.generate(request).await;
    assert!(result.is_ok());

    let response = result.unwrap();
    // The response should reference the context
    assert!(!response.content.is_empty());
}

#[test]
fn test_client_creation() {
    let client = QwenClient::new();
    let _client_with_defaults = QwenClient::new_with_defaults();
    let _streaming_client = QwenClient::new_streaming();

    // Test custom config
    let config = QwenConfig {
        api_key: None,
        base_url: "http://localhost:11434".to_string(),
        model: "qwen2.5:3b".to_string(),
    };
    let _custom_client = QwenClient::new_with_config(config);
}

#[tokio::test]
async fn test_generate_simple() {
    let client = QwenClient::new();

    let result = client.generate_simple("What is 1+1?", None).await;
    assert!(result.is_ok());
    assert!(!result.unwrap().is_empty());

    let result_with_context = client
        .generate_simple(
            "What was my previous question?",
            Some("You asked about 1+1"),
        )
        .await;
    assert!(result_with_context.is_ok());
}

#[tokio::test]
async fn test_generate_with_context() {
    let client = QwenClient::new();

    let result = client
        .generate_with_context("Explain this", "Quantum computing uses qubits", Some(0.5))
        .await;

    assert!(result.is_ok());
    assert!(!result.unwrap().is_empty());
}
