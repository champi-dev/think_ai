use super::{Notification, NotificationService};
use async_trait::async_trait;
use reqwest::Client;
use serde_json::json;
use std::env;

pub struct WhatsAppNotifier {
    client: Client,
    api_url: String,
    phone_number: String,
    api_key: String,
}

impl WhatsAppNotifier {
    pub fn new() -> Option<Self> {
        let api_key = env::var("WHATSAPP_API_KEY").ok()?;
        let phone_number = env::var("WHATSAPP_PHONE_NUMBER").ok()?;
        let api_url = env::var("WHATSAPP_API_URL")
            .unwrap_or_else(|_| "https://api.whatsapp.com/v1/messages".to_string());

        Some(Self {
            client: Client::new(),
            api_url,
            phone_number,
            api_key,
        })
    }

    pub fn with_twilio() -> Option<Self> {
        let account_sid = env::var("TWILIO_ACCOUNT_SID").ok()?;
        let auth_token = env::var("TWILIO_AUTH_TOKEN").ok()?;
        let from_number = env::var("TWILIO_WHATSAPP_FROM").ok()?;
        let to_number = env::var("WHATSAPP_TO_NUMBER").ok()?;

        let client = Client::builder()
            .basic_auth(&account_sid, Some(&auth_token))
            .build()
            .ok()?;

        Some(Self {
            client,
            api_url: format!(
                "https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json",
                account_sid
            ),
            phone_number: to_number,
            api_key: auth_token,
        })
    }

    fn format_message(&self, notification: &Notification) -> String {
        let emoji = match notification.severity {
            super::NotificationSeverity::Info => "ℹ️",
            super::NotificationSeverity::Warning => "⚠️",
            super::NotificationSeverity::Error => "❌",
            super::NotificationSeverity::Critical => "🚨",
        };

        format!(
            "{} *ThinkAI Alert*\n\n*{}*\n\n{}\n\n_Time: {}_",
            emoji,
            notification.title,
            notification.message,
            notification.timestamp.format("%Y-%m-%d %H:%M:%S UTC")
        )
    }
}

#[async_trait]
impl NotificationService for WhatsAppNotifier {
    async fn send(&self, notification: &Notification) -> Result<(), Box<dyn std::error::Error>> {
        let message = self.format_message(notification);

        // For Twilio
        if self.api_url.contains("twilio") {
            let params = [
                ("From", format!("whatsapp:{}", env::var("TWILIO_WHATSAPP_FROM")?)),
                ("To", format!("whatsapp:{}", self.phone_number)),
                ("Body", message),
            ];

            let response = self.client
                .post(&self.api_url)
                .form(&params)
                .send()
                .await?;

            if !response.status().is_success() {
                return Err(format!("WhatsApp send failed: {}", response.status()).into());
            }
        } else {
            // Generic WhatsApp Business API
            let payload = json!({
                "to": self.phone_number,
                "type": "text",
                "text": {
                    "body": message
                }
            });

            let response = self.client
                .post(&self.api_url)
                .header("Authorization", format!("Bearer {}", self.api_key))
                .json(&payload)
                .send()
                .await?;

            if !response.status().is_success() {
                return Err(format!("WhatsApp send failed: {}", response.status()).into());
            }
        }

        Ok(())
    }
}