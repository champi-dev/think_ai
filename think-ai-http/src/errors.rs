// Custom error handling for HTTP requests

use axum::{
    http::StatusCode,
    response::{IntoResponse, Response},
    Json,
};
use serde_json::json;
/// Custom error type for API responses
pub struct ApiError {
    status: StatusCode,
    message: String,
}
impl ApiError {
    pub fn new(status: StatusCode, message: impl Into<String>) -> Self {
        Self {
            status,
            message: message.into(),
        }
    }
    pub fn bad_request(message: impl Into<String>) -> Self {
        Self::new(StatusCode::BAD_REQUEST, message)
    }

    pub fn internal_error(message: impl Into<String>) -> Self {
        Self::new(StatusCode::INTERNAL_SERVER_ERROR, message)
    }
}

impl IntoResponse for ApiError {
    fn into_response(self) -> Response {
        let body = Json(json!({
            "error": self.message,
            "status": self.status.as_u16(),
        }));
        (self.status, body).into_response()
    }
}

/// Handler for JSON parsing errors
pub async fn handle_json_rejection(
    err: axum::extract::rejection::JsonRejection,
) -> impl IntoResponse {
    let message = match err {
        axum::extract::rejection::JsonRejection::JsonDataError(_) => {
            "Invalid JSON format in request body"
        }
        axum::extract::rejection::JsonRejection::MissingJsonContentType(_) => {
            "Missing 'Content-Type: application/json' header"
        }
        _ => "Failed to parse request body",
    };
    ApiError::bad_request(message)
}
