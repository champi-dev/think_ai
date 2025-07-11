// SSE (Server-Sent Events) streaming chat handler

use crate::router::AppState;
use axum::{
    extract::State,
    response::{
        sse::{Event, KeepAlive, Sse},
        IntoResponse,
    },
    Json,
};
use futures::{stream::{self, Stream}, StreamExt};
use serde::{Deserialize, Serialize};
use std::{convert::Infallible, sync::Arc, time::Duration};
use tokio::time::sleep;
use uuid::Uuid;

#[derive(Debug, Deserialize)]
pub struct StreamChatRequest {
    message: String,
    #[serde(default)]
    session_id: Option<String>,
}

#[derive(Debug, Serialize)]
pub struct StreamChunk {
    chunk: String,
    done: bool,
    #[serde(skip_serializing_if = "Option::is_none")]
    session_id: Option<String>,
}

pub async fn stream_chat(
    State(state): State<Arc<AppState>>,
    Json(request): Json<StreamChatRequest>,
) -> Sse<impl Stream<Item = Result<Event, Infallible>>> {
    let session_id = request
        .session_id
        .unwrap_or_else(|| Uuid::new_v4().to_string());

    // Simulate streaming response with O(1) performance insights
    let response_parts = vec![
        "I'm processing your request",
        " using O(1) algorithms.",
        "\n\nThis ensures",
        " constant-time performance",
        " regardless of input size.",
        "\n\nEach chunk",
        " is delivered instantly",
        " through Server-Sent Events,",
        " providing a smooth",
        " streaming experience.",
    ];

    let stream = stream::iter(response_parts.into_iter().enumerate())
        .then(move |(index, chunk)| {
            let session_id = session_id.clone();
            async move {
                // Simulate processing time
                sleep(Duration::from_millis(200)).await;
                
                let is_last = index == 9;
                let data = StreamChunk {
                    chunk: chunk.to_string(),
                    done: is_last,
                    session_id: if is_last { Some(session_id) } else { None },
                };
                
                Ok(Event::default()
                    .data(serde_json::to_string(&data).unwrap())
                    .retry(Duration::from_secs(1)))
            }
        });

    Sse::new(stream).keep_alive(KeepAlive::default())
}

// Alternative implementation using actual response generation
pub async fn stream_chat_real(
    State(state): State<Arc<AppState>>,
    Json(request): Json<StreamChatRequest>,
) -> impl IntoResponse {
    let session_id = request
        .session_id
        .unwrap_or_else(|| Uuid::new_v4().to_string());

    // Generate response using the knowledge engine
    let response = state
        .knowledge_engine
        .generate_llm_response(&request.message);

    // Split response into owned words for streaming
    let words: Vec<String> = response
        .split_whitespace()
        .map(|s| s.to_string())
        .collect();
    let total_words = words.len();
    
    let stream = stream::iter(words.into_iter().enumerate())
        .then(move |(index, word)| {
            let session_id = session_id.clone();
            async move {
                // Faster streaming for better UX
                sleep(Duration::from_millis(50)).await;
                
                let is_last = index == total_words - 1;
                let chunk = if index == 0 {
                    word.to_string()
                } else {
                    format!(" {}", word)
                };
                
                let data = StreamChunk {
                    chunk,
                    done: is_last,
                    session_id: if is_last { Some(session_id) } else { None },
                };
                
                Ok::<_, Infallible>(
                    Event::default()
                        .data(serde_json::to_string(&data).unwrap())
                        .retry(Duration::from_secs(1))
                )
            }
        });

    Sse::new(stream).keep_alive(KeepAlive::default())
}