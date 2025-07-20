use axum::{
    body::Body,
    extract::Request,
    http::{Response, StatusCode},
    middleware::Next,
};
use chrono::Utc;
use std::time::Instant;

use crate::metrics::RequestMetric;

pub async fn metrics_middleware(
    req: Request,
    next: Next,
) -> Result<Response<Body>, StatusCode> {
    let start = Instant::now();
    let method = req.method().to_string();
    let uri = req.uri().path().to_string();
    
    // Extract metadata
    let user_agent = req
        .headers()
        .get("user-agent")
        .and_then(|v| v.to_str().ok())
        .map(|s| s.to_string());
    
    let ip_address = req
        .headers()
        .get("x-forwarded-for")
        .and_then(|v| v.to_str().ok())
        .map(|s| s.to_string())
        .or_else(|| {
            req.headers()
                .get("x-real-ip")
                .and_then(|v| v.to_str().ok())
                .map(|s| s.to_string())
        });
    
    // Extract session ID from cookie or header
    let session_id = req
        .headers()
        .get("x-session-id")
        .and_then(|v| v.to_str().ok())
        .map(|s| s.to_string());
    
    // Process request
    let response = next.run(req).await;
    
    let elapsed = start.elapsed();
    let status = response.status().as_u16();
    
    // Record metric if we have access to metrics collector
    // This would need to be passed through app state
    let _metric = RequestMetric {
        endpoint: uri,
        method,
        status_code: status,
        response_time_ms: elapsed.as_secs_f64() * 1000.0,
        timestamp: Utc::now(),
        user_agent,
        ip_address,
        session_id,
    };
    
    // TODO: Actually record the metric
    // metrics_collector.record_request(metric).await;
    
    Ok(response)
}