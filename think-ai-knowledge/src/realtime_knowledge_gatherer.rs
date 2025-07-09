// Real-time knowledge gathering from public web sources
// Collects data from newsletters, blogs, social media, and live streams

use crate::{KnowledgeDomain, KnowledgeEngine};
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::RwLock;

/// Types of web sources we can gather from
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub enum WebSourceType {
    Newsletter,
    Blog,
    SocialMedia(SocialPlatform),
    LiveStream(StreamPlatform),
    RSS,
    API,
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum SocialPlatform {
    X, // formerly Twitter
    Facebook,
    Instagram,
    TikTok,
    YouTube,
    LinkedIn,
    Reddit,
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum StreamPlatform {
    Twitch,
    YouTube,
    FacebookLive,
    InstagramLive,
}

/// Configuration for a web source
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WebSource {
    pub id: String,
    pub name: String,
    pub url: String,
    pub source_type: WebSourceType,
    pub check_interval_minutes: u32,
    pub last_checked: Option<DateTime<Utc>>,
    pub is_active: bool,
    pub rate_limit_ms: u64, // Milliseconds between requests
}

/// Gathered content from web
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WebContent {
    pub source_id: String,
    pub title: String,
    pub content: String,
    pub url: String,
    pub author: Option<String>,
    pub published_date: Option<DateTime<Utc>>,
    pub gathered_at: DateTime<Utc>,
    pub metadata: HashMap<String, String>,
}

/// Real-time knowledge gatherer
pub struct RealtimeKnowledgeGatherer {
    knowledge_engine: Arc<KnowledgeEngine>,
    sources: Arc<RwLock<HashMap<String, WebSource>>>,
    content_cache: Arc<RwLock<HashMap<String, WebContent>>>,
    rate_limiters: Arc<RwLock<HashMap<String, DateTime<Utc>>>>,
    http_client: reqwest::Client,
}

impl RealtimeKnowledgeGatherer {
    pub fn new(knowledge_engine: Arc<KnowledgeEngine>) -> Self {
        let http_client = reqwest::Client::builder()
            .user_agent("ThinkAI/1.0 (Knowledge Gatherer; Public Data Only)")
            .timeout(std::time::Duration::from_secs(30))
            .build()
            .unwrap();

        let mut gatherer = Self {
            knowledge_engine,
            sources: Arc::new(RwLock::new(HashMap::new())),
            content_cache: Arc::new(RwLock::new(HashMap::new())),
            rate_limiters: Arc::new(RwLock::new(HashMap::new())),
            http_client,
        };

        // Initialize default sources
        gatherer.initialize_default_sources();
        gatherer
    }

    /// Initialize with popular public sources
    fn initialize_default_sources(&mut self) {
        let default_sources = vec![
            // Tech Blogs
            WebSource {
                id: "hackernews".to_string(),
                name: "Hacker News".to_string(),
                url: "https://news.ycombinator.com/rss".to_string(),
                source_type: WebSourceType::RSS,
                check_interval_minutes: 60,
                last_checked: None,
                is_active: true,
                rate_limit_ms: 1000,
            },
            WebSource {
                id: "medium_tech".to_string(),
                name: "Medium - Technology".to_string(),
                url: "https://medium.com/feed/topic/technology".to_string(),
                source_type: WebSourceType::Blog,
                check_interval_minutes: 120,
                last_checked: None,
                is_active: true,
                rate_limit_ms: 2000,
            },
            WebSource {
                id: "dev_to".to_string(),
                name: "Dev.to".to_string(),
                url: "https://dev.to/feed".to_string(),
                source_type: WebSourceType::RSS,
                check_interval_minutes: 90,
                last_checked: None,
                is_active: true,
                rate_limit_ms: 1500,
            },
            // News Sources
            WebSource {
                id: "techcrunch".to_string(),
                name: "TechCrunch".to_string(),
                url: "https://techcrunch.com/feed/".to_string(),
                source_type: WebSourceType::RSS,
                check_interval_minutes: 120,
                last_checked: None,
                is_active: true,
                rate_limit_ms: 2000,
            },
            // Reddit (public posts only)
            WebSource {
                id: "reddit_tech".to_string(),
                name: "Reddit - Technology".to_string(),
                url: "https://www.reddit.com/r/technology/.rss".to_string(),
                source_type: WebSourceType::SocialMedia(SocialPlatform::Reddit),
                check_interval_minutes: 30,
                last_checked: None,
                is_active: true,
                rate_limit_ms: 3000,
            },
        ];

        // Initialize sources synchronously
        let sources_clone = self.sources.clone();
        let handle = tokio::runtime::Handle::try_current();

        if let Ok(handle) = handle {
            handle.block_on(async {
                let mut sources = sources_clone.write().await;
                for source in default_sources {
                    sources.insert(source.id.clone(), source);
                }
            });
        } else {
            // If no tokio runtime is available, we'll add sources later
            eprintln!("Warning: Could not initialize default sources - no tokio runtime available");
        }
    }

    /// Add a new source
    pub async fn add_source(&self, source: WebSource) -> Result<(), String> {
        // Validate URL
        if !source.url.starts_with("http://") && !source.url.starts_with("https://") {
            return Err("URL must start with http:// or https://".to_string());
        }

        let mut sources = self.sources.write().await;
        sources.insert(source.id.clone(), source);
        Ok(())
    }

    /// Gather content from all active sources
    pub async fn gather_all(&self) -> Vec<WebContent> {
        let sources = self.sources.read().await;
        let active_sources: Vec<WebSource> =
            sources.values().filter(|s| s.is_active).cloned().collect();
        drop(sources);

        let mut all_content = Vec::new();

        for source in active_sources {
            if self.should_check_source(&source).await {
                match self.gather_from_source(&source).await {
                    Ok(content) => {
                        all_content.extend(content);
                        self.update_last_checked(&source.id).await;
                    }
                    Err(e) => {
                        eprintln!("Error gathering from {}: {}", source.name, e);
                    }
                }
            }
        }

        // Store in knowledge engine
        for content in &all_content {
            self.store_in_knowledge_engine(content).await;
        }

        all_content
    }

    /// Check if we should gather from this source (rate limiting)
    async fn should_check_source(&self, source: &WebSource) -> bool {
        let rate_limiters = self.rate_limiters.read().await;

        if let Some(last_request) = rate_limiters.get(&source.id) {
            let elapsed = Utc::now().signed_duration_since(*last_request);
            if elapsed.num_milliseconds() < source.rate_limit_ms as i64 {
                return false;
            }
        }

        // Check interval
        if let Some(last_checked) = source.last_checked {
            let elapsed = Utc::now().signed_duration_since(last_checked);
            if elapsed.num_minutes() < source.check_interval_minutes as i64 {
                return false;
            }
        }

        true
    }

    /// Gather content from a specific source
    async fn gather_from_source(
        &self,
        source: &WebSource,
    ) -> Result<Vec<WebContent>, Box<dyn std::error::Error + Send + Sync>> {
        // Update rate limiter
        {
            let mut rate_limiters = self.rate_limiters.write().await;
            rate_limiters.insert(source.id.clone(), Utc::now());
        }

        match &source.source_type {
            WebSourceType::RSS => self.gather_rss(source).await,
            WebSourceType::Blog => self.gather_blog(source).await,
            WebSourceType::Newsletter => self.gather_newsletter(source).await,
            WebSourceType::SocialMedia(platform) => {
                self.gather_social_media(source, platform).await
            }
            WebSourceType::LiveStream(platform) => self.gather_live_stream(source, platform).await,
            WebSourceType::API => self.gather_api(source).await,
        }
    }

    /// Gather RSS feed content
    async fn gather_rss(
        &self,
        source: &WebSource,
    ) -> Result<Vec<WebContent>, Box<dyn std::error::Error + Send + Sync>> {
        let response = self.http_client.get(&source.url).send().await?;
        let body = response.text().await?;

        // Parse RSS (simplified - in production use proper RSS parser)
        let mut content_items = Vec::new();

        // Extract items from RSS XML
        let items: Vec<&str> = body.split("<item>").skip(1).collect();

        for item in items.iter().take(10) {
            // Limit to 10 items
            let title = self.extract_xml_content(item, "title").unwrap_or_default();
            let description = self
                .extract_xml_content(item, "description")
                .unwrap_or_default();
            let link = self.extract_xml_content(item, "link").unwrap_or_default();
            let pub_date = self.extract_xml_content(item, "pubDate");

            let content = WebContent {
                source_id: source.id.clone(),
                url: link.clone(),
                title: title.clone(),
                content: description,
                author: self.extract_xml_content(item, "author"),
                published_date: pub_date
                    .and_then(|d| DateTime::parse_from_rfc2822(&d).ok())
                    .map(|d| d.with_timezone(&Utc)),
                gathered_at: Utc::now(),
                metadata: HashMap::new(),
            };

            content_items.push(content);
        }

        Ok(content_items)
    }

    /// Extract content from XML tags
    fn extract_xml_content(&self, xml: &str, tag: &str) -> Option<String> {
        let start_tag = format!("<{tag}>");
        let end_tag = format!("</{tag}>");

        if let Some(start) = xml.find(&start_tag) {
            if let Some(end) = xml.find(&end_tag) {
                let content = &xml[start + start_tag.len()..end];

                // Clean CDATA
                let cleaned = content
                    .trim()
                    .trim_start_matches("<![CDATA[")
                    .trim_end_matches("]]>")
                    .replace("&lt;", "<")
                    .replace("&gt;", ">")
                    .replace("&amp;", "&")
                    .replace("&quot;", "\"")
                    .replace("&#39;", "'");

                return Some(cleaned);
            }
        }

        None
    }

    /// Gather blog content (using RSS or scraping)
    async fn gather_blog(
        &self,
        source: &WebSource,
    ) -> Result<Vec<WebContent>, Box<dyn std::error::Error + Send + Sync>> {
        // For now, treat blogs as RSS feeds
        // In production, implement proper blog scraping
        self.gather_rss(source).await
    }

    /// Gather newsletter content
    async fn gather_newsletter(
        &self,
        _source: &WebSource,
    ) -> Result<Vec<WebContent>, Box<dyn std::error::Error + Send + Sync>> {
        // Newsletter gathering would require email integration
        // For now, return empty
        Ok(vec![])
    }

    /// Gather social media content (public posts only)
    async fn gather_social_media(
        &self,
        source: &WebSource,
        platform: &SocialPlatform,
    ) -> Result<Vec<WebContent>, Box<dyn std::error::Error + Send + Sync>> {
        match platform {
            SocialPlatform::Reddit => {
                // Reddit supports RSS for public subreddits
                self.gather_rss(source).await
            }
            _ => {
                // Other platforms would require API integration
                // For now, return empty
                Ok(vec![])
            }
        }
    }

    /// Gather live stream data
    async fn gather_live_stream(
        &self,
        _source: &WebSource,
        _platform: &StreamPlatform,
    ) -> Result<Vec<WebContent>, Box<dyn std::error::Error + Send + Sync>> {
        // Live stream gathering would require platform-specific APIs
        // For now, return empty
        Ok(vec![])
    }

    /// Gather from API endpoint
    async fn gather_api(
        &self,
        source: &WebSource,
    ) -> Result<Vec<WebContent>, Box<dyn std::error::Error + Send + Sync>> {
        // Generic API gathering
        let response = self.http_client.get(&source.url).send().await?;
        let _body = response.text().await?;

        // Parse API response based on format
        // For now, return empty
        Ok(vec![])
    }

    /// Update last checked time
    async fn update_last_checked(&self, source_id: &str) {
        let mut sources = self.sources.write().await;
        if let Some(source) = sources.get_mut(source_id) {
            source.last_checked = Some(Utc::now());
        }
    }

    /// Store content in knowledge engine
    async fn store_in_knowledge_engine(&self, content: &WebContent) {
        // Determine domain based on source
        let domain = match content.source_id.as_str() {
            "hackernews" | "techcrunch" | "dev_to" => KnowledgeDomain::Technology,
            "medium_tech" => KnowledgeDomain::Technology,
            "reddit_tech" => KnowledgeDomain::Technology,
            _ => KnowledgeDomain::General,
        };

        // Create knowledge entry
        let topic = format!("{} - {}", content.source_id, content.title);
        let knowledge_content = format!(
            "{}\n\nSource: {}\nDate: {}\n\n{}",
            content.title,
            content.url,
            content.gathered_at.format("%Y-%m-%d %H:%M:%S UTC"),
            content.content
        );

        // Add to knowledge engine
        self.knowledge_engine.add_knowledge(
            domain,
            topic,
            knowledge_content,
            vec![content.source_id.clone(), "realtime".to_string()],
        );
    }

    /// Get recent content from cache
    pub async fn get_recent_content(&self, hours: i64) -> Vec<WebContent> {
        let cache = self.content_cache.read().await;
        let cutoff = Utc::now() - chrono::Duration::hours(hours);

        cache
            .values()
            .filter(|c| c.gathered_at > cutoff)
            .cloned()
            .collect()
    }

    /// Search gathered content
    pub async fn search_content(&self, query: &str) -> Vec<WebContent> {
        let cache = self.content_cache.read().await;
        let query_lower = query.to_lowercase();

        cache
            .values()
            .filter(|c| {
                c.title.to_lowercase().contains(&query_lower)
                    || c.content.to_lowercase().contains(&query_lower)
            })
            .cloned()
            .collect()
    }
}

/// Background task to continuously gather knowledge
pub async fn run_knowledge_gatherer(gatherer: Arc<RealtimeKnowledgeGatherer>) {
    let mut interval = tokio::time::interval(tokio::time::Duration::from_secs(300)); // 5 minutes

    loop {
        interval.tick().await;
        println!("🌐 Gathering real-time knowledge...");

        let content = gatherer.gather_all().await;
        println!("📚 Gathered {} new items", content.len());

        // Cache the content
        let mut cache = gatherer.content_cache.write().await;
        for item in content {
            cache.insert(format!("{}_{}", item.source_id, item.url), item);
        }

        // Clean old cache entries (older than 24 hours)
        let cutoff = Utc::now() - chrono::Duration::hours(24);
        cache.retain(|_, v| v.gathered_at > cutoff);
    }
}