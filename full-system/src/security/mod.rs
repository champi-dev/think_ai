pub mod auth;
pub mod rate_limiter;
pub mod encryption;
pub mod validation;
pub mod headers;

use axum::{
    body::Body,
    extract::{Request, State},
    http::{header, HeaderMap, StatusCode},
    middleware::Next,
    response::Response,
};
use std::sync::Arc;
use tower_http::cors::CorsLayer;

pub use auth::{AuthConfig, AuthMiddleware, Claims};
pub use encryption::EncryptionService;
pub use headers::SecurityHeaders;
pub use rate_limiter::RateLimiter;
pub use validation::InputValidator;

#[derive(Clone)]
pub struct SecurityConfig {
    pub auth_config: AuthConfig,
    pub rate_limiter: Arc<RateLimiter>,
    pub encryption: Arc<EncryptionService>,
    pub validator: Arc<InputValidator>,
}

impl SecurityConfig {
    pub fn new(secret_key: &str) -> Self {
        Self {
            auth_config: AuthConfig::new(secret_key),
            rate_limiter: Arc::new(RateLimiter::new(100, 60)), // 100 requests per minute
            encryption: Arc::new(EncryptionService::new()),
            validator: Arc::new(InputValidator::new()),
        }
    }

    pub fn cors_layer() -> CorsLayer {
        CorsLayer::new()
            .allow_origin(tower_http::cors::Any)
            .allow_methods(vec![
                axum::http::Method::GET,
                axum::http::Method::POST,
                axum::http::Method::OPTIONS,
            ])
            .allow_headers(vec![
                header::CONTENT_TYPE,
                header::AUTHORIZATION,
                header::ACCEPT,
            ])
            .max_age(std::time::Duration::from_secs(3600))
    }
}

pub async fn security_middleware(
    State(config): State<Arc<SecurityConfig>>,
    mut request: Request,
    next: Next,
) -> Result<Response, StatusCode> {
    // Apply security headers
    let mut response = next.run(request).await;
    SecurityHeaders::apply(&mut response);
    
    Ok(response)
}