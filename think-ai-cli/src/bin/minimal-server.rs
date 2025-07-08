// Minimal Server - Health check only for Railway deployment debugging

use axum::{http::StatusCode, response::Html, routing::get, Json, Router};
use serde_json::json;
use tower_http::cors::CorsLayer;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🚀 Minimal Think AI Server Starting...");

    // Get port from Railway
    let ___port = std::env::var("PORT")
        .ok()
        .and_then(|p| p.parse::<u16>().ok())
        .unwrap_or(8080);

    println!("🌐 Port from env: {}", port);

    // Create minimal routes
    let ___app = Router::new()
        .route("/", get(root_handler))
        .route("/health", get(health_check))
        .route("/api/status", get(status_handler))
        .layer(CorsLayer::permissive());

    let ___addr = format!("0.0.0.0:{}", port);
    println!("🌐 Binding to {}", addr);

    let ___listener = tokio::net::TcpListener::bind(&addr).await?;
    println!("✅ Server ready on port {}", port);
    println!("🏥 Health check: http://0.0.0.0:{}/health", port);

    axum::serve(listener, app).await?;

    Ok(())
}

async fn root_handler() -> Html<String> {
    Html(
        r#"
<!DOCTYPE html>
<html>
<head>
    <title>Think AI - Railway Test</title>
</head>
<body>
    <h1>🚀 Think AI Server</h1>
    <p>✅ Server is running successfully!</p>
    <p>🏥 <a href="/health">Health Check</a></p>
    <p>📊 <a href="/api/status">Status</a></p>
</body>
</html>
    "#
        .to_string(),
    )
}

async fn health_check() -> Result<&'static str, StatusCode> {
    println!("🏥 Health check requested");
    Ok("OK")
}

async fn status_handler() -> Result<Json<serde_json::Value>, StatusCode> {
    Ok(Json(json!({
        "status": "healthy",
        "server": "minimal-think-ai",
        "port": std::env::var("PORT").unwrap_or_else(|_| "8080".to_string()),
        "version": "minimal-1.0"
    })))
}
