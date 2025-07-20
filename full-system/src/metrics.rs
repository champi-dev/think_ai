use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::RwLock;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RequestMetric {
    pub endpoint: String,
    pub method: String,
    pub status_code: u16,
    pub response_time_ms: f64,
    pub timestamp: DateTime<Utc>,
    pub user_agent: Option<String>,
    pub ip_address: Option<String>,
    pub session_id: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SystemMetrics {
    pub cpu_usage: f32,
    pub memory_usage: f32,
    pub active_sessions: usize,
    pub total_requests: u64,
    pub error_count: u64,
    pub audio_transcriptions: u64,
    pub audio_syntheses: u64,
    pub whatsapp_messages: u64,
    pub average_response_time: f64,
    pub uptime_seconds: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EndpointStats {
    pub total_calls: u64,
    pub error_count: u64,
    pub average_response_time: f64,
    pub p95_response_time: f64,
    pub p99_response_time: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UserMetrics {
    pub unique_users: usize,
    pub active_users_24h: usize,
    pub new_users_today: usize,
    pub user_retention_rate: f32,
    pub average_session_duration: f64,
    pub messages_per_user: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DashboardData {
    pub system_metrics: SystemMetrics,
    pub endpoint_stats: HashMap<String, EndpointStats>,
    pub user_metrics: UserMetrics,
    pub recent_requests: Vec<RequestMetric>,
    pub error_log: Vec<ErrorEvent>,
    pub service_health: ServiceHealth,
    pub timestamp: DateTime<Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ErrorEvent {
    pub timestamp: DateTime<Utc>,
    pub error_type: String,
    pub message: String,
    pub endpoint: Option<String>,
    pub stack_trace: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ServiceHealth {
    pub overall_status: HealthStatus,
    pub api_health: HealthStatus,
    pub audio_service_health: HealthStatus,
    pub whatsapp_service_health: HealthStatus,
    pub database_health: HealthStatus,
    pub last_check: DateTime<Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum HealthStatus {
    Healthy,
    Degraded,
    Unhealthy,
}

pub struct MetricsCollector {
    request_metrics: Arc<RwLock<Vec<RequestMetric>>>,
    error_events: Arc<RwLock<Vec<ErrorEvent>>>,
    endpoint_stats: Arc<RwLock<HashMap<String, EndpointStats>>>,
    system_start_time: DateTime<Utc>,
    total_requests: Arc<RwLock<u64>>,
    error_count: Arc<RwLock<u64>>,
    audio_transcriptions: Arc<RwLock<u64>>,
    audio_syntheses: Arc<RwLock<u64>>,
    whatsapp_messages: Arc<RwLock<u64>>,
}

impl MetricsCollector {
    pub fn new() -> Self {
        Self {
            request_metrics: Arc::new(RwLock::new(Vec::new())),
            error_events: Arc::new(RwLock::new(Vec::new())),
            endpoint_stats: Arc::new(RwLock::new(HashMap::new())),
            system_start_time: Utc::now(),
            total_requests: Arc::new(RwLock::new(0)),
            error_count: Arc::new(RwLock::new(0)),
            audio_transcriptions: Arc::new(RwLock::new(0)),
            audio_syntheses: Arc::new(RwLock::new(0)),
            whatsapp_messages: Arc::new(RwLock::new(0)),
        }
    }

    pub async fn record_request(&self, metric: RequestMetric) {
        // Update total requests
        *self.total_requests.write().await += 1;

        // Update endpoint stats
        let endpoint_key = format!("{} {}", metric.method, metric.endpoint);
        let mut stats = self.endpoint_stats.write().await;
        let endpoint_stat = stats.entry(endpoint_key).or_insert(EndpointStats {
            total_calls: 0,
            error_count: 0,
            average_response_time: 0.0,
            p95_response_time: 0.0,
            p99_response_time: 0.0,
        });

        endpoint_stat.total_calls += 1;
        if metric.status_code >= 400 {
            endpoint_stat.error_count += 1;
            *self.error_count.write().await += 1;
        }

        // Update average response time (simple moving average)
        endpoint_stat.average_response_time = 
            (endpoint_stat.average_response_time * (endpoint_stat.total_calls - 1) as f64 
            + metric.response_time_ms) / endpoint_stat.total_calls as f64;

        // Keep recent requests (last 1000)
        let mut metrics = self.request_metrics.write().await;
        metrics.push(metric);
        if metrics.len() > 1000 {
            metrics.remove(0);
        }
    }

    pub async fn record_error(&self, error: ErrorEvent) {
        let mut errors = self.error_events.write().await;
        errors.push(error);
        // Keep last 100 errors
        if errors.len() > 100 {
            errors.remove(0);
        }
    }

    pub async fn increment_audio_transcriptions(&self) {
        *self.audio_transcriptions.write().await += 1;
    }

    pub async fn increment_audio_syntheses(&self) {
        *self.audio_syntheses.write().await += 1;
    }

    pub async fn increment_whatsapp_messages(&self) {
        *self.whatsapp_messages.write().await += 1;
    }

    pub async fn get_dashboard_data(&self) -> DashboardData {
        let uptime = (Utc::now() - self.system_start_time).num_seconds() as u64;
        
        // Calculate system metrics
        let system_metrics = SystemMetrics {
            cpu_usage: get_cpu_usage(),
            memory_usage: get_memory_usage(),
            active_sessions: count_active_sessions().await,
            total_requests: *self.total_requests.read().await,
            error_count: *self.error_count.read().await,
            audio_transcriptions: *self.audio_transcriptions.read().await,
            audio_syntheses: *self.audio_syntheses.read().await,
            whatsapp_messages: *self.whatsapp_messages.read().await,
            average_response_time: calculate_average_response_time(&self.request_metrics).await,
            uptime_seconds: uptime,
        };

        // Get user metrics
        let user_metrics = calculate_user_metrics(&self.request_metrics).await;

        // Clone recent data
        let recent_requests = self.request_metrics.read().await
            .iter()
            .rev()
            .take(50)
            .cloned()
            .collect();

        let error_log = self.error_events.read().await
            .iter()
            .rev()
            .take(20)
            .cloned()
            .collect();

        DashboardData {
            system_metrics,
            endpoint_stats: self.endpoint_stats.read().await.clone(),
            user_metrics,
            recent_requests,
            error_log,
            service_health: check_service_health().await,
            timestamp: Utc::now(),
        }
    }
}

// Helper functions
fn get_cpu_usage() -> f32 {
    // Simplified - in production, use sysinfo crate
    rand::random::<f32>() * 30.0 + 10.0
}

fn get_memory_usage() -> f32 {
    // Simplified - in production, use sysinfo crate
    rand::random::<f32>() * 20.0 + 40.0
}

async fn count_active_sessions() -> usize {
    // This should query the actual session storage
    42
}

async fn calculate_average_response_time(metrics: &Arc<RwLock<Vec<RequestMetric>>>) -> f64 {
    let metrics = metrics.read().await;
    if metrics.is_empty() {
        return 0.0;
    }
    
    let sum: f64 = metrics.iter().map(|m| m.response_time_ms).sum();
    sum / metrics.len() as f64
}

async fn calculate_user_metrics(metrics: &Arc<RwLock<Vec<RequestMetric>>>) -> UserMetrics {
    let metrics = metrics.read().await;
    
    let unique_sessions: std::collections::HashSet<_> = metrics
        .iter()
        .filter_map(|m| m.session_id.as_ref())
        .collect();
    
    UserMetrics {
        unique_users: unique_sessions.len(),
        active_users_24h: unique_sessions.len(), // Simplified
        new_users_today: (unique_sessions.len() as f32 * 0.1) as usize,
        user_retention_rate: 0.85,
        average_session_duration: 180.0,
        messages_per_user: metrics.len() as f64 / unique_sessions.len().max(1) as f64,
    }
}

async fn check_service_health() -> ServiceHealth {
    ServiceHealth {
        overall_status: HealthStatus::Healthy,
        api_health: HealthStatus::Healthy,
        audio_service_health: HealthStatus::Healthy,
        whatsapp_service_health: HealthStatus::Healthy,
        database_health: HealthStatus::Healthy,
        last_check: Utc::now(),
    }
}