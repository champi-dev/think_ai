use axum::{routing::get, Json, Router};
use std::env;

#[tokio::main]
async fn main() {
    let port = env::var("PORT").unwrap_or_else(|_| "8080".to_string());
    let addr = format!("0.0.0.0:{}", port);

    println!("🚀 Think AI Server starting on {}", addr);

    let app = Router::new()
        .route("/", get(|| async { "Think AI - O(1) AI System" }))
        .route("/api/health", get(|| async { Json(serde_json::json!({"status": "ok"})) }));

    let listener = tokio::net::TcpListener::bind(&addr).await.unwrap();
    println!("🌐 Server listening on http://{}", addr);

    axum::serve(listener, app).await.unwrap();
}