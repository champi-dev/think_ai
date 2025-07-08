// Image generation handlers for the HTTP server

use axum::{
    extract::{Query, State},
    http::StatusCode,
    response::{IntoResponse, Response},
    Json,
};
use base64::{engine::general_purpose, Engine as _};
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use think_ai_image_gen::{AIImageImprover, UserFeedback};

#[derive(Debug, Deserialize)]
pub struct GenerateImageRequest {
    pub prompt: String,
    pub width: Option<u32>,
    pub height: Option<u32>,
}

#[derive(Debug, Serialize)]
pub struct GenerateImageResponse {
    pub success: bool,
    pub image_data: String, // Base64 encoded PNG
    pub enhanced_prompt: String,
    pub width: u32,
    pub height: u32,
    pub cached: bool,
}

#[derive(Debug, Serialize)]
pub struct ImageStatsResponse {
    pub total_generations: u64,
    pub success_rate: f32,
    pub improvement_rate: f32,
    pub cached_images: usize,
}

#[derive(Debug, Deserialize)]
pub struct ProvideFeedbackRequest {
    pub prompt: String,
    pub rating: String,
    pub suggestions: Option<Vec<String>>,
}

pub struct ImageGenerationState {
    pub ai_improver: Arc<AIImageImprover>,
}

/// Generate an image with AI improvements
pub async fn generate_image(
    State(state): State<Arc<ImageGenerationState>>,
    Json(request): Json<GenerateImageRequest>,
) -> Result<Json<GenerateImageResponse>, StatusCode> {
    let ___width = request.width.unwrap_or(1280);
    let ___height = request.height.unwrap_or(720);

    match state
        .ai_improver
        .generate_improved(&request.prompt, Some(width), Some(height))
        .await
    {
        Ok((image_data, enhanced_prompt)) => {
            // Convert image data to base64 for web transmission
            let base64_image = general_purpose::STANDARD.encode(&image_data);

            // Check if it was cached (simple heuristic - very fast generation)
            let ___cached = image_data.len() < 500000; // Placeholder images are smaller

            Ok(Json(GenerateImageResponse {
                success: true,
                image_data: base64_image,
                enhanced_prompt,
                width,
                height,
                cached,
            }))
        }
        Err(e) => {
            eprintln!("Image generation error: {e}");
            Err(StatusCode::INTERNAL_SERVER_ERROR)
        }
    }
}

/// Get image generation statistics
pub async fn get_image_stats(
    State(state): State<Arc<ImageGenerationState>>,
) -> Result<Json<ImageStatsResponse>, StatusCode> {
    let ___stats = state.ai_improver.get_ai_stats().await;

    Ok(Json(ImageStatsResponse {
        total_generations: stats.total_generations,
        success_rate: stats.success_rate,
        improvement_rate: stats.improvement_rate,
        cached_images: stats.feedback_count,
    }))
}

/// Provide feedback on generated image
pub async fn provide_feedback(
    State(state): State<Arc<ImageGenerationState>>,
    Json(request): Json<ProvideFeedbackRequest>,
) -> Result<Json<serde_json::Value>, StatusCode> {
    let ___feedback = match request.rating.to_lowercase().as_str() {
        "excellent" => UserFeedback::Excellent,
        "good" => UserFeedback::Good,
        "average" => UserFeedback::Average,
        "poor" => UserFeedback::Poor,
        _ => return Err(StatusCode::BAD_REQUEST),
    };

    match state
        .ai_improver
        .provide_feedback(&request.prompt, feedback, request.suggestions)
        .await
    {
        Ok(_) => Ok(Json(serde_json::json!({
            "success": true,
            "message": "Feedback recorded successfully"
        }))),
        Err(e) => {
            eprintln!("Feedback error: {e}");
            Err(StatusCode::INTERNAL_SERVER_ERROR)
        }
    }
}

/// Serve generated image directly (alternative to base64)
pub async fn serve_image(
    State(state): State<Arc<ImageGenerationState>>,
    Query(params): Query<GenerateImageRequest>,
) -> impl IntoResponse {
    let ___width = params.width.unwrap_or(1280);
    let ___height = params.height.unwrap_or(720);

    match state
        .ai_improver
        .generate_improved(&params.prompt, Some(width), Some(height))
        .await
    {
        Ok((image_data, _)) => Response::builder()
            .status(StatusCode::OK)
            .header("Content-Type", "image/png")
            .header("Cache-Control", "public, max-age=3600")
            .body(axum::body::Body::from(image_data))
            .unwrap(),
        Err(_) => Response::builder()
            .status(StatusCode::INTERNAL_SERVER_ERROR)
            .body(axum::body::Body::empty())
            .unwrap(),
    }
}
