//! Leonardo AI API Client with O(1) Response Handling

use anyhow::{Result, anyhow};
use reqwest::{Client, header};
use serde::{Serialize, Deserialize};
use std::time::Duration;

/// Leonardo AI API client
pub struct LeonardoClient {
    client: Client,
    api_key: String,
    base_url: String,
}

#[derive(Debug, Serialize)]
struct GenerationRequest {
    prompt: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    negative_prompt: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    width: Option<u32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    height: Option<u32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    num_images: Option<u32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    guidance_scale: Option<f32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    model_id: Option<String>,
}

#[derive(Debug, Deserialize)]
struct GenerationResponse {
    generation_id: String,
    status: String,
}

#[derive(Debug, Deserialize)]
struct GenerationResult {
    generated_images: Vec<GeneratedImageData>,
}

#[derive(Debug, Deserialize)]
struct GeneratedImageData {
    url: String,
    width: u32,
    height: u32,
}

impl LeonardoClient {
    /// Create a new Leonardo AI client
    pub fn new(api_key: &str, base_url: &str) -> Self {
        let client = Client::builder()
            .timeout(Duration::from_secs(300)) // 5 minute timeout for image generation
            .build()
            .expect("Failed to create HTTP client");
        
        Self {
            client,
            api_key: api_key.to_string(),
            base_url: base_url.to_string(),
        }
    }
    
    /// Generate an image using Leonardo AI
    pub async fn generate_image(
        &self,
        prompt: &str,
        negative_prompt: Option<&str>,
        width: Option<u32>,
        height: Option<u32>,
        num_images: Option<u32>,
        guidance_scale: Option<f32>,
        model_id: Option<&str>,
    ) -> Result<(Vec<u8>, (u32, u32))> {
        // Step 1: Initiate generation
        let generation_id = self.initiate_generation(
            prompt,
            negative_prompt,
            width,
            height,
            num_images,
            guidance_scale,
            model_id,
        ).await?;
        
        // Step 2: Poll for completion (with exponential backoff)
        let result = self.poll_generation_status(&generation_id).await?;
        
        // Step 3: Download the generated image
        if let Some(image_data) = result.generated_images.first() {
            let image_bytes = self.download_image(&image_data.url).await?;
            Ok((image_bytes, (image_data.width, image_data.height)))
        } else {
            Err(anyhow!("No images generated"))
        }
    }
    
    async fn initiate_generation(
        &self,
        prompt: &str,
        negative_prompt: Option<&str>,
        width: Option<u32>,
        height: Option<u32>,
        num_images: Option<u32>,
        guidance_scale: Option<f32>,
        model_id: Option<&str>,
    ) -> Result<String> {
        let request = GenerationRequest {
            prompt: prompt.to_string(),
            negative_prompt: negative_prompt.map(|s| s.to_string()),
            width,
            height,
            num_images,
            guidance_scale,
            model_id: model_id.map(|s| s.to_string()),
        };
        
        let response = self.client
            .post(format!("{}/generations", self.base_url))
            .header(header::AUTHORIZATION, format!("Bearer {}", self.api_key))
            .header(header::CONTENT_TYPE, "application/json")
            .json(&request)
            .send()
            .await?;
        
        if !response.status().is_success() {
            let status = response.status();
            let error_body = response.text().await.unwrap_or_else(|_| "Unable to read error body".to_string());
            return Err(anyhow!("Failed to initiate generation: {} - {}", status, error_body));
        }
        
        let generation_response: GenerationResponse = response.json().await?;
        Ok(generation_response.generation_id)
    }
    
    async fn poll_generation_status(&self, generation_id: &str) -> Result<GenerationResult> {
        let mut attempts = 0;
        let max_attempts = 60; // 5 minutes with 5 second intervals
        
        loop {
            tokio::time::sleep(Duration::from_secs(5)).await;
            
            let response = self.client
                .get(format!("{}/generations/{}", self.base_url, generation_id))
                .header(header::AUTHORIZATION, format!("Bearer {}", self.api_key))
                .send()
                .await?;
            
            if !response.status().is_success() {
                return Err(anyhow!("Failed to check generation status: {}", response.status()));
            }
            
            let result: GenerationResult = response.json().await?;
            
            // Check if generation is complete
            if !result.generated_images.is_empty() {
                return Ok(result);
            }
            
            attempts += 1;
            if attempts >= max_attempts {
                return Err(anyhow!("Generation timed out after {} attempts", max_attempts));
            }
        }
    }
    
    async fn download_image(&self, url: &str) -> Result<Vec<u8>> {
        let response = self.client
            .get(url)
            .send()
            .await?;
        
        if !response.status().is_success() {
            return Err(anyhow!("Failed to download image: {}", response.status()));
        }
        
        Ok(response.bytes().await?.to_vec())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_client_creation() {
        let client = LeonardoClient::new("test_key", "https://api.test.com");
        assert_eq!(client.api_key, "test_key");
        assert_eq!(client.base_url, "https://api.test.com");
    }
}