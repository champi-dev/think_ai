// Newsletter and blog content scraper
// Specializes in extracting content from various blog platforms

use crate::realtime_knowledge_gatherer::{WebContent, WebSource, WebSourceType};
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
/// Blog platform types
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub enum BlogPlatform {
    Medium,
    DevTo,
    Substack,
    Ghost,
    WordPress,
    Custom,
}
/// Newsletter subscription info
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NewsletterSource {
    pub name: String,
    pub url: String,
    pub platform: BlogPlatform,
    pub categories: Vec<String>,
    pub author: Option<String>,
    pub frequency: String, // daily, weekly, monthly
/// Blog post data
pub struct BlogPost {
    pub title: String,
    pub author: String,
    pub content_preview: String,
    pub full_content: Option<String>,
    pub tags: Vec<String>,
    pub published_date: DateTime<Utc>,
    pub read_time_minutes: u32,
    pub claps_or_likes: Option<u32>,
/// Newsletter and blog scraper
pub struct NewsletterBlogScraper {
    http_client: reqwest::Client,
    sources: Vec<NewsletterSource>,
impl NewsletterBlogScraper {
    pub fn new() -> Self {
        let http_client = reqwest::Client::builder()
            .user_agent("ThinkAI/1.0 (Newsletter Reader; Public Content)")
            .timeout(std::time::Duration::from_secs(30))
            .build()
            .unwrap();
        let sources = Self::initialize_sources();
        Self {
            http_client,
            sources,
        }
    }
    /// Initialize popular newsletter and blog sources
    fn initialize_sources() -> Vec<NewsletterSource> {
        vec![
            // Tech newsletters
            NewsletterSource {
                name: "Morning Brew Tech".to_string(),
                url: "https://www.morningbrew.com/emerging-tech/feed".to_string(),
                platform: BlogPlatform::Custom,
                categories: vec!["technology".to_string(), "startups".to_string()],
                author: None,
                frequency: "daily".to_string(),
            },
                name: "The Pragmatic Engineer".to_string(),
                url: "https://blog.pragmaticengineer.com/rss/".to_string(),
                platform: BlogPlatform::Substack,
                categories: vec!["engineering".to_string(), "tech-careers".to_string()],
                author: Some("Gergely Orosz".to_string()),
                frequency: "weekly".to_string(),
                name: "ByteByteGo".to_string(),
                url: "https://blog.bytebytego.com/feed".to_string(),
                categories: vec!["system-design".to_string(), "architecture".to_string()],
                author: Some("Alex Xu".to_string()),
            // AI/ML newsletters
                name: "The Batch by Andrew Ng".to_string(),
                url: "https://www.deeplearning.ai/the-batch/feed/".to_string(),
                categories: vec!["ai".to_string(), "machine-learning".to_string()],
                author: Some("Andrew Ng".to_string()),
                name: "Import AI".to_string(),
                url: "https://jack-clark.net/feed/".to_string(),
                platform: BlogPlatform::WordPress,
                categories: vec!["ai".to_string(), "research".to_string()],
                author: Some("Jack Clark".to_string()),
            // Dev blogs
                name: "JavaScript Weekly".to_string(),
                url: "https://javascriptweekly.com/rss/".to_string(),
                categories: vec!["javascript".to_string(), "web-dev".to_string()],
                name: "Rust Weekly".to_string(),
                url: "https://this-week-in-rust.org/rss.xml".to_string(),
                categories: vec!["rust".to_string(), "systems-programming".to_string()],
        ]
    /// Scrape all newsletter sources
    pub async fn scrape_all_sources(&self) -> Vec<BlogPost> {
        let mut all_posts = Vec::new();
        for source in &self.sources {
            match self.scrape_source(source).await {
                Ok(posts) => {
                    println!("📰 Scraped {} posts from {}", posts.len(), source.name);
                    all_posts.extend(posts);
                }
                Err(e) => {
                    eprintln!("❌ Error scraping {}: {}", source.name, e);
            }
            // Rate limiting
            tokio::time::sleep(tokio::time::Duration::from_millis(500)).await;
        // Sort by published date (newest first)
        all_posts.sort_by(|a, b| b.published_date.cmp(&a.published_date));
        all_posts
    /// Scrape a specific source
    async fn scrape_source(
        &self,
        source: &NewsletterSource,
    ) -> Result<Vec<BlogPost>, Box<dyn std::error::Error + Send + Sync>> {
        match source.platform {
            BlogPlatform::Medium => self.scrape_medium(&source.url).await,
            BlogPlatform::DevTo => self.scrape_devto(&source.url).await,
            BlogPlatform::Substack => self.scrape_rss(&source.url, &source.platform).await,
            BlogPlatform::Ghost => self.scrape_rss(&source.url, &source.platform).await,
            BlogPlatform::WordPress => self.scrape_rss(&source.url, &source.platform).await,
            BlogPlatform::Custom => self.scrape_rss(&source.url, &source.platform).await,
    /// Scrape Medium RSS feed
    async fn scrape_medium(
        url: &str,
        // Medium uses RSS but with specific structure
        let response = self.http_client.get(url).send().await?;
        let body = response.text().await?;
        let mut posts = Vec::new();
        let items: Vec<&str> = body.split("<item>").skip(1).collect();
        for item in items.iter().take(10) {
            if let Some(post) = self.parse_medium_item(item) {
                posts.push(post);
        Ok(posts)
    /// Parse Medium RSS item
    fn parse_medium_item(&self, item: &str) -> Option<BlogPost> {
        let title = self.extract_xml_content(item, "title")?;
        let link = self.extract_xml_content(item, "link")?;
        let creator = self
            .extract_xml_content(item, "dc:creator")
            .unwrap_or_default();
        let description = self
            .extract_xml_content(item, "description")
        let pub_date = self.extract_xml_content(item, "pubDate")?;
        // Extract categories as tags
        let mut tags = Vec::new();
        let categories: Vec<&str> = item.split("<category>").skip(1).collect();
        for category in categories {
            if let Some(end) = category.find("</category>") {
                let tag = category[..end].trim();
                if !tag.is_empty() {
                    tags.push(tag.to_string());
        // Parse publication date
        let published_date = DateTime::parse_from_rfc2822(&pub_date)
            .ok()?
            .with_timezone(&Utc);
        // Estimate read time (250 words per minute)
        let word_count = description.split_whitespace().count();
        let read_time = (word_count / 250).max(1) as u32;
        Some(BlogPost {
            title,
            url: link,
            author: creator,
            platform: BlogPlatform::Medium,
            content_preview: self.clean_html(&description),
            full_content: None,
            tags,
            published_date,
            read_time_minutes: read_time,
            claps_or_likes: None,
        })
    /// Scrape Dev.to API
    async fn scrape_devto(
        _url: &str,
        // Dev.to has a public API
        let api_url = "https://dev.to/api/articles?per_page=30&top=7";
        let response = self.http_client.get(api_url).send().await?;
        let articles: Vec<DevToArticle> = response.json().await?;
        let posts = articles
            .into_iter()
            .map(|article| BlogPost {
                title: article.title,
                url: article.url,
                author: article.user.name,
                platform: BlogPlatform::DevTo,
                content_preview: article.description,
                full_content: None,
                tags: article
                    .tag_list
                    .split(", ")
                    .map(|s| s.to_string())
                    .collect(),
                published_date: article
                    .published_at
                    .parse::<DateTime<Utc>>()
                    .unwrap_or_else(|_| Utc::now()),
                read_time_minutes: article.reading_time_minutes,
                claps_or_likes: Some(article.positive_reactions_count),
            })
            .collect();
    /// Generic RSS scraper
    async fn scrape_rss(
        platform: &BlogPlatform,
            if let Some(post) = self.parse_rss_item(item, platform) {
    /// Parse generic RSS item
    fn parse_rss_item(&self, item: &str, platform: &BlogPlatform) -> Option<BlogPost> {
        let author = self
            .extract_xml_content(item, "author")
            .or_else(|| self.extract_xml_content(item, "dc:creator"))
            .unwrap_or_else(|| "Unknown".to_string());
            author,
            platform: platform.clone(),
            tags: vec![],
    /// Extract content from XML tags
    fn extract_xml_content(&self, xml: &str, tag: &str) -> Option<String> {
        let start_tag = format!("<{}>", tag);
        let end_tag = format!("</{}>", tag);
        if let Some(start) = xml.find(&start_tag) {
            if let Some(end) = xml.find(&end_tag) {
                let content = &xml[start + start_tag.len()..end];
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
        None
    /// Clean HTML tags from content
    fn clean_html(&self, html: &str) -> String {
        // Simple HTML tag removal
        let mut result = html.to_string();
        // Remove script and style blocks
        while let Some(start) = result.find("<script") {
            if let Some(end) = result.find("</script>") {
                result.replace_range(start..end + 9, "");
            } else {
                break;
        while let Some(start) = result.find("<style") {
            if let Some(end) = result.find("</style>") {
                result.replace_range(start..end + 8, "");
        // Remove all HTML tags
        let tag_regex = regex::Regex::new(r"<[^>]+>").unwrap();
        let result = tag_regex.replace_all(&result, " ");
        // Clean up whitespace
        result.split_whitespace().collect::<Vec<_>>().join(" ")
    /// Convert blog post to WebContent
    pub fn blog_to_web_content(&self, post: &BlogPost) -> WebContent {
        let mut metadata = HashMap::new();
        metadata.insert("platform".to_string(), format!("{:?}", post.platform));
        metadata.insert("author".to_string(), post.author.clone());
        metadata.insert(
            "read_time".to_string(),
            format!("{} min", post.read_time_minutes),
        );
        if !post.tags.is_empty() {
            metadata.insert("tags".to_string(), post.tags.join(", "));
        if let Some(likes) = post.claps_or_likes {
            metadata.insert("engagement".to_string(), likes.to_string());
        WebContent {
            source_id: format!("{:?}_blog", post.platform),
            url: post.url.clone(),
            title: post.title.clone(),
            content: post.content_preview.clone(),
            author: Some(post.author.clone()),
            published_date: Some(post.published_date),
            gathered_at: Utc::now(),
            metadata,
/// Dev.to API response structure
#[derive(Debug, Deserialize)]
struct DevToArticle {
    title: String,
    description: String,
    url: String,
    published_at: String,
    positive_reactions_count: u32,
    reading_time_minutes: u32,
    tag_list: String,
    user: DevToUser,
struct DevToUser {
    name: String,
