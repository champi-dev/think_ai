use reqwest;
use serde_json::json;
use std::time::Duration;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🧪 Testing Ollama connection...");

    let client = reqwest::Client::builder()
        .timeout(Duration::from_secs(5))
        .build()?;

    // Test 1: Check if Ollama is running
    match client.get("http://localhost:11434/api/tags").send().await {
        Ok(res) => {
            println!("✅ Ollama is running!");
            let body = res.text().await?;
            println!("Models: {}", body);
        }
        Err(e) => {
            println!("❌ Ollama not reachable: {}", e);
            return Err(e.into());
        }
    }

    // Test 2: Try to generate with Qwen
    let request = json!({
        "model": "qwen2.5:1.5b",
        "prompt": "Say hello",
        "stream": false
    });

    match client
        .post("http://localhost:11434/api/generate")
        .json(&request)
        .send()
        .await
    {
        Ok(res) => {
            if res.status().is_success() {
                let body: serde_json::Value = res.json().await?;
                println!("✅ Qwen responded: {}", body["response"]);
            } else {
                println!("❌ Qwen error: {}", res.status());
            }
        }
        Err(e) => {
            println!("❌ Generation failed: {}", e);
        }
    }

    Ok(())
}
