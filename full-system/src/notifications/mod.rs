pub mod whatsapp;

use async_trait::async_trait;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Notification {
    pub title: String,
    pub message: String,
    pub severity: NotificationSeverity,
    pub timestamp: chrono::DateTime<chrono::Utc>,
    pub metadata: Option<serde_json::Value>,
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize)]
pub enum NotificationSeverity {
    Info,
    Warning,
    Error,
    Critical,
}

#[async_trait]
pub trait NotificationService: Send + Sync {
    async fn send(&self, notification: &Notification) -> Result<(), Box<dyn std::error::Error>>;
}