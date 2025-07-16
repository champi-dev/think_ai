use think_ai_codellama::{CodeAssistant, CodeLlamaClient};

#[tokio::test]
async fn test_codellama_availability() {
    let client = CodeLlamaClient::new().unwrap();
    let available = client.check_model_availability().await.unwrap();

    println!("CodeLlama model available: {}", available);

    if available {
        // Test a simple code generation
        let response = client
            .generate_code("Write a hello world function in Python")
            .await;
        match response {
            Ok(code) => {
                println!("Generated code:\n{}", code);
                assert!(code.contains("def") || code.contains("print"));
            }
            Err(e) => {
                println!("Error generating code: {}", e);
            }
        }
    } else {
        println!("CodeLlama model not available, skipping generation test");
    }
}

#[tokio::test]
async fn test_code_detection() {
    let client = CodeLlamaClient::new().unwrap();

    // Test code-related query detection
    assert!(client.is_code_related("write a python function").await);
    assert!(client.is_code_related("debug this javascript").await);
    assert!(client.is_code_related("implement binary search").await);

    // Test non-code queries
    assert!(!client.is_code_related("what is the weather").await);
    assert!(!client.is_code_related("tell me a joke").await);
}

#[tokio::test]
async fn test_caching_performance() {
    let client = CodeLlamaClient::new().unwrap();

    // Skip if model not available
    if !client.check_model_availability().await.unwrap_or(false) {
        println!("CodeLlama not available, skipping cache test");
        return;
    }

    // First request (cache miss)
    let prompt = "Write a function to add two numbers";
    let _ = client.generate_code(prompt).await;

    // Second request (should be cache hit)
    let _ = client.generate_code(prompt).await;

    let metrics = client.get_metrics().await;
    assert_eq!(metrics.total_requests, 2);
    assert_eq!(metrics.cache_hits, 1);
    assert_eq!(metrics.cache_misses, 1);

    println!(
        "Cache hit rate: {}%",
        (metrics.cache_hits as f64 / metrics.total_requests as f64) * 100.0
    );
}
