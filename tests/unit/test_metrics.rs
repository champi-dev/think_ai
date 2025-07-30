use think_ai_full_production::metrics::{MetricsCollector, DashboardData, SystemMetrics};
use std::time::Duration;

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_metrics_collection() {
        let collector = MetricsCollector::new();
        
        // Record some metrics
        collector.record_request_duration("chat", Duration::from_millis(100));
        collector.record_request_duration("chat", Duration::from_millis(200));
        collector.record_request_duration("audio", Duration::from_millis(50));
        
        collector.increment_request_count("chat");
        collector.increment_request_count("chat");
        collector.increment_request_count("audio");
        
        // Get dashboard data
        let dashboard = collector.get_dashboard_data().await;
        
        assert_eq!(dashboard.total_requests, 3);
        assert_eq!(dashboard.requests_by_endpoint.get("chat"), Some(&2));
        assert_eq!(dashboard.requests_by_endpoint.get("audio"), Some(&1));
        
        // Check average response times
        assert!(dashboard.avg_response_time_ms > 0);
    }

    #[tokio::test]
    async fn test_metrics_reset() {
        let collector = MetricsCollector::new();
        
        // Add some data
        collector.increment_request_count("test");
        collector.record_error("test", "error");
        
        let dashboard = collector.get_dashboard_data().await;
        assert_eq!(dashboard.total_requests, 1);
        assert_eq!(dashboard.error_count, 1);
        
        // Reset metrics
        collector.reset().await;
        
        let dashboard = collector.get_dashboard_data().await;
        assert_eq!(dashboard.total_requests, 0);
        assert_eq!(dashboard.error_count, 0);
    }

    #[tokio::test]
    async fn test_concurrent_metrics_updates() {
        let collector = std::sync::Arc::new(MetricsCollector::new());
        let mut handles = vec![];
        
        // Spawn 100 concurrent tasks
        for i in 0..100 {
            let collector_clone = collector.clone();
            let handle = tokio::spawn(async move {
                collector_clone.increment_request_count("concurrent");
                collector_clone.record_request_duration(
                    "concurrent",
                    Duration::from_millis(i as u64)
                );
            });
            handles.push(handle);
        }
        
        for handle in handles {
            handle.await.unwrap();
        }
        
        let dashboard = collector.get_dashboard_data().await;
        assert_eq!(dashboard.total_requests, 100);
        assert_eq!(dashboard.requests_by_endpoint.get("concurrent"), Some(&100));
    }

    #[tokio::test]
    async fn test_error_tracking() {
        let collector = MetricsCollector::new();
        
        collector.record_error("chat", "timeout");
        collector.record_error("chat", "invalid_input");
        collector.record_error("audio", "format_error");
        
        let dashboard = collector.get_dashboard_data().await;
        assert_eq!(dashboard.error_count, 3);
        assert_eq!(dashboard.errors_by_type.get("timeout"), Some(&1));
        assert_eq!(dashboard.errors_by_type.get("invalid_input"), Some(&1));
        assert_eq!(dashboard.errors_by_type.get("format_error"), Some(&1));
    }

    #[tokio::test]
    async fn test_system_metrics() {
        let collector = MetricsCollector::new();
        
        // Update system metrics
        collector.update_system_metrics(SystemMetrics {
            cpu_usage: 45.5,
            memory_usage: 60.2,
            active_connections: 25,
            cache_hit_rate: 0.85,
        }).await;
        
        let dashboard = collector.get_dashboard_data().await;
        assert_eq!(dashboard.system_metrics.cpu_usage, 45.5);
        assert_eq!(dashboard.system_metrics.memory_usage, 60.2);
        assert_eq!(dashboard.system_metrics.active_connections, 25);
        assert_eq!(dashboard.system_metrics.cache_hit_rate, 0.85);
    }

    #[tokio::test]
    async fn test_percentiles() {
        let collector = MetricsCollector::new();
        
        // Add response times from 1ms to 1000ms
        for i in 1..=1000 {
            collector.record_request_duration("test", Duration::from_millis(i));
        }
        
        let dashboard = collector.get_dashboard_data().await;
        
        // P50 should be around 500ms
        assert!(dashboard.response_time_p50 >= 450 && dashboard.response_time_p50 <= 550);
        
        // P95 should be around 950ms
        assert!(dashboard.response_time_p95 >= 900 && dashboard.response_time_p95 <= 970);
        
        // P99 should be around 990ms
        assert!(dashboard.response_time_p99 >= 980 && dashboard.response_time_p99 <= 995);
    }
}