use axum::{
    extract::Extension,
    http::StatusCode,
    response::{Html, IntoResponse},
    routing::{get, get_service},
    Router,
};
use std::net::SocketAddr;
use std::sync::Arc;
use tower_http::services::ServeDir;

pub async fn run_server() -> Result<(), Box<dyn std::error::Error>> {
    let app = Router::new()
        .route("/", get(index_handler))
        .route("/health", get(health_handler))
        .nest_service("/static", get_service(ServeDir::new("static")))
        .fallback(get_service(ServeDir::new("static")));
    let addr = SocketAddr::from(([127, 0, 0, 1], 8080));
    println!("WebApp server listening on http://{}", addr);
    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await?;
    Ok(())
}
async fn index_handler() -> Html<String> {
    Html(include_str!("../../static/index.html").to_string())
async fn health_handler() -> impl IntoResponse {
    (StatusCode::OK, "OK")
