//! Debug Server - Shows all environment variables for Railway debugging

use axum::{
    http::StatusCode,
    response::Html,
    routing::get,
    Json, Router,
};
use serde_json::json;
use std::env;
use tower_http::cors::CorsLayer;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🔍 Debug Think AI Server Starting...");
    
    // Print all environment variables
    println!("📋 Environment Variables:");
    for (key, value) in env::vars() {
        println!("  {}={}", key, value);
    }
    
    // Get port from Railway
    let port = std::env::var("PORT")
        .ok()
        .and_then(|p| p.parse::<u16>().ok())
        .unwrap_or(8080);
    
    println!("🌐 Using port: {}", port);
    
    // Create routes with HEAD support for Railway health checks
    use axum::routing::{any, MethodRouter};
    
    let app = Router::new()
        .route("/", get(root_handler))
        .route("/health", any(health_check_any))
        .route("/healthz", any(health_check_any))  // Alternative health check
        .route("/api/env", get(env_handler))
        .layer(CorsLayer::permissive());
    
    let addr = format!("0.0.0.0:{}", port);
    println!("🌐 Binding to {}", addr);
    
    let listener = tokio::net::TcpListener::bind(&addr).await?;
    println!("✅ Server ready and listening");
    println!("🏥 Health checks available at:");
    println!("   /health");
    println!("   /healthz");
    println!("   /api/env");
    
    axum::serve(listener, app).await?;
    
    Ok(())
}

async fn root_handler() -> Html<String> {
    let port = std::env::var("PORT").unwrap_or_else(|_| "8080".to_string());
    Html(format!(r#"
<!DOCTYPE html>
<html>
<head>
    <title>Think AI Debug Server</title>
</head>
<body>
    <h1>🔍 Think AI Debug Server</h1>
    <p>✅ Server is running on port {}</p>
    <p>🏥 <a href="/health">Health Check</a></p>
    <p>🏥 <a href="/healthz">Health Check (alt)</a></p>
    <p>🌐 <a href="/api/env">Environment Variables</a></p>
    <h2>Quick Tests</h2>
    <button onclick="fetch('/health').then(r=>r.text()).then(t=>alert('Health: '+t))">Test Health</button>
    <button onclick="fetch('/api/env').then(r=>r.json()).then(t=>console.log(t))">Test Env (check console)</button>
</body>
</html>
    "#, port))
}

async fn health_check_any() -> Result<&'static str, StatusCode> {
    println!("🏥 Health check requested (any method) from: {:?}", std::env::var("HTTP_X_FORWARDED_FOR"));
    Ok("OK")
}

async fn env_handler() -> Result<Json<serde_json::Value>, StatusCode> {
    let env_vars: std::collections::HashMap<String, String> = env::vars().collect();
    
    Ok(Json(json!({
        "status": "healthy",
        "server": "debug-think-ai",
        "port": std::env::var("PORT").unwrap_or_else(|_| "8080".to_string()),
        "environment_variables": env_vars,
        "relevant_vars": {
            "PORT": env::var("PORT").ok(),
            "RAILWAY_ENVIRONMENT": env::var("RAILWAY_ENVIRONMENT").ok(),
            "RAILWAY_PROJECT_ID": env::var("RAILWAY_PROJECT_ID").ok(),
            "RAILWAY_SERVICE_ID": env::var("RAILWAY_SERVICE_ID").ok(),
            "HTTP_HOST": env::var("HTTP_HOST").ok(),
            "HOST": env::var("HOST").ok(),
        }
    })))
}