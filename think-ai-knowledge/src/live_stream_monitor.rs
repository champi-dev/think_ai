// Live streaming data monitor
// Monitors public live streams for trending content and insights

use crate::realtime_knowledge_gatherer::{StreamPlatform, WebContent};
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::RwLock;

/// Live stream metadata
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LiveStreamData {
    pub platform: StreamPlatform,
    pub stream_id: String,
    pub title: String,
    pub channel: String,
    pub viewer_count: u32,
    pub category: String,
    pub tags: Vec<String>,
    pub language: String,
    pub started_at: DateTime<Utc>,
    pub thumbnail_url: Option<String>,
    pub is_live: bool,
}

/// Stream analytics
#[derive(Debug, Clone)]
pub struct StreamAnalytics {
    pub peak_viewers: u32,
    pub average_viewers: u32,
    pub chat_activity: f32, // Messages per minute
    pub engagement_rate: f32,
    pub trending_score: f32,
}

/// Live stream monitor
pub struct LiveStreamMonitor {
    _http_client: reqwest::Client,
    active_streams: Arc<RwLock<HashMap<String, LiveStreamData>>>,
    analytics: Arc<RwLock<HashMap<String, StreamAnalytics>>>,
}

impl Default for LiveStreamMonitor {
    fn default() -> Self {
        Self::new()
    }
}

impl LiveStreamMonitor {
    pub fn new() -> Self {
        let http_client = reqwest::Client::builder()
            .user_agent("ThinkAI/1.0 (Live Stream Monitor; Public Data)")
            .timeout(std::time::Duration::from_secs(30))
            .build()
            .unwrap();

        Self {
            _http_client: http_client,
            active_streams: Arc::new(RwLock::new(HashMap::new())),
            analytics: Arc::new(RwLock::new(HashMap::new())),
        }
    }

    /// Monitor trending live streams
    pub async fn monitor_trending_streams(&self) -> Vec<LiveStreamData> {
        let mut all_streams = Vec::new();

        // Simulate getting trending streams from various platforms
        // In real implementation, this would fetch from APIs

        // Example: Twitch-like platform
        let example_stream = LiveStreamData {
            platform: StreamPlatform::Twitch,
            stream_id: "123456".to_string(),
            title: "AI Development Stream".to_string(),
            channel: "TechStreamer".to_string(),
            viewer_count: 5000,
            category: "Science & Technology".to_string(),
            tags: vec![
                "AI".to_string(),
                "Programming".to_string(),
                "Rust".to_string(),
            ],
            language: "en".to_string(),
            started_at: Utc::now() - chrono::Duration::hours(2),
            thumbnail_url: Some("https://example.com/thumb.jpg".to_string()),
            is_live: true,
        };

        all_streams.push(example_stream.clone());

        // Update active streams
        let mut streams = self.active_streams.write().await;
        streams.insert(example_stream.stream_id.clone(), example_stream);

        all_streams
    }

    /// Analyze stream metrics
    pub async fn analyze_stream(&self, stream_id: &str) -> Option<StreamAnalytics> {
        let streams = self.active_streams.read().await;

        if let Some(stream) = streams.get(stream_id) {
            let analytics = StreamAnalytics {
                peak_viewers: stream.viewer_count,
                average_viewers: (stream.viewer_count as f32 * 0.85) as u32,
                chat_activity: 50.0,   // Messages per minute (simulated)
                engagement_rate: 0.75, // 75% engagement (simulated)
                trending_score: self.calculate_trending_score(stream),
            };

            // Store analytics
            let mut analytics_map = self.analytics.write().await;
            analytics_map.insert(stream_id.to_string(), analytics.clone());

            Some(analytics)
        } else {
            None
        }
    }

    /// Calculate trending score based on various factors
    fn calculate_trending_score(&self, stream: &LiveStreamData) -> f32 {
        let mut score = 0.0;

        // Viewer count factor
        score += (stream.viewer_count as f32 / 1000.0).min(10.0);

        // Duration factor (newer streams get boost)
        let duration_hours = Utc::now()
            .signed_duration_since(stream.started_at)
            .num_hours() as f32;
        if duration_hours < 1.0 {
            score += 2.0;
        }

        // Category relevance (tech streams get boost for AI system)
        if stream.category.to_lowercase().contains("tech")
            || stream.category.to_lowercase().contains("science")
        {
            score += 1.5;
        }

        // Tag relevance
        for tag in &stream.tags {
            if tag.to_lowercase().contains("ai") || tag.to_lowercase().contains("machine learning")
            {
                score += 1.0;
            }
        }

        score.min(10.0) // Cap at 10.0
    }

    /// Get top trending streams
    pub async fn get_top_streams(&self, limit: usize) -> Vec<LiveStreamData> {
        let streams = self.active_streams.read().await;
        let mut stream_list: Vec<LiveStreamData> = streams.values().cloned().collect();

        // Sort by viewer count
        stream_list.sort_by(|a, b| b.viewer_count.cmp(&a.viewer_count));

        stream_list.into_iter().take(limit).collect()
    }

    /// Convert stream data to WebContent
    pub fn stream_to_web_content(&self, stream: &LiveStreamData) -> WebContent {
        let mut metadata = HashMap::new();
        metadata.insert("platform".to_string(), format!("{:?}", stream.platform));
        metadata.insert("viewer_count".to_string(), stream.viewer_count.to_string());
        metadata.insert("category".to_string(), stream.category.clone());
        metadata.insert("language".to_string(), stream.language.clone());

        if !stream.tags.is_empty() {
            metadata.insert("tags".to_string(), stream.tags.join(", "));
        }

        WebContent {
            source_id: format!("{:?}", stream.platform),
            url: format!("https://platform.com/stream/{}", stream.stream_id),
            title: stream.title.clone(),
            content: format!("{} streaming in {}", stream.channel, stream.category),
            author: Some(stream.channel.clone()),
            published_date: Some(stream.started_at),
            gathered_at: Utc::now(),
            metadata,
        }
    }

    /// Clean up inactive streams
    pub async fn cleanup_inactive_streams(&self) {
        let mut streams = self.active_streams.write().await;
        let mut analytics = self.analytics.write().await;

        // Remove streams that are no longer live
        let inactive_ids: Vec<String> = streams
            .iter()
            .filter(|(_, stream)| !stream.is_live)
            .map(|(id, _)| id.clone())
            .collect();

        for id in inactive_ids {
            streams.remove(&id);
            analytics.remove(&id);
        }
    }
}

/// Stream monitoring configuration
pub struct StreamMonitorConfig {
    pub platforms: Vec<StreamPlatform>,
    pub categories: Vec<String>,
    pub languages: Vec<String>,
    pub min_viewers: u32,
    pub update_interval_seconds: u64,
}

impl Default for StreamMonitorConfig {
    fn default() -> Self {
        Self {
            platforms: vec![StreamPlatform::Twitch, StreamPlatform::YouTube],
            categories: vec![
                "Science & Technology".to_string(),
                "Education".to_string(),
                "Programming".to_string(),
            ],
            languages: vec!["en".to_string()],
            min_viewers: 100,
            update_interval_seconds: 300, // 5 minutes
        }
    }
}
