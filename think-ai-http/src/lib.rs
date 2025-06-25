//! Think AI HTTP - Functional HTTP server framework

pub mod server;
pub mod router;
pub mod handlers;

use thiserror::Error;

#[derive(Error, Debug)]
pub enum HttpError {
    #[error("Server error: {0}")]
    ServerError(String),
}

pub type Result<T> = std::result::Result<T, HttpError>;