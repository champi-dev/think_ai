use anyhow::Result;
use bytes::Bytes;
use reqwest::Client;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::path::PathBuf;
use std::sync::Arc;
use tokio::fs;
use tokio::sync::RwLock;
use tracing::{error, info};

#[derive(Clone)]
pub struct AudioService {
    deepgram_api_key: String,
    elevenlabs_api_key: String,
    cache_dir: PathBuf,
    cache: Arc<RwLock<HashMap<String, String>>>, // hash -> file_path
    client: Client,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct TranscriptionResult {
    pub text: String,
    pub confidence: f32,
    pub duration: f32,
    pub language: Option<String>,
    pub processing_time_ms: f64,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct SynthesisRequest {
    pub text: String,
    pub voice_id: Option<String>, // ElevenLabs voice ID
    pub model_id: Option<String>, // Use "eleven_turbo_v2" for fastest
    pub language: Option<String>, // Language code for multilingual synthesis
}

impl AudioService {
    pub fn new(deepgram_api_key: String, elevenlabs_api_key: String, cache_dir: PathBuf) -> Self {
        Self {
            deepgram_api_key,
            elevenlabs_api_key,
            cache_dir,
            cache: Arc::new(RwLock::new(HashMap::new())),
            client: Client::new(),
        }
    }

    /// Initialize the audio service and create cache directory
    pub async fn init(&self) -> Result<()> {
        // Create cache directory if it doesn't exist
        fs::create_dir_all(&self.cache_dir).await?;

        // Load existing cache entries
        self.load_cache().await?;

        info!(
            "Audio service initialized with cache at {:?}",
            self.cache_dir
        );
        Ok(())
    }

    /// Load cached audio files
    async fn load_cache(&self) -> Result<()> {
        let mut cache = self.cache.write().await;

        let mut entries = fs::read_dir(&self.cache_dir).await?;
        while let Some(entry) = entries.next_entry().await? {
            if let Some(file_name) = entry.file_name().to_str() {
                if file_name.ends_with(".mp3") || file_name.ends_with(".wav") {
                    let hash = file_name.trim_end_matches(".mp3").trim_end_matches(".wav");
                    cache.insert(hash.to_string(), entry.path().to_string_lossy().to_string());
                }
            }
        }

        info!("Loaded {} cached audio files", cache.len());
        Ok(())
    }

    /// Transcribe audio using Deepgram
    pub async fn transcribe(
        &self,
        audio_data: Bytes,
        mime_type: &str,
        language: Option<String>,
    ) -> Result<TranscriptionResult> {
        // Use multilingual mode for automatic language detection and code-switching support
        let mut url =
            "https://api.deepgram.com/v1/listen?model=nova-2&smart_format=true&language=multi"
                .to_string();

        // Only override with specific language if explicitly requested
        if let Some(ref lang) = language {
            if lang != "auto" && lang != "multi" {
                // Map our language codes to Deepgram's language codes
                let deepgram_lang = match lang.as_str() {
                    "zh" => "zh-CN",
                    "pt" => "pt-BR",
                    "en" => "en-US",
                    _ => &lang, // Use as-is for other languages
                };
                // Replace multi with specific language
                url = format!(
                    "https://api.deepgram.com/v1/listen?model=nova-2&smart_format=true&language={}",
                    deepgram_lang
                );
            }
        }

        let response = self
            .client
            .post(url)
            .header("Authorization", format!("Token {}", self.deepgram_api_key))
            .header("Content-Type", mime_type)
            .body(audio_data)
            .send()
            .await?;

        if !response.status().is_success() {
            let error_text = response.text().await?;
            error!("Deepgram API error: {}", error_text);
            anyhow::bail!("Deepgram API error: {}", error_text);
        }

        let deepgram_response: DeepgramResponse = response.json().await?;

        // Extract the best alternative
        let transcript = deepgram_response
            .results
            .channels
            .first()
            .and_then(|c| c.alternatives.first())
            .map(|a| a.transcript.clone())
            .unwrap_or_default();

        let confidence = deepgram_response
            .results
            .channels
            .first()
            .and_then(|c| c.alternatives.first())
            .map(|a| a.confidence)
            .unwrap_or(0.0);

        let duration = deepgram_response.metadata.duration.unwrap_or(0.0);

        Ok(TranscriptionResult {
            text: transcript,
            confidence,
            duration,
            language: language,
            processing_time_ms: 0.0, // TODO: Add actual timing
        })
    }

    /// Synthesize speech using ElevenLabs
    pub async fn synthesize(&self, request: SynthesisRequest) -> Result<(Bytes, String)> {
        // Generate cache key
        let cache_key = self.generate_cache_key(&request.text);

        // Check cache first
        if let Some(cached_path) = self.get_cached(&cache_key).await {
            info!("Using cached audio for text hash: {}", cache_key);
            let audio_data = fs::read(&cached_path).await?;
            return Ok((Bytes::from(audio_data), cache_key));
        }

        // Select voice based on language, using multilingual voices
        let voice_id = request.voice_id.unwrap_or_else(|| {
            match request.language.as_deref() {
                Some("es") | Some("fr") | Some("de") | Some("it") | Some("pt") | Some("pl")
                | Some("tr") | Some("ru") | Some("nl") | Some("cs") | Some("ar") | Some("zh")
                | Some("ja") | Some("ko") | Some("hi") => {
                    "XB0fDUnXU5powFXDhCwa".to_string() // Charlotte - multilingual voice
                }
                _ => "21m00Tcm4TlvDq8ikWAM".to_string(), // Rachel - English voice
            }
        });

        let model_id = request
            .model_id
            .unwrap_or_else(|| "eleven_turbo_v2_5".to_string()); // Latest multilingual model

        let url = format!("https://api.elevenlabs.io/v1/text-to-speech/{}", voice_id);

        let payload = serde_json::json!({
            "text": request.text,
            "model_id": model_id,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5,
                "style": 0.0,
                "use_speaker_boost": true
            }
        });

        let response = self
            .client
            .post(&url)
            .header("xi-api-key", &self.elevenlabs_api_key)
            .header("Content-Type", "application/json")
            .json(&payload)
            .send()
            .await?;

        if !response.status().is_success() {
            let error_text = response.text().await?;
            error!("ElevenLabs API error: {}", error_text);
            anyhow::bail!("ElevenLabs API error: {}", error_text);
        }

        let audio_data = response.bytes().await?;

        // Cache the audio
        self.cache_audio(&cache_key, &audio_data).await?;

        Ok((audio_data, cache_key))
    }

    /// Generate a cache key for text
    fn generate_cache_key(&self, text: &str) -> String {
        use sha2::{Digest, Sha256};
        let mut hasher = Sha256::new();
        hasher.update(text.as_bytes());
        format!("{:x}", hasher.finalize())
    }

    /// Get cached audio file path
    async fn get_cached(&self, cache_key: &str) -> Option<String> {
        let cache = self.cache.read().await;
        cache.get(cache_key).cloned()
    }

    /// Cache audio data
    async fn cache_audio(&self, cache_key: &str, audio_data: &Bytes) -> Result<()> {
        let file_name = format!("{}.mp3", cache_key);
        let file_path = self.cache_dir.join(&file_name);

        fs::write(&file_path, audio_data).await?;

        let mut cache = self.cache.write().await;
        cache.insert(
            cache_key.to_string(),
            file_path.to_string_lossy().to_string(),
        );

        info!("Cached audio file: {}", file_name);
        Ok(())
    }

    /// Clean up old cache entries (optional)
    pub async fn cleanup_cache(&self, max_entries: usize) -> Result<()> {
        let cache = self.cache.read().await;
        if cache.len() <= max_entries {
            return Ok(());
        }

        // This is a simple implementation - you might want to use LRU or timestamp-based cleanup
        let to_remove = cache.len() - max_entries;
        let mut cache = self.cache.write().await;

        let keys_to_remove: Vec<String> = cache.keys().take(to_remove).cloned().collect();
        for key in keys_to_remove {
            if let Some(path) = cache.remove(&key) {
                let _ = fs::remove_file(&path).await;
            }
        }

        Ok(())
    }
}

// Deepgram response structures
#[derive(Debug, Deserialize)]
struct DeepgramResponse {
    metadata: DeepgramMetadata,
    results: DeepgramResults,
}

#[derive(Debug, Deserialize)]
struct DeepgramMetadata {
    duration: Option<f32>,
}

#[derive(Debug, Deserialize)]
struct DeepgramResults {
    channels: Vec<DeepgramChannel>,
}

#[derive(Debug, Deserialize)]
struct DeepgramChannel {
    alternatives: Vec<DeepgramAlternative>,
}

#[derive(Debug, Deserialize)]
struct DeepgramAlternative {
    transcript: String,
    confidence: f32,
}

#[cfg(test)]
mod tests {
    use super::*;
    use mockito::{mock, Matcher};

    #[tokio::test]
    async fn test_transcribe_with_multilingual_mode() {
        let _m = mock("POST", "/v1/listen")
            .match_query(Matcher::AllOf(vec![
                Matcher::UrlEncoded("model".into(), "nova-2".into()),
                Matcher::UrlEncoded("smart_format".into(), "true".into()),
                Matcher::UrlEncoded("language".into(), "multi".into()),
            ]))
            .with_header("content-type", "application/json")
            .with_body(
                r#"{
                "metadata": { "duration": 3.5 },
                "results": {
                    "channels": [{
                        "alternatives": [{
                            "transcript": "Hello, hola, 你好",
                            "confidence": 0.95
                        }]
                    }]
                }
            }"#,
            )
            .create();

        let temp_dir = tempfile::TempDir::new().unwrap();
        let audio_service = AudioService::new(
            "test_deepgram_key".to_string(),
            "test_elevenlabs_key".to_string(),
            temp_dir.path().to_path_buf(),
        );

        let audio_data = Bytes::from("fake audio data");
        let result = audio_service
            .transcribe(audio_data, "audio/webm", None)
            .await
            .unwrap();

        assert_eq!(result.text, "Hello, hola, 你好");
        assert_eq!(result.confidence, 0.95);
    }

    #[tokio::test]
    async fn test_transcribe_with_auto_language() {
        let _m = mock("POST", "/v1/listen")
            .match_query(Matcher::AllOf(vec![
                Matcher::UrlEncoded("model".into(), "nova-2".into()),
                Matcher::UrlEncoded("smart_format".into(), "true".into()),
                Matcher::UrlEncoded("language".into(), "multi".into()),
            ]))
            .with_header("content-type", "application/json")
            .with_body(
                r#"{
                "metadata": { "duration": 4.0 },
                "results": {
                    "channels": [{
                        "alternatives": [{
                            "transcript": "Mixed languages detected",
                            "confidence": 0.92
                        }]
                    }]
                }
            }"#,
            )
            .create();

        let temp_dir = tempfile::TempDir::new().unwrap();
        let audio_service = AudioService::new(
            "test_deepgram_key".to_string(),
            "test_elevenlabs_key".to_string(),
            temp_dir.path().to_path_buf(),
        );

        let audio_data = Bytes::from("fake audio data");
        let result = audio_service
            .transcribe(audio_data, "audio/webm", Some("auto".to_string()))
            .await
            .unwrap();

        assert_eq!(result.text, "Mixed languages detected");
        assert_eq!(result.confidence, 0.92);
    }
}
