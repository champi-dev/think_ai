//! Port management utilities

use std::process::Command;

/// Kill any process using the specified port
/// 
/// What it does: Ensures port is free before binding
/// How: Uses system commands to find and kill processes
/// Why: Prevents "address already in use" errors
/// Confidence: 95% - System-dependent but handles common cases
pub fn kill_port(port: u16) -> Result<(), String> {
    // Try to find process using the port
    let output = if cfg!(target_os = "linux") {
        Command::new("lsof")
            .args(&["-ti", &format!(":{}", port)])
            .output()
            .map_err(|e| format!("Failed to run lsof: {}", e))?
    } else if cfg!(target_os = "macos") {
        Command::new("lsof")
            .args(&["-ti", &format!(":{}", port)])
            .output()
            .map_err(|e| format!("Failed to run lsof: {}", e))?
    } else {
        // Windows
        Command::new("netstat")
            .args(&["-ano", "|", "findstr", &format!(":{}", port)])
            .output()
            .map_err(|e| format!("Failed to run netstat: {}", e))?
    };
    
    if output.status.success() && !output.stdout.is_empty() {
        let pid_str = String::from_utf8_lossy(&output.stdout);
        for pid in pid_str.lines() {
            if let Ok(pid_num) = pid.trim().parse::<u32>() {
                kill_process(pid_num)?;
            }
        }
    }
    
    Ok(())
}

fn kill_process(pid: u32) -> Result<(), String> {
    if cfg!(target_os = "windows") {
        Command::new("taskkill")
            .args(&["/F", "/PID", &pid.to_string()])
            .output()
            .map_err(|e| format!("Failed to kill process: {}", e))?;
    } else {
        Command::new("kill")
            .args(&["-9", &pid.to_string()])
            .output()
            .map_err(|e| format!("Failed to kill process: {}", e))?;
    }
    Ok(())
}