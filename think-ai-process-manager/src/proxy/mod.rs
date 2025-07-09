// O(1) reverse proxy for service routing

pub mod server;
use hyper::{Body, Request, Response, Client};
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::RwLock;
use crate::Result;
/// Route configuration
#[derive(Clone)]
pub struct Route {
    pub path_prefix: String,
    pub target_host: String,
    pub target_port: u16,
}
/// O(1) reverse proxy
pub struct ReverseProxy {
    routes: Arc<RwLock<HashMap<String, Route>>>,
    client: Client<hyper::client::HttpConnector>,
impl ReverseProxy {
    pub fn new() -> Self {
        Self {
            routes: Arc::new(RwLock::new(HashMap::new())),
            client: Client::new(),
        }
    }
    /// Add route (O(1) insertion)
    pub async fn add_route(&self, route: Route) {
        let mut routes = self.routes.write().await;
        routes.insert(route.path_prefix.clone(), route);
    /// Handle request with O(1) routing
    pub async fn handle_request(
        &self,
        req: Request<Body>
    ) -> Result<Response<Body>> {
        let path = req.uri().path();
        let routes = self.routes.read().await;
        // Find matching route (O(1) for exact prefix)
        let route = routes.values()
            .find(|r| path.starts_with(&r.path_prefix))
            .ok_or_else(|| {
                crate::ProcessError::ProxyError(
                    "No route found".to_string()
                )
            })?;
        // Forward request
        let uri = format!(
            "http://{}:{}{}",
            route.target_host,
            route.target_port,
            req.uri()
        );
        let (parts, body) = req.into_parts();
        let mut new_req = Request::from_parts(parts, body);
        *new_req.uri_mut() = uri.parse().unwrap();
        self.client.request(new_req)
            .await
            .map_err(|e| crate::ProcessError::ProxyError(
                format!("Proxy request failed: {}", e)
            ))
