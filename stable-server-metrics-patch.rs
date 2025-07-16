// Add these imports at the top of stable-server-streaming-websearch.rs
use std::sync::Arc;
use std::time::Instant;
use uuid::Uuid;

// Add to the imports section
mod metrics;
use metrics::MetricsCollector;

// Update the StableState struct to include metrics
#[derive(Clone)]
struct StableState {
    o1_engine: Arc<O1Engine>,
    vector_index: Arc<O1VectorIndex>,
    knowledge_engine: Arc<KnowledgeEngine>,
    qwen_client: Arc<QwenClient>,
    response_generator: Arc<ComponentResponseGenerator>,
    web_search_engine: Arc<WebSearchEngine>,
    source_tracker: Arc<SourceTracker>,
    fact_checker: Arc<FactChecker>,
    metrics: Arc<MetricsCollector>, // Add this
}

// In main(), after initializing other components:
let metrics = Arc::new(MetricsCollector::new());

// Update state initialization:
let state = StableState {
    o1_engine,
    vector_index,
    knowledge_engine,
    qwen_client,
    response_generator,
    web_search_engine,
    source_tracker,
    fact_checker,
    metrics, // Add this
};

// Update the router to include the stats HTML endpoint:
let app = Router::new()
    .route("/", get(webapp_handler))
    .route("/api", get(api_docs_handler))
    .route("/api-docs", get(api_docs_handler))
    .route("/health", get(health_check))
    .route("/api/chat", post(chat_handler))
    .route("/api/chat/stream", post(chat_stream_handler))
    .route("/stats", get(stats_dashboard_handler))  // Changed from stats_handler
    .route("/stats/api", get(stats_api_handler))    // New API endpoint
    .nest_service("/static", ServeDir::new("/home/administrator/think_ai/static"))
    .layer(CorsLayer::permissive())
    .with_state(state);

// Add new handler for the HTML dashboard
async fn stats_dashboard_handler() -> Html<String> {
    match std::fs::read_to_string("/home/administrator/think_ai/static/stats-dashboard.html") {
        Ok(content) => Html(content),
        Err(_) => Html("Error: Could not load stats dashboard".to_string()),
    }
}

// Update the stats_handler to be stats_api_handler
async fn stats_api_handler(
    State(state): State<StableState>,
) -> Result<Json<serde_json::Value>, StatusCode> {
    let knowledge_stats = state.knowledge_engine.get_stats();
    let usage_stats = state.metrics.get_stats();
    let uptime_seconds = state.metrics.get_uptime_seconds();

    Ok(Json(serde_json::json!({
        "server_status": "✅ Stable with streaming and web search",
        "version": "1.0.0",
        "uptime_seconds": uptime_seconds,
        "usage_stats": {
            "total_requests": usage_stats.total_requests,
            "requests_today": usage_stats.requests_today,
            "web_searches_today": usage_stats.web_searches_today,
            "fact_checks_today": usage_stats.fact_checks_today,
            "errors_today": usage_stats.errors_today,
            "active_sessions": usage_stats.active_sessions,
            "avg_response_time_ms": usage_stats.avg_response_time_ms,
            "hourly_activity": usage_stats.hourly_activity,
        },
        "knowledge_stats": {
            "total_nodes": knowledge_stats.total_nodes,
            "domains": knowledge_stats.domains,
            "cache_hit_rate": knowledge_stats.cache_hit_rate,
            "avg_response_time_ms": knowledge_stats.avg_response_time_ms,
        },
        "optimizations": {
            "o1_engine": "Active",
            "vector_search": "O(1) LSH",
            "knowledge_lookup": "O(1) Hash",
            "timeout_protection": "30 seconds",
            "streaming": "SSE enabled",
            "web_search": "Real-time information",
            "fact_checking": "Cross-reference validation",
            "hanging_risk": "ZERO - Timeout protected"
        },
        "features": {
            "web_search": "DuckDuckGo, Wikipedia integration",
            "source_tracking": "Credibility scoring and citations",
            "fact_checking": "Multi-source verification",
            "real_time_info": "Current events and updates"
        }
    })))
}

// Update chat_handler to track metrics
async fn chat_handler(
    State(state): State<StableState>,
    Json(request): Json<ChatRequest>,
) -> Result<Json<ChatResponse>, StatusCode> {
    let start = std::time::Instant::now();
    let session_id = Uuid::new_v4().to_string();
    
    // Track session
    state.metrics.add_session(session_id.clone());
    
    // Apply timeout to prevent hanging
    match timeout(Duration::from_secs(30), async {
        // ... existing chat handling code ...
        
        // At the end of the handler, before returning:
        let elapsed = start.elapsed().as_secs_f64() * 1000.0;
        let error_occurred = false; // Set this to true if an error occurs
        
        // Record metrics
        state.metrics.record_request(
            elapsed,
            web_search_used,
            request.fact_check,
            error_occurred
        );
        
        // Update session
        state.metrics.update_session(&session_id);
        
        // Return the response as before
        Json(ChatResponse {
            response: final_response,
            metadata: ResponseMetadata {
                response_time_ms: elapsed,
                source: "hybrid_with_web_search".to_string(),
                optimization_level: "O(1)".to_string(),
                web_search_used,
            },
            sources,
            fact_check: fact_check_info,
        })
    })
    .await
    {
        Ok(result) => result,
        Err(_) => {
            // Record timeout as an error
            state.metrics.record_request(30000.0, false, false, true);
            Err(StatusCode::REQUEST_TIMEOUT)
        }
    }
}