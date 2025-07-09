// Real-time knowledge response component
// Provides responses based on recently gathered web content

use crate::realtime_knowledge_gatherer::RealtimeKnowledgeGatherer;
use crate::response_generator::{ResponseComponent, ResponseContext};
use std::sync::Arc;

/// Component that uses real-time gathered knowledge
pub struct RealtimeKnowledgeComponent {
    gatherer: Option<Arc<RealtimeKnowledgeGatherer>>,
}

impl Default for RealtimeKnowledgeComponent {
    fn default() -> Self {
        Self::new()
    }
}

impl RealtimeKnowledgeComponent {
    pub fn new() -> Self {
        Self { gatherer: None }
    }

    pub fn with_gatherer(gatherer: Arc<RealtimeKnowledgeGatherer>) -> Self {
        Self {
            gatherer: Some(gatherer),
        }
    }
}

impl ResponseComponent for RealtimeKnowledgeComponent {
    fn name(&self) -> &'static str {
        "RealtimeKnowledge"
    }

    fn can_handle(&self, query: &str, _context: &ResponseContext) -> f32 {
        let query_lower = query.to_lowercase();

        // High priority for current events and trending topics
        if query_lower.contains("trending")
            || query_lower.contains("latest")
            || query_lower.contains("recent")
            || query_lower.contains("today")
            || query_lower.contains("current")
            || query_lower.contains("news")
            || query_lower.contains("what's new")
            || query_lower.contains("what is new")
        {
            return 0.9;
        }

        // Medium priority for tech topics that might have recent updates
        if query_lower.contains("javascript")
            || query_lower.contains("rust")
            || query_lower.contains("python")
            || query_lower.contains("react")
            || query_lower.contains("ai")
            || query_lower.contains("machine learning")
            || query_lower.contains("tech")
        {
            return 0.6;
        }

        // Low priority for general queries
        0.2
    }

    fn generate(&self, query: &str, _context: &ResponseContext) -> Option<String> {
        if let Some(gatherer) = &self.gatherer {
            // Search recent content
            let recent_content = tokio::task::block_in_place(|| {
                tokio::runtime::Handle::current()
                    .block_on(async { gatherer.search_content(query).await })
            });

            if !recent_content.is_empty() {
                let mut response = String::from("Based on recent information I've gathered:\n\n");

                // Show top 3 relevant items
                for (i, content) in recent_content.iter().take(3).enumerate() {
                    response.push_str(&format!("{}. **{}**\n", i + 1, content.title));

                    // Add source info
                    if let Some(author) = &content.author {
                        response.push_str(&format!("   by {author} "));
                    }
                    response.push_str(&format!("from {}\n", content.source_id));

                    // Add preview
                    let preview = if content.content.len() > 200 {
                        format!("{}...", &content.content[..200])
                    } else {
                        content.content.clone()
                    };
                    response.push_str(&format!("   {preview}\n"));

                    // Add metadata if relevant
                    if let Some(date) = content.published_date {
                        response.push_str(&format!("   Published: {}\n", date.format("%Y-%m-%d")));
                    }

                    response.push('\n');
                }

                // Add summary for trending topics
                if query.to_lowercase().contains("trending") {
                    response.push_str("These topics are currently generating significant discussion in the tech community. ");
                    response.push_str("The information comes from trusted sources like Hacker News, Dev.to, and tech blogs.");
                }

                return Some(response);
            }
        }

        // Fallback response
        Some("I don't have any recent real-time information on that topic. My real-time knowledge gathering might not be active or might not have found relevant content yet.".to_string())
    }
}

/// Component for current events and news
pub struct CurrentEventsComponent;

impl ResponseComponent for CurrentEventsComponent {
    fn name(&self) -> &'static str {
        "CurrentEvents"
    }

    fn can_handle(&self, query: &str, _context: &ResponseContext) -> f32 {
        let query_lower = query.to_lowercase();

        if query_lower.contains("happening")
            || query_lower.contains("going on")
            || query_lower.contains("events")
            || query_lower.contains("updates")
        {
            return 0.8;
        }

        0.0
    }

    fn generate(&self, _query: &str, _context: &ResponseContext) -> Option<String> {
        let mut response = String::from("Here's what I know about current events:\n\n");

        // Provide a general response about capabilities
        response.push_str("I can access real-time information from various sources including:\n");
        response.push_str("• Tech news from Hacker News and TechCrunch\n");
        response.push_str("• Developer discussions from Reddit and Dev.to\n");
        response.push_str("• Technical articles from Medium and various blogs\n");
        response.push_str("• Trending topics in programming and technology\n\n");
        response.push_str("To get the most current information, make sure the real-time knowledge gathering service is running. ");
        response.push_str(
            "You can start it with: `cargo run --release --bin start-realtime-knowledge`",
        );

        Some(response)
    }
}