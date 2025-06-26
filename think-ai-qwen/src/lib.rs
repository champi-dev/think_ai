//! Qwen Integration for Think AI
//! Handles cache misses with external LLM calls

use anyhow::Result;
use serde::{Deserialize, Serialize};
use std::time::Duration;
use tracing::info;

/// Knowledge context for generating responses
#[derive(Debug, Clone)]
pub struct KnowledgeContext {
    pub domain: String,
    pub title: String,
    pub content: String,
}

#[derive(Debug, Clone)]
pub struct QwenClient {
    client: reqwest::Client,
    api_key: Option<String>,
    api_url: String,
    model_id: String,
}

#[derive(Serialize)]
struct QwenRequest {
    model: String,
    messages: Vec<Message>,
    temperature: f32,
    max_tokens: u32,
}

#[derive(Serialize)]
struct HuggingFaceRequest {
    inputs: String,
    parameters: HFParameters,
}

#[derive(Serialize)]
struct HFParameters {
    max_new_tokens: u32,
    temperature: f32,
    return_full_text: bool,
}

#[derive(Serialize, Deserialize)]
struct Message {
    role: String,
    content: String,
}

#[derive(Deserialize)]
struct QwenResponse {
    choices: Vec<Choice>,
}

#[derive(Deserialize)]
struct Choice {
    message: Message,
}

#[derive(Deserialize)]
struct HuggingFaceResponse {
    generated_text: String,
}

impl QwenClient {
    pub fn new() -> Self {
        println!("Initializing Qwen client...");
        let client = reqwest::Client::builder()
            .timeout(Duration::from_secs(5))
            .build()
            .expect("Failed to create HTTP client");
        println!("HTTP client created");
        
        // Check for Hugging Face API key first, then Qwen
        let api_key = std::env::var("HUGGINGFACE_API_KEY")
            .or_else(|_| std::env::var("HF_API_KEY"))
            .or_else(|_| std::env::var("QWEN_API_KEY"))
            .ok();
        
        if api_key.is_some() {
            info!("API key configured for intelligent responses");
        } else {
            info!("No API key found - will use offline responses");
        }
        
        // Use Hugging Face inference API if HF key is available
        let (api_url, model_id) = if api_key.as_ref().map(|k| k.starts_with("hf_")).unwrap_or(false) {
            // Use a smaller, faster model for better performance
            let model = std::env::var("HF_MODEL")
                .unwrap_or_else(|_| "mistralai/Mixtral-8x7B-Instruct-v0.1".to_string());
            (
                format!("https://api-inference.huggingface.co/models/{}", model),
                model
            )
        } else {
            (
                std::env::var("QWEN_API_URL")
                    .unwrap_or_else(|_| "https://api.qwen.ai/v1/chat/completions".to_string()),
                "qwen-turbo".to_string()
            )
        };
        
        Self {
            client,
            api_key,
            api_url,
            model_id,
        }
    }
    
    pub async fn generate_response_with_context(&self, query: &str, knowledge_pieces: &[KnowledgeContext]) -> Result<String> {
        info!("Generating response with {} knowledge pieces", knowledge_pieces.len());
        
        // If no API key, return a helpful response
        if self.api_key.is_none() {
            return Ok(self.generate_context_aware_offline_response(query, knowledge_pieces));
        }
        
        let api_key = self.api_key.as_ref().unwrap();
        
        // Build context from knowledge pieces
        let mut context = String::new();
        if !knowledge_pieces.is_empty() {
            context.push_str("\n\nRelevant knowledge from Think AI's database:\n");
            for (i, node) in knowledge_pieces.iter().take(3).enumerate() {
                context.push_str(&format!("{}. [{}] {}: {}\n", 
                    i + 1, 
                    node.domain.to_lowercase(),
                    node.title, 
                    &node.content[..node.content.len().min(200)]
                ));
            }
        }
        
        // Use Hugging Face API if it's an HF key
        if api_key.starts_with("hf_") {
            return self.generate_huggingface_response_with_context(query, &context).await;
        }
        
        // Otherwise use Qwen API with context
        self.generate_qwen_response_with_context(query, &context).await
    }
    
    pub async fn generate_response(&self, query: &str) -> Result<String> {
        info!("Handling cache miss for query: {}", query);
        
        // If no API key, return a helpful response
        if self.api_key.is_none() {
            return Ok(self.generate_offline_response(query));
        }
        
        let api_key = self.api_key.as_ref().unwrap();
        
        // Use Hugging Face API if it's an HF key
        if api_key.starts_with("hf_") {
            return self.generate_huggingface_response(query).await;
        }
        
        // Otherwise use Qwen API
        let request = QwenRequest {
            model: self.model_id.clone(),
            messages: vec![
                Message {
                    role: "system".to_string(),
                    content: "You are Think AI, a helpful assistant with expertise in science, programming, mathematics, and philosophy. Provide direct, comprehensive answers.".to_string(),
                },
                Message {
                    role: "user".to_string(),
                    content: query.to_string(),
                },
            ],
            temperature: 0.7,
            max_tokens: 500,
        };
        
        let response = self.client
            .post(&self.api_url)
            .header("Authorization", format!("Bearer {}", api_key))
            .json(&request)
            .send()
            .await?;
        
        if response.status().is_success() {
            let qwen_response: QwenResponse = response.json().await?;
            if let Some(choice) = qwen_response.choices.first() {
                return Ok(choice.message.content.clone());
            }
        }
        
        // Fallback to offline response
        Ok(self.generate_offline_response(query))
    }
    
    async fn generate_huggingface_response(&self, query: &str) -> Result<String> {
        let prompt = format!(
            "You are Think AI, a helpful assistant. User asks: {}\n\nProvide a direct, comprehensive answer:",
            query
        );
        
        let request = HuggingFaceRequest {
            inputs: prompt,
            parameters: HFParameters {
                max_new_tokens: 500,
                temperature: 0.7,
                return_full_text: false,
            },
        };
        
        let response = self.client
            .post(&self.api_url)
            .header("Authorization", format!("Bearer {}", self.api_key.as_ref().unwrap()))
            .json(&request)
            .send()
            .await?;
        
        if response.status().is_success() {
            let text = response.text().await?;
            // Try to parse as array first (HF sometimes returns array)
            if let Ok(responses) = serde_json::from_str::<Vec<HuggingFaceResponse>>(&text) {
                if let Some(first) = responses.first() {
                    return Ok(first.generated_text.clone());
                }
            }
            // Otherwise try as single response
            if let Ok(hf_response) = serde_json::from_str::<HuggingFaceResponse>(&text) {
                return Ok(hf_response.generated_text);
            }
        }
        
        // Fallback to offline response
        Ok(self.generate_offline_response(query))
    }
    
    async fn generate_huggingface_response_with_context(&self, query: &str, context: &str) -> Result<String> {
        let prompt = format!(
            "You are Think AI, an advanced AI assistant with a comprehensive knowledge base. 

{}

User asks: {}

Based on the knowledge above and your understanding, provide a relevant, useful, and actionable answer in a natural, conversational way. Be specific and comprehensive:",
            context, query
        );
        
        let request = HuggingFaceRequest {
            inputs: prompt,
            parameters: HFParameters {
                max_new_tokens: 500,
                temperature: 0.7,
                return_full_text: false,
            },
        };
        
        let response = self.client
            .post(&self.api_url)
            .header("Authorization", format!("Bearer {}", self.api_key.as_ref().unwrap()))
            .json(&request)
            .send()
            .await?;
        
        
        if response.status().is_success() {
            let text = response.text().await?;
            
            // Try to parse as array first (HF sometimes returns array)
            if let Ok(responses) = serde_json::from_str::<Vec<HuggingFaceResponse>>(&text) {
                if let Some(first) = responses.first() {
                    return Ok(first.generated_text.clone());
                }
            }
            // Otherwise try as single response
            if let Ok(hf_response) = serde_json::from_str::<HuggingFaceResponse>(&text) {
                return Ok(hf_response.generated_text);
            }
            
        } else if response.status() == 401 {
            eprintln!("⚠️  Invalid API key. Please check your HUGGINGFACE_API_KEY.");
        } else if response.status() == 404 {
            eprintln!("⚠️  Model not found or not available.");
        }
        
        // Fallback to context-aware offline response
        Ok(self.generate_context_aware_offline_response(query, &[]))
    }
    
    async fn generate_qwen_response_with_context(&self, query: &str, context: &str) -> Result<String> {
        let system_message = format!(
            "You are Think AI, an advanced AI assistant with a comprehensive knowledge base. {}

Analyze the user's question and the knowledge pieces provided. Synthesize a relevant, useful, and actionable answer that:
1. Directly addresses the user's question
2. Incorporates relevant information from the knowledge base
3. Provides specific, practical insights
4. Uses a natural, conversational tone",
            context
        );
        
        let request = QwenRequest {
            model: self.model_id.clone(),
            messages: vec![
                Message {
                    role: "system".to_string(),
                    content: system_message,
                },
                Message {
                    role: "user".to_string(),
                    content: query.to_string(),
                },
            ],
            temperature: 0.7,
            max_tokens: 500,
        };
        
        let response = self.client
            .post(&self.api_url)
            .header("Authorization", format!("Bearer {}", self.api_key.as_ref().unwrap()))
            .json(&request)
            .send()
            .await?;
        
        if response.status().is_success() {
            let qwen_response: QwenResponse = response.json().await?;
            if let Some(choice) = qwen_response.choices.first() {
                return Ok(choice.message.content.clone());
            }
        }
        
        // Fallback to context-aware offline response
        Ok(self.generate_context_aware_offline_response(query, &[]))
    }
    
    fn generate_context_aware_offline_response(&self, query: &str, knowledge_pieces: &[KnowledgeContext]) -> String {
        let query_lower = query.to_lowercase();
        
        // If we have relevant knowledge pieces, synthesize from them
        if !knowledge_pieces.is_empty() {
            let primary = &knowledge_pieces[0];
            let mut response = format!(
                "Based on Think AI's knowledge base: {}\n\n",
                primary.content
            );
            
            if knowledge_pieces.len() > 1 {
                response.push_str("Related information:\n");
                for node in knowledge_pieces.iter().skip(1).take(2) {
                    response.push_str(&format!("• {}: {}\n", 
                        node.title, 
                        &node.content[..node.content.len().min(150)]
                    ));
                }
            }
            
            return response;
        }
        
        // Otherwise use standard offline response
        self.generate_offline_response(query)
    }
    
    fn generate_offline_response(&self, query: &str) -> String {
        // Smart offline responses based on query patterns
        let query_lower = query.to_lowercase();
        
        if query_lower.contains("how") && query_lower.contains("work") {
            format!("To understand how {} works, we need to examine its fundamental principles and mechanisms. While I don't have specific details in my current knowledge base, the general approach involves analyzing its components, processes, and interactions. Would you like to explore a related topic I can help with?", 
                extract_topic(&query_lower))
        } else if query_lower.starts_with("what is") {
            let topic = query_lower.replace("what is", "").trim().to_string();
            format!("{} is a concept that would require detailed explanation. While I don't have specific information about it in my knowledge base, I can help with related topics in science, programming, mathematics, or philosophy. What specific aspect interests you?", topic)
        } else if query_lower.contains("why") {
            format!("That's an interesting question about causation and reasoning. While I don't have specific information about this in my knowledge base, understanding 'why' often involves examining causes, effects, and underlying principles. Can you provide more context or ask about a related topic?")
        } else {
            format!("I don't have specific information about '{}' in my knowledge base. However, I can help with topics in programming, science, mathematics, philosophy, and more. What else would you like to know?", query)
        }
    }
}

fn extract_topic(query: &str) -> &str {
    let words: Vec<&str> = query.split_whitespace().collect();
    if words.len() > 2 {
        // Skip common question words
        for word in words.iter() {
            if !matches!(*word, "how" | "what" | "why" | "when" | "where" | "who" | "does" | "do" | "is" | "are" | "can" | "will") {
                return word;
            }
        }
    }
    "this"
}

impl Default for QwenClient {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_offline_response_generation() {
        let client = QwenClient::new();
        
        let response = client.generate_offline_response("what is quantum computing");
        assert!(response.contains("quantum computing"));
        
        let response = client.generate_offline_response("how does photosynthesis work");
        assert!(response.contains("photosynthesis"));
        
        let response = client.generate_offline_response("why is the sky blue");
        assert!(response.contains("question about causation"));
    }
    
    #[test]
    fn test_extract_topic() {
        assert_eq!(extract_topic("how does photosynthesis work"), "photosynthesis");
        assert_eq!(extract_topic("what is gravity"), "gravity");
        assert_eq!(extract_topic("why is important"), "important");
    }
}