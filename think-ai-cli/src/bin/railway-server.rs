use std::env;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Initialize logging
    tracing_subscriber::fmt::init();

    // Get port from environment or use default
    let port = env::var("PORT")
        .ok()
        .and_then(|p| p.parse::<u16>().ok())
        .unwrap_or(8080);

    // Always bind to 0.0.0.0 for cloud deployments
    let host = "0.0.0.0";

    println!("🚀 Think AI Server starting on {}:{}", host, port);

    // Create a simple HTTP server
    let app = axum::Router::new()
        .route("/", axum::routing::get(root_handler))
        .route("/api/health", axum::routing::get(health_handler))
        .route("/api/chat", axum::routing::post(chat_handler));

    let addr = std::net::SocketAddr::from(([0, 0, 0, 0], port));

    println!("🌐 Server listening on http://{}", addr);

    let listener = tokio::net::TcpListener::bind(&addr).await?;
    axum::serve(listener, app).await?;

    Ok(())
}

async fn root_handler() -> &'static str {
    "Think AI Server - O(1) AI System"
}

async fn health_handler() -> impl axum::response::IntoResponse {
    axum::Json(serde_json::json!({
        "status": "ok",
        "service": "think-ai",
        "version": "0.1.0"
    }))
}

async fn chat_handler(
    axum::Json(payload): axum::Json<serde_json::Value>,
) -> impl axum::response::IntoResponse {
    let query = payload
        .get("query")
        .and_then(|v| v.as_str())
        .unwrap_or("Hello");

    // Simple response for now
    let response = format!("Think AI received: {}", query);

    axum::Json(serde_json::json!({
        "response": response,
        "time_ms": 0.002
    }))
}
