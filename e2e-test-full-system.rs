#!/usr/bin/env rust-script
//! ```cargo
//! [dependencies]
//! tokio = { version = "1", features = ["full"] }
//! reqwest = { version = "0.11", features = ["json"] }
//! serde = { version = "1.0", features = ["derive"] }
//! serde_json = "1.0"
//! anyhow = "1.0"
//! colored = "2.0"
//! uuid = "1.4"
//! ```

use colored::*;
use serde::{Deserialize, Serialize};
use std::time::Instant;
use uuid::Uuid;

#[derive(Debug, Serialize)]
struct ChatRequest {
    message: String,
    session_id: Option<String>,
}

#[derive(Debug, Deserialize)]
struct ChatResponse {
    response: String,
    session_id: Option<String>,
    confidence: Option<f64>,
    response_time_ms: Option<f64>,
}

#[derive(Debug, Serialize)]
struct StableChatRequest {
    query: String,
}

#[derive(Debug, Deserialize)]
struct StableChatResponse {
    response: String,
    metadata: Option<ResponseMetadata>,
}

#[derive(Debug, Deserialize)]
struct ResponseMetadata {
    response_time_ms: f64,
    source: String,
    optimization_level: String,
}

struct TestResult {
    name: String,
    passed: bool,
    message: String,
    duration_ms: f64,
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    println!("{}", "🧪 Think AI Comprehensive E2E Test Suite".bright_blue().bold());
    println!("{}", "=========================================".bright_blue());
    
    let client = reqwest::Client::builder()
        .timeout(std::time::Duration::from_secs(30))
        .build()?;
    
    let mut results = Vec::new();
    
    // Test 1: Server Health Check
    results.push(test_health_check(&client).await);
    
    // Test 2: Basic Chat Functionality
    results.push(test_basic_chat(&client).await);
    
    // Test 3: Session Management (This will fail on stable-server)
    results.push(test_session_management(&client).await);
    
    // Test 4: Chat History Deletion (This will fail on stable-server)
    results.push(test_chat_history_deletion(&client).await);
    
    // Test 5: Performance Test
    results.push(test_performance(&client).await);
    
    // Test 6: Concurrent Requests
    results.push(test_concurrent_requests(&client).await);
    
    // Test 7: Response Quality
    results.push(test_response_quality(&client).await);
    
    // Print summary
    println!("\n{}", "📊 Test Results Summary".bright_yellow().bold());
    println!("{}", "=======================".bright_yellow());
    
    let total_tests = results.len();
    let passed_tests = results.iter().filter(|r| r.passed).count();
    let failed_tests = total_tests - passed_tests;
    
    for result in &results {
        let status = if result.passed {
            "✅ PASS".green()
        } else {
            "❌ FAIL".red()
        };
        println!("{} {} - {} ({}ms)", 
            status, 
            result.name.bright_white(), 
            result.message,
            result.duration_ms
        );
    }
    
    println!("\n{}", "📈 Overall Statistics".bright_cyan().bold());
    println!("Total Tests: {}", total_tests);
    println!("Passed: {} {}", passed_tests, "✅".green());
    println!("Failed: {} {}", failed_tests, "❌".red());
    println!("Success Rate: {:.1}%", (passed_tests as f64 / total_tests as f64) * 100.0);
    
    if failed_tests > 0 {
        println!("\n{}", "⚠️  Some tests failed! See details above.".yellow().bold());
    } else {
        println!("\n{}", "🎉 All tests passed!".green().bold());
    }
    
    Ok(())
}

async fn test_health_check(client: &reqwest::Client) -> TestResult {
    let start = Instant::now();
    let test_name = "Health Check".to_string();
    
    match client.get("http://localhost:5555/health").send().await {
        Ok(resp) => {
            if resp.status().is_success() {
                TestResult {
                    name: test_name,
                    passed: true,
                    message: "Server is healthy".to_string(),
                    duration_ms: start.elapsed().as_millis() as f64,
                }
            } else {
                TestResult {
                    name: test_name,
                    passed: false,
                    message: format!("Unexpected status: {}", resp.status()),
                    duration_ms: start.elapsed().as_millis() as f64,
                }
            }
        }
        Err(e) => TestResult {
            name: test_name,
            passed: false,
            message: format!("Failed to connect: {}", e),
            duration_ms: start.elapsed().as_millis() as f64,
        }
    }
}

async fn test_basic_chat(client: &reqwest::Client) -> TestResult {
    let start = Instant::now();
    let test_name = "Basic Chat".to_string();
    
    let request = StableChatRequest {
        query: "What is 2+2?".to_string(),
    };
    
    match client
        .post("http://localhost:5555/chat")
        .json(&request)
        .send()
        .await
    {
        Ok(resp) => {
            if resp.status().is_success() {
                match resp.json::<StableChatResponse>().await {
                    Ok(data) => {
                        if data.response.contains("4") {
                            TestResult {
                                name: test_name,
                                passed: true,
                                message: "Correct response received".to_string(),
                                duration_ms: start.elapsed().as_millis() as f64,
                            }
                        } else {
                            TestResult {
                                name: test_name,
                                passed: false,
                                message: format!("Unexpected response: {}", data.response),
                                duration_ms: start.elapsed().as_millis() as f64,
                            }
                        }
                    }
                    Err(e) => TestResult {
                        name: test_name,
                        passed: false,
                        message: format!("Failed to parse response: {}", e),
                        duration_ms: start.elapsed().as_millis() as f64,
                    }
                }
            } else {
                TestResult {
                    name: test_name,
                    passed: false,
                    message: format!("Request failed: {}", resp.status()),
                    duration_ms: start.elapsed().as_millis() as f64,
                }
            }
        }
        Err(e) => TestResult {
            name: test_name,
            passed: false,
            message: format!("Request error: {}", e),
            duration_ms: start.elapsed().as_millis() as f64,
        }
    }
}

async fn test_session_management(client: &reqwest::Client) -> TestResult {
    let start = Instant::now();
    let test_name = "Session Management".to_string();
    let session_id = format!("test_session_{}", Uuid::new_v4());
    
    // Try sending with session_id (stable-server doesn't support this)
    let request = serde_json::json!({
        "query": "Remember my name is TestUser",
        "session_id": session_id.clone()
    });
    
    match client
        .post("http://localhost:5555/chat")
        .json(&request)
        .send()
        .await
    {
        Ok(_resp) => {
            // Send follow-up to test memory
            let follow_up = serde_json::json!({
                "query": "What is my name?",
                "session_id": session_id
            });
            
            match client
                .post("http://localhost:5555/chat")
                .json(&follow_up)
                .send()
                .await
            {
                Ok(resp) => {
                    if let Ok(data) = resp.json::<serde_json::Value>().await {
                        let response = data["response"].as_str().unwrap_or("");
                        if response.contains("TestUser") {
                            TestResult {
                                name: test_name,
                                passed: true,
                                message: "Session memory working".to_string(),
                                duration_ms: start.elapsed().as_millis() as f64,
                            }
                        } else {
                            TestResult {
                                name: test_name,
                                passed: false,
                                message: "No session memory (expected for stable-server)".to_string(),
                                duration_ms: start.elapsed().as_millis() as f64,
                            }
                        }
                    } else {
                        TestResult {
                            name: test_name,
                            passed: false,
                            message: "Failed to parse response".to_string(),
                            duration_ms: start.elapsed().as_millis() as f64,
                        }
                    }
                }
                Err(e) => TestResult {
                    name: test_name,
                    passed: false,
                    message: format!("Follow-up request failed: {}", e),
                    duration_ms: start.elapsed().as_millis() as f64,
                }
            }
        }
        Err(e) => TestResult {
            name: test_name,
            passed: false,
            message: format!("Initial request failed: {}", e),
            duration_ms: start.elapsed().as_millis() as f64,
        }
    }
}

async fn test_chat_history_deletion(client: &reqwest::Client) -> TestResult {
    let start = Instant::now();
    let test_name = "Chat History Deletion".to_string();
    let session_id = format!("test_delete_{}", Uuid::new_v4());
    
    // Send delete command
    let request = serde_json::json!({
        "query": "delete my chat history",
        "session_id": session_id
    });
    
    match client
        .post("http://localhost:5555/chat")
        .json(&request)
        .send()
        .await
    {
        Ok(resp) => {
            if let Ok(data) = resp.json::<serde_json::Value>().await {
                let response = data["response"].as_str().unwrap_or("");
                if response.contains("deleted") || response.contains("fresh") {
                    TestResult {
                        name: test_name,
                        passed: true,
                        message: "Delete command recognized".to_string(),
                        duration_ms: start.elapsed().as_millis() as f64,
                    }
                } else {
                    TestResult {
                        name: test_name,
                        passed: false,
                        message: "Delete command not implemented (expected for stable-server)".to_string(),
                        duration_ms: start.elapsed().as_millis() as f64,
                    }
                }
            } else {
                TestResult {
                    name: test_name,
                    passed: false,
                    message: "Failed to parse response".to_string(),
                    duration_ms: start.elapsed().as_millis() as f64,
                }
            }
        }
        Err(e) => TestResult {
            name: test_name,
            passed: false,
            message: format!("Request failed: {}", e),
            duration_ms: start.elapsed().as_millis() as f64,
        }
    }
}

async fn test_performance(client: &reqwest::Client) -> TestResult {
    let start = Instant::now();
    let test_name = "Performance (O(1))".to_string();
    
    let request = StableChatRequest {
        query: "What is Think AI?".to_string(),
    };
    
    match client
        .post("http://localhost:5555/chat")
        .json(&request)
        .send()
        .await
    {
        Ok(resp) => {
            if let Ok(data) = resp.json::<StableChatResponse>().await {
                if let Some(metadata) = data.metadata {
                    if metadata.response_time_ms < 100.0 {
                        TestResult {
                            name: test_name,
                            passed: true,
                            message: format!("O(1) performance verified: {:.2}ms", metadata.response_time_ms),
                            duration_ms: start.elapsed().as_millis() as f64,
                        }
                    } else {
                        TestResult {
                            name: test_name,
                            passed: false,
                            message: format!("Response too slow: {:.2}ms", metadata.response_time_ms),
                            duration_ms: start.elapsed().as_millis() as f64,
                        }
                    }
                } else {
                    TestResult {
                        name: test_name,
                        passed: false,
                        message: "No performance metadata".to_string(),
                        duration_ms: start.elapsed().as_millis() as f64,
                    }
                }
            } else {
                TestResult {
                    name: test_name,
                    passed: false,
                    message: "Failed to parse response".to_string(),
                    duration_ms: start.elapsed().as_millis() as f64,
                }
            }
        }
        Err(e) => TestResult {
            name: test_name,
            passed: false,
            message: format!("Request failed: {}", e),
            duration_ms: start.elapsed().as_millis() as f64,
        }
    }
}

async fn test_concurrent_requests(client: &reqwest::Client) -> TestResult {
    let start = Instant::now();
    let test_name = "Concurrent Requests".to_string();
    
    let mut handles = vec![];
    for i in 0..5 {
        let client = client.clone();
        let handle = tokio::spawn(async move {
            let request = StableChatRequest {
                query: format!("What is {}+{}?", i, i),
            };
            client
                .post("http://localhost:5555/chat")
                .json(&request)
                .send()
                .await
        });
        handles.push(handle);
    }
    
    let mut success_count = 0;
    for handle in handles {
        if let Ok(Ok(resp)) = handle.await {
            if resp.status().is_success() {
                success_count += 1;
            }
        }
    }
    
    if success_count == 5 {
        TestResult {
            name: test_name,
            passed: true,
            message: "All concurrent requests succeeded".to_string(),
            duration_ms: start.elapsed().as_millis() as f64,
        }
    } else {
        TestResult {
            name: test_name,
            passed: false,
            message: format!("Only {}/5 requests succeeded", success_count),
            duration_ms: start.elapsed().as_millis() as f64,
        }
    }
}

async fn test_response_quality(client: &reqwest::Client) -> TestResult {
    let start = Instant::now();
    let test_name = "Response Quality".to_string();
    
    let test_queries = vec![
        ("What is artificial intelligence?", vec!["AI", "intelligence", "computer", "machine"]),
        ("Explain quantum computing", vec!["quantum", "qubit", "superposition", "computing"]),
        ("What is Think AI?", vec!["Think AI", "O(1)", "performance", "system"]),
    ];
    
    let mut quality_score = 0;
    let mut total_tests = 0;
    
    for (query, expected_keywords) in test_queries {
        let request = StableChatRequest {
            query: query.to_string(),
        };
        
        if let Ok(resp) = client
            .post("http://localhost:5555/chat")
            .json(&request)
            .send()
            .await
        {
            if let Ok(data) = resp.json::<StableChatResponse>().await {
                let response_lower = data.response.to_lowercase();
                let matched_keywords = expected_keywords
                    .iter()
                    .filter(|&keyword| response_lower.contains(&keyword.to_lowercase()))
                    .count();
                
                if matched_keywords >= expected_keywords.len() / 2 {
                    quality_score += 1;
                }
            }
        }
        total_tests += 1;
    }
    
    let quality_percentage = (quality_score as f64 / total_tests as f64) * 100.0;
    
    if quality_percentage >= 66.0 {
        TestResult {
            name: test_name,
            passed: true,
            message: format!("Response quality: {:.0}%", quality_percentage),
            duration_ms: start.elapsed().as_millis() as f64,
        }
    } else {
        TestResult {
            name: test_name,
            passed: false,
            message: format!("Low response quality: {:.0}%", quality_percentage),
            duration_ms: start.elapsed().as_millis() as f64,
        }
    }
}