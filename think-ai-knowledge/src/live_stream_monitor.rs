// Live streaming data monitor
// Monitors public live streams for trending content and insights

use crate::realtime_knowledge_gatherer::{StreamPlatform, WebContent};
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
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
pub struct StreamAnalytics {
    pub peak_viewers: u32,
    pub average_viewers: u32,
    pub chat_activity: f32, // Messages per minute
    pub engagement_rate: f32,
    pub trending_score: f32,
/// Live stream monitor
pub struct LiveStreamMonitor {
    http_client: reqwest::Client,
    active_streams: HashMap<String, LiveStreamData>,
    analytics: HashMap<String, StreamAnalytics>,
impl LiveStreamMonitor {
    pub fn new() -> Self {
        let http_client = reqwest::Client::builder()
            .user_agent("ThinkAI/1.0 (Live Stream Monitor; Public Data)")
            .timeout(std::time::Duration::from_secs(30))
            .build()
            .unwrap();
        Self {
            http_client,
            active_streams: HashMap::new(),
            analytics: HashMap::new(),
        }
    }
    /// Monitor trending live streams
    pub async fn monitor_trending_streams(&mut self) -> Vec<LiveStreamData> {
        let mut all_streams = Vec::new();
        // YouTube Live trending
        if let Ok(youtube_streams) = self.get_youtube_live_trending().await {
            all_streams.extend(youtube_streams);
        // Twitch trending (public data)
        if let Ok(twitch_streams) = self.get_twitch_trending().await {
            all_streams.extend(twitch_streams);
        // Update active streams
        self.update_active_streams(&all_streams);
        // Sort by viewer count
        all_streams.sort_by(|a, b| b.viewer_count.cmp(&a.viewer_count));
        all_streams
    /// Get YouTube Live trending streams
    async fn get_youtube_live_trending(
        &self,
    ) -> Result<Vec<LiveStreamData>, Box<dyn std::error::Error + Send + Sync>> {
        // YouTube doesn't provide a direct public API for live streams without authentication
        // Using search results page as fallback
        let url = "https://www.youtube.com/results?search_query=live&sp=EgJAAQ%253D%253D";
        // In production, would parse the page or use YouTube Data API
        // For now, return mock data to demonstrate structure
        Ok(vec![LiveStreamData {
            platform: StreamPlatform::YouTube,
            stream_id: "sample_yt_1".to_string(),
            title: "Tech News Live Stream".to_string(),
            channel: "TechChannel".to_string(),
            viewer_count: 5000,
            category: "Technology".to_string(),
            tags: vec!["tech".to_string(), "news".to_string()],
            language: "en".to_string(),
            started_at: Utc::now() - chrono::Duration::hours(1),
            thumbnail_url: None,
            is_live: true,
        }])
    /// Get Twitch trending streams
    async fn get_twitch_trending(
        // Twitch requires OAuth for API access
        // Using public web data as fallback
        let _url = "https://www.twitch.tv/directory/all";
        // In production, would use Twitch API with proper authentication
        // For now, return mock data
            platform: StreamPlatform::Twitch,
            stream_id: "sample_twitch_1".to_string(),
            title: "Coding Stream - Building AI".to_string(),
            channel: "CodeStreamer".to_string(),
            viewer_count: 3000,
            category: "Software Development".to_string(),
            tags: vec!["coding".to_string(), "ai".to_string()],
            started_at: Utc::now() - chrono::Duration::hours(2),
    /// Update active streams tracking
    fn update_active_streams(&mut self, streams: &[LiveStreamData]) {
        // Remove ended streams
        self.active_streams.retain(|_, stream| stream.is_live);
        // Update or add new streams
        for stream in streams {
            let stream_key = format!("{:?}_{}", stream.platform, stream.stream_id);
            // Update analytics
            if let Some(_existing) = self.active_streams.get(&stream_key) {
                if let Some(analytics) = self.analytics.get_mut(&stream_key) {
                    // Update peak viewers
                    if stream.viewer_count > analytics.peak_viewers {
                        analytics.peak_viewers = stream.viewer_count;
                    }
                    // Calculate average (simplified)
                    analytics.average_viewers =
                        (analytics.average_viewers + stream.viewer_count) / 2;
                    // Calculate trending score
                    let trending_score =
                        Self::calculate_trending_score_static(stream, analytics);
                    analytics.trending_score = trending_score;
                }
            } else {
                // New stream
                self.analytics.insert(
                    stream_key.clone(),
                    StreamAnalytics {
                        peak_viewers: stream.viewer_count,
                        average_viewers: stream.viewer_count,
                        chat_activity: 0.0,
                        engagement_rate: 0.0,
                        trending_score: 0.0,
                    },
                );
            }
            self.active_streams.insert(stream_key, stream.clone());
    /// Calculate trending score for a stream (static version)
    fn calculate_trending_score_static(
        stream: &LiveStreamData,
        analytics: &StreamAnalytics,
    ) -> f32 {
        let mut score = 0.0;
        // Viewer count weight
        score += (stream.viewer_count as f32) / 1000.0;
        // Growth rate
        if analytics.average_viewers > 0 {
            let growth = (stream.viewer_count as f32 - analytics.average_viewers as f32)
                / analytics.average_viewers as f32;
            score += growth * 10.0;
        // Stream duration bonus
        let duration = Utc::now().signed_duration_since(stream.started_at);
        if duration.num_hours() > 2 {
            score += 5.0;
        score.max(0.0).min(100.0)
    /// Get top trending streams
    pub fn get_top_trending(&self, limit: usize) -> Vec<(LiveStreamData, StreamAnalytics)> {
        let mut trending: Vec<(LiveStreamData, StreamAnalytics)> = self
            .active_streams
            .iter()
            .filter_map(|(key, stream)| {
                self.analytics
                    .get(key)
                    .map(|analytics| (stream.clone(), analytics.clone()))
            })
            .collect();
        // Sort by trending score
        trending.sort_by(|a, b| b.1.trending_score.partial_cmp(&a.1.trending_score).unwrap());
        trending.into_iter().take(limit).collect()
    /// Convert stream data to WebContent
    pub fn stream_to_web_content(&self, stream: &LiveStreamData) -> WebContent {
        let mut metadata = HashMap::new();
        metadata.insert("platform".to_string(), format!("{:?}", stream.platform));
        metadata.insert("viewers".to_string(), stream.viewer_count.to_string());
        metadata.insert("category".to_string(), stream.category.clone());
        metadata.insert("language".to_string(), stream.language.clone());
        if !stream.tags.is_empty() {
            metadata.insert("tags".to_string(), stream.tags.join(", "));
        WebContent {
            source_id: format!("{:?}_live", stream.platform),
            url: self.get_stream_url(stream),
            title: stream.title.clone(),
            content: format!(
                "Live stream by {} in {} category with {} viewers. Tags: {}",
                stream.channel,
                stream.category,
                stream.viewer_count,
                stream.tags.join(", ")
            ),
            author: Some(stream.channel.clone()),
            published_date: Some(stream.started_at),
            gathered_at: Utc::now(),
            metadata,
    /// Get stream URL
    fn get_stream_url(&self, stream: &LiveStreamData) -> String {
        match stream.platform {
            StreamPlatform::YouTube => format!("https://youtube.com/watch?v={}", stream.stream_id),
            StreamPlatform::Twitch => format!("https://twitch.tv/{}", stream.channel),
            StreamPlatform::FacebookLive => {
                format!("https://facebook.com/live/{}", stream.stream_id)
            StreamPlatform::InstagramLive => {
                format!("https://instagram.com/{}/live", stream.channel)
    /// Get stream insights
    pub fn get_stream_insights(&self) -> HashMap<String, String> {
        let mut insights = HashMap::new();
        // Platform distribution
        let mut platform_counts: HashMap<StreamPlatform, u32> = HashMap::new();
        for stream in self.active_streams.values() {
            *platform_counts.entry(stream.platform.clone()).or_insert(0) += 1;
        for (platform, count) in platform_counts {
            insights.insert(format!("{:?}_active_streams", platform), count.to_string());
        // Category insights
        let mut category_viewers: HashMap<String, u32> = HashMap::new();
            *category_viewers.entry(stream.category.clone()).or_insert(0) += stream.viewer_count;
        // Top category by viewers
        if let Some((category, viewers)) = category_viewers.iter().max_by_key(|(_, v)| *v) {
            insights.insert("top_category".to_string(), category.clone());
            insights.insert("top_category_viewers".to_string(), viewers.to_string());
        // Total viewers
        let total_viewers: u32 = self.active_streams.values().map(|s| s.viewer_count).sum();
        insights.insert("total_live_viewers".to_string(), total_viewers.to_string());
        insights
