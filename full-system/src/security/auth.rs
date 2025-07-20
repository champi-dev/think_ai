use axum::{
    extract::{Request, State},
    http::{header, StatusCode},
    middleware::Next,
    response::Response,
};
use jsonwebtoken::{decode, encode, DecodingKey, EncodingKey, Header, Validation};
use serde::{Deserialize, Serialize};
use std::sync::Arc;

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Claims {
    pub sub: String,
    pub exp: usize,
    pub iat: usize,
    pub roles: Vec<String>,
}

#[derive(Clone)]
pub struct AuthConfig {
    pub secret: String,
    pub encoding_key: EncodingKey,
    pub decoding_key: DecodingKey,
}

impl AuthConfig {
    pub fn new(secret: &str) -> Self {
        Self {
            secret: secret.to_string(),
            encoding_key: EncodingKey::from_secret(secret.as_bytes()),
            decoding_key: DecodingKey::from_secret(secret.as_bytes()),
        }
    }

    pub fn create_token(&self, user_id: &str, roles: Vec<String>) -> Result<String, jsonwebtoken::errors::Error> {
        let now = chrono::Utc::now();
        let exp = (now + chrono::Duration::hours(24)).timestamp() as usize;
        let iat = now.timestamp() as usize;

        let claims = Claims {
            sub: user_id.to_string(),
            exp,
            iat,
            roles,
        };

        encode(&Header::default(), &claims, &self.encoding_key)
    }

    pub fn validate_token(&self, token: &str) -> Result<Claims, jsonwebtoken::errors::Error> {
        decode::<Claims>(token, &self.decoding_key, &Validation::default())
            .map(|data| data.claims)
    }
}

pub struct AuthMiddleware;

impl AuthMiddleware {
    pub async fn verify(
        State(auth_config): State<Arc<AuthConfig>>,
        mut request: Request,
        next: Next,
    ) -> Result<Response, StatusCode> {
        let auth_header = request
            .headers()
            .get(header::AUTHORIZATION)
            .and_then(|value| value.to_str().ok());

        let token = match auth_header {
            Some(value) if value.starts_with("Bearer ") => &value[7..],
            _ => return Err(StatusCode::UNAUTHORIZED),
        };

        match auth_config.validate_token(token) {
            Ok(claims) => {
                request.extensions_mut().insert(claims);
                Ok(next.run(request).await)
            }
            Err(_) => Err(StatusCode::UNAUTHORIZED),
        }
    }
}