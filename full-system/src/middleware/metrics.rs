use axum::{
    body::Body,
    extract::Request,
    http::Response,
};
use chrono::Utc;
use std::time::Instant;
use std::sync::Arc;
use tower::{Layer, Service};
use std::task::{Context, Poll};
use std::future::Future;
use std::pin::Pin;

use crate::metrics::{RequestMetric, MetricsCollector};

#[derive(Clone)]
pub struct MetricsLayer {
    metrics_collector: Arc<MetricsCollector>,
}

impl MetricsLayer {
    pub fn new(metrics_collector: Arc<MetricsCollector>) -> Self {
        Self { metrics_collector }
    }
}

impl<S> Layer<S> for MetricsLayer {
    type Service = MetricsMiddleware<S>;

    fn layer(&self, inner: S) -> Self::Service {
        MetricsMiddleware {
            inner,
            metrics_collector: self.metrics_collector.clone(),
        }
    }
}

#[derive(Clone)]
pub struct MetricsMiddleware<S> {
    inner: S,
    metrics_collector: Arc<MetricsCollector>,
}

impl<S> Service<Request> for MetricsMiddleware<S>
where
    S: Service<Request, Response = Response<Body>> + Send + 'static,
    S::Future: Send + 'static,
{
    type Response = S::Response;
    type Error = S::Error;
    type Future = Pin<Box<dyn Future<Output = Result<Self::Response, Self::Error>> + Send>>;

    fn poll_ready(&mut self, cx: &mut Context<'_>) -> Poll<Result<(), Self::Error>> {
        self.inner.poll_ready(cx)
    }

    fn call(&mut self, req: Request) -> Self::Future {
        let start = Instant::now();
        let method = req.method().to_string();
        let uri = req.uri().path().to_string();
        
        // Extract metadata
        let user_agent = req
            .headers()
            .get("user-agent")
            .and_then(|v| v.to_str().ok())
            .map(|s| s.to_string());
        
        let ip_address = req
            .headers()
            .get("x-forwarded-for")
            .and_then(|v| v.to_str().ok())
            .map(|s| s.to_string())
            .or_else(|| {
                req.headers()
                    .get("x-real-ip")
                    .and_then(|v| v.to_str().ok())
                    .map(|s| s.to_string())
            });
        
        // Extract session ID from cookie or header
        let session_id = req
            .headers()
            .get("x-session-id")
            .and_then(|v| v.to_str().ok())
            .map(|s| s.to_string());
        
        let metrics_collector = self.metrics_collector.clone();
        let future = self.inner.call(req);
        
        Box::pin(async move {
            let response = future.await?;
            
            let elapsed = start.elapsed();
            let status = response.status().as_u16();
            
            // Record the metric
            let metric = RequestMetric {
                endpoint: uri,
                method,
                status_code: status,
                response_time_ms: elapsed.as_secs_f64() * 1000.0,
                timestamp: Utc::now(),
                user_agent,
                ip_address,
                session_id,
            };
            
            // Record the metric to the collector
            metrics_collector.record_request(metric).await;
            
            Ok(response)
        })
    }
}