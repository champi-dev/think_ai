//! Port killing utilities

use std::process::Command;
use crate::Result;

/// Kill process using a port
/// 
/// What it does: Terminates process bound to port
/// How: Uses lsof/netstat to find and kill process
/// Why: Ensures clean port binding
/// Confidence: 95% - Platform-specific commands
pub fn kill_port(port: u16) -> Result<()> {
    #[cfg(target_os = "linux")]
    {
        // Find process using the port
        let output = Command::new("lsof")
            .args(&["-ti", &format!(":{}", port)])
            .output()?;
        
        if !output.stdout.is_empty() {
            let pid = String::from_utf8_lossy(&output.stdout)
                .trim()
                .to_string();
            
            // Kill the process
            Command::new("kill")
                .args(&["-9", &pid])
                .output()?;
        }
    }
    
    #[cfg(target_os = "macos")]
    {
        // Similar to Linux
        let output = Command::new("lsof")
            .args(&["-ti", &format!(":{}", port)])
            .output()?;
        
        if !output.stdout.is_empty() {
            let pid = String::from_utf8_lossy(&output.stdout)
                .trim()
                .to_string();
            
            Command::new("kill")
                .args(&["-9", &pid])
                .output()?;
        }
    }
    
    Ok(())
}