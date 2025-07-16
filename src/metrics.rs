// Metrics module for tracking usage statistics
use std::sync::{Arc, RwLock};
use std::time::{SystemTime, UNIX_EPOCH, Instant};
use std::collections::HashMap;
use serde::{Serialize, Deserialize};
use chrono::{DateTime, Utc, Local};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UsageStats {
    pub total_requests: u64,
    pub requests_today: u64,
    pub web_searches_today: u64,
    pub fact_checks_today: u64,
    pub errors_today: u64,
    pub active_sessions: usize,
    pub avg_response_time_ms: f64,
    pub hourly_activity: Vec<u64>,
    pub last_reset: DateTime<Utc>,
}

#[derive(Debug, Clone)]
pub struct MetricsCollector {
    stats: Arc<RwLock<UsageStats>>,
    response_times: Arc<RwLock<Vec<f64>>>,
    start_time: Instant,
    active_sessions: Arc<RwLock<HashMap<String, Instant>>>,
}

impl MetricsCollector {
    pub fn new() -> Self {
        Self {
            stats: Arc::new(RwLock::new(UsageStats {
                total_requests: 0,
                requests_today: 0,
                web_searches_today: 0,
                fact_checks_today: 0,
                errors_today: 0,
                active_sessions: 0,
                avg_response_time_ms: 0.0,
                hourly_activity: vec![0; 24],
                last_reset: Utc::now(),
            })),
            response_times: Arc::new(RwLock::new(Vec::new())),
            start_time: Instant::now(),
            active_sessions: Arc::new(RwLock::new(HashMap::new())),
        }
    }
    
    pub fn record_request(&self, response_time_ms: f64, used_web_search: bool, used_fact_check: bool, error: bool) {
        let mut stats = self.stats.write().unwrap();
        let mut response_times = self.response_times.write().unwrap();
        
        // Check if we need to reset daily stats
        let now = Utc::now();
        if now.date_naive() != stats.last_reset.date_naive() {
            stats.requests_today = 0;
            stats.web_searches_today = 0;
            stats.fact_checks_today = 0;
            stats.errors_today = 0;
            stats.hourly_activity = vec![0; 24];
            stats.last_reset = now;
            response_times.clear();
        }
        
        // Update stats
        stats.total_requests += 1;
        stats.requests_today += 1;
        
        if used_web_search {
            stats.web_searches_today += 1;
        }
        
        if used_fact_check {
            stats.fact_checks_today += 1;
        }
        
        if error {
            stats.errors_today += 1;
        }
        
        // Update hourly activity
        let current_hour = Local::now().hour() as usize;
        if current_hour < 24 {
            stats.hourly_activity[current_hour] += 1;
        }
        
        // Update response times
        response_times.push(response_time_ms);
        if response_times.len() > 1000 {
            response_times.remove(0);
        }
        
        // Calculate average response time
        if !response_times.is_empty() {
            let sum: f64 = response_times.iter().sum();
            stats.avg_response_time_ms = sum / response_times.len() as f64;
        }
    }
    
    pub fn add_session(&self, session_id: String) {
        let mut sessions = self.active_sessions.write().unwrap();
        sessions.insert(session_id, Instant::now());
        
        // Clean up old sessions (older than 30 minutes)
        let cutoff = Instant::now() - std::time::Duration::from_secs(30 * 60);
        sessions.retain(|_, last_seen| *last_seen > cutoff);
        
        // Update active sessions count
        let mut stats = self.stats.write().unwrap();
        stats.active_sessions = sessions.len();
    }
    
    pub fn update_session(&self, session_id: &str) {
        let mut sessions = self.active_sessions.write().unwrap();
        if let Some(last_seen) = sessions.get_mut(session_id) {
            *last_seen = Instant::now();
        }
    }
    
    pub fn get_stats(&self) -> UsageStats {
        self.stats.read().unwrap().clone()
    }
    
    pub fn get_uptime_seconds(&self) -> u64 {
        self.start_time.elapsed().as_secs()
    }
}