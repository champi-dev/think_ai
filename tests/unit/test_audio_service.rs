use think_ai_full_production::audio_service::{AudioService, TranscriptionResult};
use mockall::mock;
use mockall::predicate::*;

#[cfg(test)]
mod tests {
    use super::*;
    
    mock! {
        AudioClient {
            async fn transcribe(&self, audio_data: Vec<u8>) -> Result<String, String>;
            async fn synthesize(&self, text: &str) -> Result<Vec<u8>, String>;
        }
    }

    #[tokio::test]
    async fn test_audio_transcription_success() {
        let mut mock_client = MockAudioClient::new();
        mock_client
            .expect_transcribe()
            .with(eq(vec![1, 2, 3, 4]))
            .times(1)
            .returning(|_| Ok("Hello, world!".to_string()));
        
        let service = AudioService::with_client(Box::new(mock_client));
        let result = service.transcribe(vec![1, 2, 3, 4]).await;
        
        assert!(result.is_ok());
        assert_eq!(result.unwrap().text, "Hello, world!");
    }

    #[tokio::test]
    async fn test_audio_transcription_empty_audio() {
        let service = AudioService::new();
        let result = service.transcribe(vec![]).await;
        
        assert!(result.is_err());
        assert!(result.unwrap_err().contains("empty"));
    }

    #[tokio::test]
    async fn test_audio_synthesis_success() {
        let mut mock_client = MockAudioClient::new();
        mock_client
            .expect_synthesize()
            .with(eq("Hello, world!"))
            .times(1)
            .returning(|_| Ok(vec![5, 6, 7, 8]));
        
        let service = AudioService::with_client(Box::new(mock_client));
        let result = service.synthesize("Hello, world!").await;
        
        assert!(result.is_ok());
        assert_eq!(result.unwrap(), vec![5, 6, 7, 8]);
    }

    #[tokio::test]
    async fn test_audio_synthesis_empty_text() {
        let service = AudioService::new();
        let result = service.synthesize("").await;
        
        assert!(result.is_err());
    }

    #[tokio::test]
    async fn test_audio_caching() {
        let service = AudioService::new();
        
        // First call should cache
        let text = "Cacheable text";
        let result1 = service.synthesize_with_cache(text).await;
        assert!(result1.is_ok());
        
        // Second call should use cache (faster)
        let start = std::time::Instant::now();
        let result2 = service.synthesize_with_cache(text).await;
        let duration = start.elapsed();
        
        assert!(result2.is_ok());
        assert!(duration.as_millis() < 10); // Should be very fast from cache
        assert_eq!(result1.unwrap(), result2.unwrap());
    }

    #[tokio::test]
    async fn test_audio_format_validation() {
        let service = AudioService::new();
        
        // Test WAV format
        let wav_header = vec![0x52, 0x49, 0x46, 0x46]; // RIFF
        assert!(service.is_valid_audio_format(&wav_header, "wav"));
        
        // Test MP3 format
        let mp3_header = vec![0xFF, 0xFB];
        assert!(service.is_valid_audio_format(&mp3_header, "mp3"));
        
        // Test invalid format
        let invalid = vec![0x00, 0x00];
        assert!(!service.is_valid_audio_format(&invalid, "mp3"));
    }

    #[tokio::test]
    async fn test_concurrent_audio_requests() {
        let service = AudioService::new();
        let service = std::sync::Arc::new(service);
        
        let mut handles = vec![];
        
        for i in 0..5 {
            let service_clone = service.clone();
            let handle = tokio::spawn(async move {
                let text = format!("Concurrent request {}", i);
                let result = service_clone.synthesize(&text).await;
                assert!(result.is_ok());
            });
            handles.push(handle);
        }
        
        for handle in handles {
            handle.await.unwrap();
        }
    }
}