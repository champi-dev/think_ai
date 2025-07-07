# 🌐 Think AI Real-Time Knowledge Gathering

Think AI now includes a powerful real-time knowledge gathering system that continuously monitors public web sources to keep its knowledge current and up-to-date!

## Features

### 📰 Newsletter & Blog Scraping
- **Medium** - Technology articles and insights
- **Dev.to** - Developer community posts
- **Substack** - Popular newsletters
- **Hacker News** - Tech news and discussions
- **TechCrunch** - Startup and tech industry news
- **JavaScript Weekly** - JS ecosystem updates
- **Rust Weekly** - Rust programming updates
- **The Pragmatic Engineer** - Engineering insights
- **ByteByteGo** - System design knowledge

### 💬 Social Media Monitoring
- **Reddit** - Trending topics from tech subreddits
- **YouTube** - Trending tech videos (via RSS)
- Public posts and discussions
- Trending topic aggregation
- Sentiment analysis ready

### 📺 Live Stream Analytics
- **YouTube Live** - Tech streams and tutorials
- **Twitch** - Coding streams
- Stream popularity tracking
- Category analysis
- Viewer engagement metrics

### 🛡️ Ethical Data Collection
- **Respects robots.txt** - Always checks site policies
- **Rate limiting** - 1-2 second delays between requests
- **Public data only** - No private or authenticated content
- **User agent identification** - Clear bot identification
- **Minimal server load** - Conservative request limits

## How It Works

1. **Background Service**: Runs continuously, checking sources every 5-60 minutes
2. **Smart Caching**: Stores recent content for 24 hours
3. **Knowledge Integration**: Automatically adds to Think AI's knowledge base
4. **O(1) Performance**: Uses hash-based lookups for instant access
5. **Domain Classification**: Categorizes content by subject area

## Usage

### Start the Service
```bash
# Build and run the real-time knowledge gatherer
./test-realtime-knowledge.sh

# Or run directly
cargo run --release --bin start-realtime-knowledge
```

### Integration with Chat
When chatting with Think AI, it automatically uses the latest gathered knowledge:
```bash
./target/release/think-ai chat

# Ask about recent topics
> What's trending in tech today?
> Tell me about the latest JavaScript features
> What are developers discussing on Reddit?
```

### Configuration

Edit sources in `realtime_knowledge_gatherer.rs`:
```rust
WebSource {
    id: "custom_blog".to_string(),
    name: "My Favorite Blog".to_string(),
    url: "https://example.com/feed.xml".to_string(),
    source_type: WebSourceType::RSS,
    check_interval_minutes: 30,
    is_active: true,
    rate_limit_ms: 1000,
}
```

## Architecture

### Core Components

1. **RealtimeKnowledgeGatherer** - Main orchestrator
   - Manages sources and scheduling
   - Handles rate limiting
   - Stores in knowledge engine

2. **NewsletterBlogScraper** - Blog content extraction
   - RSS feed parsing
   - HTML content cleaning
   - Multi-platform support

3. **SocialMediaGatherer** - Social platform monitoring
   - Reddit API integration
   - YouTube RSS feeds
   - Trend aggregation

4. **LiveStreamMonitor** - Live content tracking
   - Platform-specific adapters
   - Real-time analytics
   - Trending score calculation

### Data Flow

```
Web Sources → Gatherers → Content Extraction → Knowledge Engine → Think AI Chat
     ↓            ↓               ↓                    ↓
Rate Limiter  Parsers      Deduplication      O(1) Hash Storage
```

### Performance

- **Gathering Speed**: ~100-500 items per minute
- **Memory Usage**: ~50-100MB for cache
- **Network**: Minimal bandwidth usage
- **Storage**: O(1) hash-based lookups

## Supported Formats

- **RSS/Atom** feeds
- **JSON APIs** (with proper headers)
- **Public web pages** (with ethical scraping)

## Privacy & Ethics

Think AI's real-time knowledge gathering follows strict ethical guidelines:

1. **Public Data Only**: Never accesses private or authenticated content
2. **Respect for Servers**: Conservative rate limiting to avoid overload
3. **Clear Identification**: User agent identifies as "ThinkAI/1.0"
4. **No Personal Data**: Doesn't collect or store personal information
5. **Robots.txt Compliance**: Respects website policies

## Adding New Sources

To add a new knowledge source:

1. Define the source in `initialize_default_sources()`
2. Implement parser if needed (RSS is automatic)
3. Set appropriate rate limits
4. Test with a single gather cycle

Example:
```rust
WebSource {
    id: "arxiv_cs".to_string(),
    name: "arXiv Computer Science".to_string(),
    url: "https://arxiv.org/rss/cs".to_string(),
    source_type: WebSourceType::RSS,
    check_interval_minutes: 120,
    last_checked: None,
    is_active: true,
    rate_limit_ms: 2000,
}
```

## Monitoring

Check gathering status:
```bash
# View logs
./target/release/start-realtime-knowledge

# Sample output:
🌐 Gathering real-time knowledge...
📚 Gathered 45 new items
📰 Scraped 10 posts from Hacker News
📰 Scraped 15 posts from Dev.to
📰 Scraped 8 posts from Medium - Technology
```

## Future Enhancements

- [ ] More social platforms (Twitter/X API when available)
- [ ] Academic paper monitoring (arXiv, PubMed)
- [ ] Podcast transcripts
- [ ] GitHub trending repositories
- [ ] Stack Overflow questions
- [ ] News aggregation with summarization
- [ ] Multi-language support
- [ ] Webhooks for instant updates
- [ ] GraphQL API support
- [ ] Custom scraping rules

## Troubleshooting

### No Content Gathered
- Check internet connection
- Verify RSS feed URLs are accessible
- Check rate limiting hasn't been triggered

### High Memory Usage
- Reduce cache duration in `run_knowledge_gatherer()`
- Limit number of sources
- Adjust check intervals

### Parsing Errors
- Some RSS feeds may have non-standard formats
- Check feed URL returns valid XML
- Add custom parser for specific formats

Think AI now stays current with the latest knowledge from across the web! 🚀