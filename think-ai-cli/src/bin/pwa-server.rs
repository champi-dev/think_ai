use axum::{
    extract::Query,
    http::StatusCode,
    response::{Html, IntoResponse, Json},
    routing::{get, post},
    Router,
};
use serde::{Deserialize, Serialize};
use std::net::SocketAddr;
use think_ai_knowledge::KnowledgeEngine;
use tower_http::cors::CorsLayer;

#[derive(Debug, Deserialize)]
struct ChatQuery {
    message: String,
}

#[derive(Debug, Serialize)]
struct ChatResponse {
    response: String,
}

#[tokio::main]
async fn main() {
    let knowledge_engine = KnowledgeEngine::new();

    let app = Router::new()
        .route("/", get(serve_pwa))
        .route("/manifest.json", get(serve_manifest))
        .route("/service-worker.js", get(serve_sw))
        .route("/api/chat", post(chat_handler))
        .layer(CorsLayer::permissive());

    let addr = SocketAddr::from(([0, 0, 0, 0], 3000));
    println!("PWA Server running at http://localhost:3000");

    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await
        .unwrap();
}

async fn serve_pwa() -> Html<&'static str> {
    Html(include_str!("../../../think-ai-webapp/static/pwa.html"))
}

async fn serve_manifest() -> impl IntoResponse {
    (
        [("content-type", "application/json")],
        include_str!("../../../think-ai-webapp/static/manifest.json"),
    )
}

async fn serve_sw() -> impl IntoResponse {
    (
        [("content-type", "application/javascript")],
        include_str!("../../../think-ai-webapp/static/service-worker.js"),
    )
}

async fn chat_handler(Json(query): Json<ChatQuery>) -> Result<Json<ChatResponse>, StatusCode> {
    Ok(Json(ChatResponse {
        response: format!("Echo: {}", query.message),
    }))
}
