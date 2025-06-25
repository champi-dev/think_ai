//! Process manager for orchestrating Think AI services

pub mod service;
pub mod proxy;
pub mod port;
pub mod manager;

use thiserror::Error;

#[derive(Error, Debug)]
pub enum ProcessError {
    #[error("Service error: {0}")]
    ServiceError(String),
    
    #[error("Proxy error: {0}")]
    ProxyError(String),
    
    #[error("Port error: {0}")]
    PortError(String),
    
    #[error("IO error: {0}")]
    IoError(#[from] std::io::Error),
}

pub type Result<T> = std::result::Result<T, ProcessError>;