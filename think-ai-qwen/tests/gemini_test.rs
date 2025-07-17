use std::time::{Duration, Instant};
use think_ai_qwen::gemini::{GeminiClient, GeminiConfig};

#[tokio::test]
async fn test_gemini_basic_response() {
    // Skip if no API key
    let api_key = match std::env::var("GEMINI_API_KEY") {
        Ok(key) if !key.is_empty() => key,
        _ => {
            eprintln!("Skipping Gemini test - GEMINI_API_KEY not set");
            return;
        }
    };

    let client = GeminiClient::new(api_key);

    let start = Instant::now();
    let result = client.generate("What is 2+2?".to_string(), None).await;
    let elapsed = start.elapsed();

    assert!(
        result.is_ok(),
        "Failed to generate response: {:?}",
        result.err()
    );
    assert!(
        elapsed < Duration::from_millis(500),
        "Response took too long: {:?}",
        elapsed
    );

    let (content, usage) = result.unwrap();
    assert!(!content.is_empty());
    assert!(usage.total_tokens > 0);
}

#[tokio::test]
async fn test_gemini_with_temperature() {
    let api_key = match std::env::var("GEMINI_API_KEY") {
        Ok(key) if !key.is_empty() => key,
        _ => {
            eprintln!("Skipping Gemini temperature test - GEMINI_API_KEY not set");
            return;
        }
    };

    let client = GeminiClient::new(api_key);

    // Test with low temperature (more deterministic)
    let result = client.generate("What is 1+1?".to_string(), Some(0.1)).await;
    assert!(result.is_ok());

    // Test with high temperature (more creative)
    let result = client
        .generate("Tell me a story".to_string(), Some(0.9))
        .await;
    assert!(result.is_ok());
}

#[tokio::test]
async fn test_gemini_concurrent_requests() {
    let api_key = match std::env::var("GEMINI_API_KEY") {
        Ok(key) if !key.is_empty() => key,
        _ => {
            eprintln!("Skipping Gemini concurrent test - GEMINI_API_KEY not set");
            return;
        }
    };

    let client = GeminiClient::new(api_key.clone());

    // Test 3 concurrent requests
    let mut handles = vec![];

    for i in 0..3 {
        let api_key_clone = api_key.clone();
        let handle = tokio::spawn(async move {
            let client = GeminiClient::new(api_key_clone);
            let start = Instant::now();
            let result = client.generate(format!("What is {}+{}?", i, i), None).await;
            let elapsed = start.elapsed();

            (result, elapsed)
        });
        handles.push(handle);
    }

    // Wait for all requests
    let mut all_success = true;
    for handle in handles {
        let (result, elapsed) = handle.await.unwrap();
        if result.is_err() || elapsed >= Duration::from_millis(500) {
            all_success = false;
            eprintln!(
                "Gemini request failed or took too long: {:?}, elapsed: {:?}",
                result.err(),
                elapsed
            );
        }
    }

    assert!(
        all_success,
        "Not all Gemini requests completed within 500ms"
    );
}

#[test]
fn test_gemini_config() {
    let config = GeminiConfig::default();
    assert_eq!(
        config.base_url,
        "https://generativelanguage.googleapis.com/v1beta"
    );
    assert_eq!(config.model, "gemini-1.5-flash");

    let custom_config = GeminiConfig {
        api_key: "test_key".to_string(),
        base_url: "https://custom.url".to_string(),
        model: "gemini-pro".to_string(),
    };

    let client = GeminiClient::new_with_config(custom_config);
    // Client should be created successfully
}
