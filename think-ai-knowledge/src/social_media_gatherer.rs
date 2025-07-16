// Social media data gathering (public data only)
// Collects trending topics, public posts, and insights

use crate::realtime_knowledge_gatherer::{SocialPlatform, WebContent};
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::RwLock;

/// Social media post data
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SocialMediaPost {
    pub platform: SocialPlatform,
    pub post_id: String,
    pub author: String,
    pub content: String,
    pub url: String,
    pub likes: u32,
    pub shares: u32,
    pub comments: u32,
    pub hashtags: Vec<String>,
    pub mentions: Vec<String>,
    pub media_urls: Vec<String>,
    pub posted_at: DateTime<Utc>,
    pub gathered_at: DateTime<Utc>,
}

/// Trending topic across platforms
#[derive(Debug, Clone)]
pub struct TrendingTopic {
    pub topic: String,
    pub platforms: Vec<SocialPlatform>,
    pub volume: u32,
    pub sentiment: f32, // -1.0 to 1.0
    pub related_hashtags: Vec<String>,
    pub sample_posts: Vec<String>,
    pub trending_since: DateTime<Utc>,
}

/// Social media data gatherer
pub struct SocialMediaGatherer {
    http_client: reqwest::Client,
    rate_limits: Arc<RwLock<HashMap<SocialPlatform, RateLimit>>>,
}

#[derive(Debug, Clone)]
struct RateLimit {
    requests_per_hour: u32,
    last_request: Option<DateTime<Utc>>,
    request_count: u32,
}

impl Default for SocialMediaGatherer {
    fn default() -> Self {
        Self::new()
    }
}

impl SocialMediaGatherer {
    pub fn new() -> Self {
        let http_client = reqwest::Client::builder()
            .user_agent("ThinkAI/1.0 (Public Data Gatherer)")
            .timeout(std::time::Duration::from_secs(30))
            .build()
            .unwrap();

        let mut rate_limits = HashMap::new();

        // Set conservative rate limits for each platform
        rate_limits.insert(
            SocialPlatform::X,
            RateLimit {
                requests_per_hour: 100,
                last_request: None,
                request_count: 0,
            },
        );

        rate_limits.insert(
            SocialPlatform::Reddit,
            RateLimit {
                requests_per_hour: 60,
                last_request: None,
                request_count: 0,
            },
        );

        rate_limits.insert(
            SocialPlatform::YouTube,
            RateLimit {
                requests_per_hour: 60,
                last_request: None,
                request_count: 0,
            },
        );

        Self {
            http_client,
            rate_limits: Arc::new(RwLock::new(rate_limits)),
        }
    }

    /// Gather trending topics across all platforms
    pub async fn gather_trending_topics(&self) -> Vec<TrendingTopic> {
        let mut all_trends = Vec::new();

        // Reddit trending
        if let Ok(reddit_trends) = self.gather_reddit_trending().await {
            all_trends.extend(reddit_trends);
        }

        // YouTube trending
        if let Ok(youtube_trends) = self.gather_youtube_trending().await {
            all_trends.extend(youtube_trends);
        }

        // Aggregate and deduplicate trends
        self.aggregate_trends(all_trends)
    }

    /// Gather Reddit trending topics
    async fn gather_reddit_trending(
        &self,
    ) -> Result<Vec<TrendingTopic>, Box<dyn std::error::Error + Send + Sync>> {
        if !self.check_rate_limit(&SocialPlatform::Reddit).await {
            return Ok(vec![]);
        }

        let mut trends = Vec::new();

        // Popular subreddits to check
        let subreddits = vec!["all", "technology", "worldnews", "science", "programming"];

        for subreddit in subreddits {
            let url = format!("https://www.reddit.com/r/{subreddit}/hot.json?limit=10");

            match self.http_client.get(&url).send().await {
                Ok(response) => {
                    if let Ok(text) = response.text().await {
                        if let Ok(json) = serde_json::from_str::<serde_json::Value>(&text) {
                            if let Some(posts) = json["data"]["children"].as_array() {
                                for post in posts {
                                    let data = &post["data"];
                                    let title = data["title"].as_str().unwrap_or_default();
                                    let score = data["score"].as_u64().unwrap_or(0) as u32;

                                    if score > 1000 {
                                        // High engagement threshold
                                        trends.push(TrendingTopic {
                                            topic: title.to_string(),
                                            platforms: vec![SocialPlatform::Reddit],
                                            volume: score,
                                            sentiment: 0.0, // Would need sentiment analysis
                                            related_hashtags: vec![],
                                            sample_posts: vec![title.to_string()],
                                            trending_since: Utc::now(),
                                        });
                                    }
                                }
                            }
                        }
                    }
                }
                Err(e) => eprintln!("Error fetching Reddit trends: {e}"),
            }

            // Rate limit between requests
            tokio::time::sleep(tokio::time::Duration::from_millis(1000)).await;
        }

        self.update_rate_limit(&SocialPlatform::Reddit).await;
        Ok(trends)
    }

    /// Gather YouTube trending videos
    async fn gather_youtube_trending(
        &self,
    ) -> Result<Vec<TrendingTopic>, Box<dyn std::error::Error + Send + Sync>> {
        if !self.check_rate_limit(&SocialPlatform::YouTube).await {
            return Ok(vec![]);
        }

        // YouTube RSS feed for trending
        let url = "https://www.youtube.com/feeds/videos.xml?chart=mostPopular";

        let trends = match self.http_client.get(url).send().await {
            Ok(response) => {
                if let Ok(text) = response.text().await {
                    self.parse_youtube_trending(&text)
                } else {
                    vec![]
                }
            }
            Err(e) => {
                eprintln!("Error fetching YouTube trends: {e}");
                vec![]
            }
        };

        self.update_rate_limit(&SocialPlatform::YouTube).await;
        Ok(trends)
    }

    /// Parse YouTube RSS feed
    fn parse_youtube_trending(&self, xml: &str) -> Vec<TrendingTopic> {
        let mut trends = Vec::new();

        // Simple XML parsing for entries
        let entries: Vec<&str> = xml.split("<entry>").skip(1).collect();

        for entry in entries.iter().take(10) {
            if let Some(title) = self.extract_xml_content(entry, "title") {
                trends.push(TrendingTopic {
                    topic: title.clone(),
                    platforms: vec![SocialPlatform::YouTube],
                    volume: 0, // Would need view count from API
                    sentiment: 0.0,
                    related_hashtags: vec![],
                    sample_posts: vec![title],
                    trending_since: Utc::now(),
                });
            }
        }

        trends
    }

    /// Extract content from XML
    fn extract_xml_content(&self, xml: &str, tag: &str) -> Option<String> {
        let start_tag = format!("<{tag}>");
        let end_tag = format!("</{tag}>");

        if let Some(start) = xml.find(&start_tag) {
            if let Some(end) = xml.find(&end_tag) {
                let content = &xml[start + start_tag.len()..end];
                return Some(content.trim().to_string());
            }
        }

        None
    }

    /// Check rate limit for platform
    async fn check_rate_limit(&self, platform: &SocialPlatform) -> bool {
        let limits = self.rate_limits.read().await;

        if let Some(limit) = limits.get(platform) {
            if let Some(last_request) = limit.last_request {
                let elapsed = Utc::now().signed_duration_since(last_request);
                if elapsed.num_hours() < 1 && limit.request_count >= limit.requests_per_hour {
                    return false;
                }
            }
        }

        true
    }

    /// Update rate limit tracking
    async fn update_rate_limit(&self, platform: &SocialPlatform) {
        let mut limits = self.rate_limits.write().await;

        if let Some(limit) = limits.get_mut(platform) {
            let now = Utc::now();

            if let Some(last_request) = limit.last_request {
                let elapsed = now.signed_duration_since(last_request);
                if elapsed.num_hours() >= 1 {
                    limit.request_count = 1;
                } else {
                    limit.request_count += 1;
                }
            } else {
                limit.request_count = 1;
            }

            limit.last_request = Some(now);
        }
    }

    /// Aggregate and deduplicate trends
    fn aggregate_trends(&self, trends: Vec<TrendingTopic>) -> Vec<TrendingTopic> {
        let mut aggregated: HashMap<String, TrendingTopic> = HashMap::new();

        for trend in trends {
            let key = trend.topic.to_lowercase();

            if let Some(existing) = aggregated.get_mut(&key) {
                // Merge platforms
                for platform in trend.platforms {
                    if !existing.platforms.contains(&platform) {
                        existing.platforms.push(platform);
                    }
                }
                existing.volume += trend.volume;
                existing.sample_posts.extend(trend.sample_posts);
            } else {
                aggregated.insert(key, trend);
            }
        }

        // Sort by volume
        let mut sorted_trends: Vec<TrendingTopic> = aggregated.into_values().collect();
        sorted_trends.sort_by(|a, b| b.volume.cmp(&a.volume));

        sorted_trends
    }

    /// Convert social media data to WebContent
    pub fn social_to_web_content(&self, post: &SocialMediaPost) -> WebContent {
        let mut metadata = HashMap::new();
        metadata.insert("platform".to_string(), format!("{:?}", post.platform));
        metadata.insert("likes".to_string(), post.likes.to_string());
        metadata.insert("shares".to_string(), post.shares.to_string());
        metadata.insert("comments".to_string(), post.comments.to_string());

        if !post.hashtags.is_empty() {
            metadata.insert("hashtags".to_string(), post.hashtags.join(", "));
        }

        WebContent {
            source_id: format!("{:?}", post.platform),
            url: post.url.clone(),
            title: format!("Post by {}", post.author),
            content: post.content.clone(),
            author: Some(post.author.clone()),
            published_date: Some(post.posted_at),
            gathered_at: post.gathered_at,
            metadata,
        }
    }
}

/// Ethical scraping guidelines
pub struct EthicalScrapingRules {
    pub respect_robots_txt: bool,
    pub min_request_interval_ms: u64,
    pub max_requests_per_hour: u32,
    pub user_agent: String,
    pub only_public_data: bool,
}

impl Default for EthicalScrapingRules {
    fn default() -> Self {
        Self {
            respect_robots_txt: true,
            min_request_interval_ms: 1000, // 1 second minimum
            max_requests_per_hour: 100,
            user_agent: "ThinkAI/1.0 (Ethical Public Data Gatherer; +https://thinkai.dev/bot)"
                .to_string(),
            only_public_data: true,
        }
    }
}
