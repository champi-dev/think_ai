use axum::{
    http::StatusCode,
    response::{Html, IntoResponse},
    routing::get,
    Router,
};
use std::net::SocketAddr;
use tower_http::services::ServeDir;

pub async fn run_server() -> Result<(), Box<dyn std::error::Error>> {
    let app = Router::new()
        .route("/", get(index_handler))
        .route("/health", get(health_handler))
        .nest_service("/static", ServeDir::new("think-ai-webapp/static"))
        .fallback_service(ServeDir::new("think-ai-webapp/static"));
    
    let addr = SocketAddr::from(([0, 0, 0, 0], 8080));
    let listener = tokio::net::TcpListener::bind(addr).await?;
    println!("WebApp server listening on http://{}", addr);
    
    axum::serve(listener, app).await?;
    Ok(())
}
async fn index_handler() -> Html<String> {
    Html(include_str!("../../static/index.html").to_string())
}

async fn health_handler() -> impl IntoResponse {
    (StatusCode::OK, "OK")
}
