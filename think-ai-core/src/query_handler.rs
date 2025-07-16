use anyhow::{anyhow, Result};
use futures::stream::{Stream, StreamExt};
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use std::time::Duration;
use tokio::sync::{mpsc, Semaphore};
use tokio::time::timeout;

mod gpu_detector;
pub use gpu_detector::{get_gpu_info, DeviceType, GpuInfo};

/// Maximum concurrent queries to prevent resource exhaustion
const MAX_CONCURRENT_QUERIES: usize = 10;

/// Maximum token limit per query (50k tokens)
const MAX_TOKENS_PER_QUERY: usize = 50000;

/// Query timeout in seconds
const QUERY_TIMEOUT_SECS: u64 = 300; // 5 minutes for massive queries

/// Chunk size for streaming responses
const STREAM_CHUNK_SIZE: usize = 1000; // tokens

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QueryRequest {
    pub prompt: String,
    pub max_tokens: Option<usize>,
    pub stream: bool,
    pub temperature: Option<f32>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QueryResponse {
    pub text: String,
    pub tokens_used: usize,
    pub truncated: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StreamChunk {
    pub text: String,
    pub is_final: bool,
    pub tokens_so_far: usize,
}

pub struct O1QueryHandler {
    semaphore: Arc<Semaphore>,
    max_tokens: usize,
    device: String,
    gpu_available: bool,
}

impl Default for O1QueryHandler {
    fn default() -> Self {
        Self::new()
    }
}

impl O1QueryHandler {
    pub fn new() -> Self {
        let gpu_info = get_gpu_info();
        let device = gpu_info.device_type.to_torch_device().to_string();

        println!(
            "🚀 Query Handler initialized with device: {} ({})",
            device, gpu_info.device_name
        );

        if gpu_info.available {
            println!(
                "✅ GPU detected: {} with {}MB memory",
                gpu_info.device_name, gpu_info.memory_mb
            );
            if let Some(cuda_ver) = &gpu_info.cuda_version {
                println!("   CUDA version: {}", cuda_ver);
            }
        } else {
            println!("⚠️  No GPU detected, using CPU for inference");
        }

        Self {
            semaphore: Arc::new(Semaphore::new(MAX_CONCURRENT_QUERIES)),
            max_tokens: MAX_TOKENS_PER_QUERY,
            device,
            gpu_available: gpu_info.available,
        }
    }

    /// Handle a query with proper timeout and resource protection
    pub async fn handle_query(&self, request: QueryRequest) -> Result<QueryResponse> {
        // Acquire semaphore to limit concurrent queries
        let _permit = self.semaphore.acquire().await?;

        // Validate and cap max_tokens
        let max_tokens = request
            .max_tokens
            .unwrap_or(self.max_tokens)
            .min(self.max_tokens);

        // Apply timeout to prevent hanging
        let result = timeout(
            Duration::from_secs(QUERY_TIMEOUT_SECS),
            self.process_query_internal(request.prompt, max_tokens),
        )
        .await;

        match result {
            Ok(Ok(response)) => Ok(response),
            Ok(Err(e)) => Err(e),
            Err(_) => Err(anyhow!(
                "Query timed out after {} seconds",
                QUERY_TIMEOUT_SECS
            )),
        }
    }

    /// Handle streaming query with backpressure and chunking
    pub async fn handle_streaming_query(
        &self,
        request: QueryRequest,
    ) -> Result<impl Stream<Item = Result<StreamChunk>>> {
        // Acquire semaphore
        let permit = Arc::new(self.semaphore.clone().acquire_owned().await?);

        let max_tokens = request
            .max_tokens
            .unwrap_or(self.max_tokens)
            .min(self.max_tokens);

        let (tx, rx) = mpsc::channel::<Result<StreamChunk>>(10); // Bounded channel for backpressure

        // Spawn background task to generate stream
        let prompt = request.prompt.clone();
        tokio::spawn(async move {
            let _permit = permit; // Keep permit alive for duration of stream

            match timeout(
                Duration::from_secs(QUERY_TIMEOUT_SECS),
                Self::generate_stream(prompt, max_tokens, tx.clone()),
            )
            .await
            {
                Ok(Ok(_)) => {}
                Ok(Err(e)) => {
                    let _ = tx.send(Err(e)).await;
                }
                Err(_) => {
                    let _ = tx.send(Err(anyhow!("Stream timed out"))).await;
                }
            }
        });

        Ok(tokio_stream::wrappers::ReceiverStream::new(rx))
    }

    /// Internal query processing with O(1) token counting
    async fn process_query_internal(
        &self,
        prompt: String,
        max_tokens: usize,
    ) -> Result<QueryResponse> {
        // Estimate prompt tokens (O(1) approximation)
        let prompt_tokens = Self::estimate_tokens(&prompt);

        if prompt_tokens > max_tokens {
            return Ok(QueryResponse {
                text: "Error: Prompt exceeds maximum token limit".to_string(),
                tokens_used: prompt_tokens,
                truncated: true,
            });
        }

        // Simulate model generation (replace with actual model call)
        let response_text = self
            .generate_response(&prompt, max_tokens - prompt_tokens)
            .await?;
        let total_tokens = prompt_tokens + Self::estimate_tokens(&response_text);

        Ok(QueryResponse {
            text: response_text,
            tokens_used: total_tokens,
            truncated: false,
        })
    }

    /// Generate streaming response with chunking
    async fn generate_stream(
        prompt: String,
        max_tokens: usize,
        tx: mpsc::Sender<Result<StreamChunk>>,
    ) -> Result<()> {
        let prompt_tokens = Self::estimate_tokens(&prompt);
        let mut tokens_generated = 0;

        // Simulate streaming generation (replace with actual model)
        let words: Vec<&str> = "This is a simulated streaming response that demonstrates chunking and token counting for massive queries without hanging.".split_whitespace().collect();

        for (i, word) in words.iter().enumerate() {
            let word_tokens = Self::estimate_tokens(word);

            if tokens_generated + word_tokens > max_tokens - prompt_tokens {
                // Send final chunk indicating truncation
                let _ = tx
                    .send(Ok(StreamChunk {
                        text: " [TRUNCATED]".to_string(),
                        is_final: true,
                        tokens_so_far: tokens_generated + prompt_tokens,
                    }))
                    .await;
                break;
            }

            tokens_generated += word_tokens;

            let chunk = StreamChunk {
                text: format!("{} ", word),
                is_final: i == words.len() - 1,
                tokens_so_far: tokens_generated + prompt_tokens,
            };

            if tx.send(Ok(chunk)).await.is_err() {
                // Client disconnected
                break;
            }

            // Small delay to simulate generation
            tokio::time::sleep(Duration::from_millis(10)).await;
        }

        Ok(())
    }

    /// O(1) token estimation (4 chars ≈ 1 token)
    fn estimate_tokens(text: &str) -> usize {
        (text.len() + 3) / 4
    }

    /// Generate response using GPU when available
    async fn generate_response(&self, prompt: &str, max_tokens: usize) -> Result<String> {
        // In production, this would initialize the model with the detected device
        // For example with candle or torch bindings:
        // let model = Model::load(&self.device)?;

        let device_info = if self.gpu_available {
            "🚀 GPU-accelerated".to_string()
        } else {
            "💻 CPU-based".to_string()
        };

        // Simulate faster generation on GPU
        let generation_time = if self.gpu_available {
            Duration::from_millis(10) // GPU is ~10x faster
        } else {
            Duration::from_millis(100)
        };

        tokio::time::sleep(generation_time).await;

        Ok(format!(
            "Generated response with up to {} tokens using {} inference on device: {}",
            max_tokens, device_info, self.device
        ))
    }

    /// Get device info for monitoring
    pub fn get_device_info(&self) -> (String, bool) {
        (self.device.clone(), self.gpu_available)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use futures::StreamExt;

    #[tokio::test]
    async fn test_query_handler_basic() {
        let handler = O1QueryHandler::new();
        let request = QueryRequest {
            prompt: "Test prompt".to_string(),
            max_tokens: Some(100),
            stream: false,
            temperature: None,
        };

        let response = handler.handle_query(request).await.unwrap();
        assert!(!response.truncated);
        assert!(response.tokens_used > 0);
    }

    #[tokio::test]
    async fn test_query_handler_max_tokens() {
        let handler = O1QueryHandler::new();
        let request = QueryRequest {
            prompt: "Test".to_string(),
            max_tokens: Some(100000), // Over limit
            stream: false,
            temperature: None,
        };

        let response = handler.handle_query(request).await.unwrap();
        assert!(response.tokens_used <= MAX_TOKENS_PER_QUERY);
    }

    #[tokio::test]
    async fn test_streaming_query() {
        let handler = O1QueryHandler::new();
        let request = QueryRequest {
            prompt: "Test streaming".to_string(),
            max_tokens: Some(1000),
            stream: true,
            temperature: None,
        };

        let mut stream = handler.handle_streaming_query(request).await.unwrap();
        let mut total_chunks = 0;

        while let Some(chunk_result) = stream.next().await {
            let chunk = chunk_result.unwrap();
            total_chunks += 1;

            if chunk.is_final {
                break;
            }
        }

        assert!(total_chunks > 0);
    }

    #[tokio::test]
    async fn test_concurrent_queries() {
        let handler = Arc::new(O1QueryHandler::new());
        let mut handles = vec![];

        // Launch multiple concurrent queries
        for i in 0..15 {
            let handler_clone = handler.clone();
            let handle = tokio::spawn(async move {
                let request = QueryRequest {
                    prompt: format!("Test query {}", i),
                    max_tokens: Some(1000),
                    stream: false,
                    temperature: None,
                };
                handler_clone.handle_query(request).await
            });
            handles.push(handle);
        }

        // Wait for all to complete
        let results: Vec<_> = futures::future::join_all(handles).await;

        // Should all succeed despite concurrency limit
        for result in results {
            assert!(result.is_ok());
            assert!(result.unwrap().is_ok());
        }
    }
}
