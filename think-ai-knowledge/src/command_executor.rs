// Safe Command Executor for Autonomous Agent
//!
//! Provides safe, sandboxed command execution with security constraints
//! Ensures the agent cannot interfere with critical system processes

use async_trait::async_trait;
use std::collections::HashMap;
use std::path::{Path, PathBuf};
use std::process::Stdio;
use std::sync::Arc;
use std::time::Duration;
use tokio::process::Command;
use tokio::sync::{Mutex, RwLock};
use tokio::time::timeout;
use tracing::{debug, error, info, warn};

/// Security policy for command execution
#[derive(Debug, Clone)]
pub struct SecurityPolicy {
    /// Allowed commands (whitelist)
    pub allowed_commands: Vec<String>,
    
    /// Forbidden paths
    pub forbidden_paths: Vec<PathBuf>,
    
    /// Allowed working directories
    pub allowed_directories: Vec<PathBuf>,
    
    /// Environment variable restrictions
    pub env_restrictions: HashMap<String, String>,
    
    /// Maximum execution time
    pub max_execution_time: Duration,
    
    /// Maximum output size in bytes
    pub max_output_size: usize,
    
    /// Rate limiting
    pub rate_limit_per_minute: usize,
}

impl Default for SecurityPolicy {
    fn default() -> Self {
        Self {
            allowed_commands: vec![
                "ls".to_string(),
                "cat".to_string(),
                "echo".to_string(),
                "pwd".to_string(),
                "date".to_string(),
                "whoami".to_string(),
                "cargo".to_string(),
                "rustc".to_string(),
                "python3".to_string(),
                "node".to_string(),
                "git".to_string(),
                "curl".to_string(),
                "grep".to_string(),
                "sed".to_string(),
                "awk".to_string(),
                "find".to_string(),
                "wc".to_string(),
                "sort".to_string(),
                "uniq".to_string(),
                "head".to_string(),
                "tail".to_string(),
            ],
            forbidden_paths: vec![
                PathBuf::from("/etc"),
                PathBuf::from("/sys"),
                PathBuf::from("/proc"),
                PathBuf::from("/boot"),
                PathBuf::from("/root"),
                PathBuf::from("/usr/bin/sudo"),
                PathBuf::from("/usr/bin/su"),
            ],
            allowed_directories: vec![
                PathBuf::from("/tmp"),
                PathBuf::from("./workspace"),
                PathBuf::from("./knowledge"),
                PathBuf::from("./logs"),
            ],
            env_restrictions: HashMap::new(),
            max_execution_time: Duration::from_secs(30),
            max_output_size: 1024 * 1024, // 1MB
            rate_limit_per_minute: 60,
        }
    }
}

/// Command execution result
#[derive(Debug, Clone)]
pub struct ExecutionResult {
    pub command: String,
    pub args: Vec<String>,
    pub stdout: String,
    pub stderr: String,
    pub exit_code: Option<i32>,
    pub execution_time: Duration,
    pub truncated: bool,
}

/// Safe command executor
pub struct CommandExecutor {
    /// Security policy
    policy: Arc<RwLock<SecurityPolicy>>,
    
    /// Execution history
    history: Arc<Mutex<Vec<ExecutionResult>>>,
    
    /// Rate limiter
    rate_limiter: Arc<Mutex<RateLimiter>>,
}

struct RateLimiter {
    executions: Vec<u64>,
    window_start: std::time::Instant,
}

impl CommandExecutor {
    /// Create new command executor
    pub fn new(policy: Option<SecurityPolicy>) -> Self {
        Self {
            policy: Arc::new(RwLock::new(policy.unwrap_or_default())),
            history: Arc::new(Mutex::new(Vec::new())),
            rate_limiter: Arc::new(Mutex::new(RateLimiter {
                executions: Vec::new(),
                window_start: std::time::Instant::now(),
            })),
        }
    }
    
    /// Execute a command safely
    pub async fn execute(
        &self,
        command: &str,
        args: &[String],
        working_dir: Option<&Path>,
    ) -> Result<ExecutionResult, String> {
        // Check rate limit
        self.check_rate_limit().await?;
        
        // Validate command
        self.validate_command(command, args, working_dir).await?;
        
        // Prepare command
        let mut cmd = Command::new(command);
        cmd.args(args)
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .stdin(Stdio::null()); // Prevent interactive commands
        
        // Set working directory if provided
        if let Some(dir) = working_dir {
            cmd.current_dir(dir);
        }
        
        // Apply environment restrictions
        let policy = self.policy.read().await;
        for (key, value) in &policy.env_restrictions {
            cmd.env(key, value);
        }
        
        let max_time = policy.max_execution_time;
        let max_output = policy.max_output_size;
        drop(policy);
        
        // Execute with timeout
        let start_time = std::time::Instant::now();
        let result = match timeout(max_time, cmd.output()).await {
            Ok(Ok(output)) => {
                let stdout = String::from_utf8_lossy(&output.stdout);
                let stderr = String::from_utf8_lossy(&output.stderr);
                
                // Truncate if necessary
                let (stdout_str, stderr_str, truncated) = if stdout.len() + stderr.len() > max_output {
                    (
                        stdout.chars().take(max_output / 2).collect(),
                        stderr.chars().take(max_output / 2).collect(),
                        true,
                    )
                } else {
                    (stdout.to_string(), stderr.to_string(), false)
                };
                
                ExecutionResult {
                    command: command.to_string(),
                    args: args.to_vec(),
                    stdout: stdout_str,
                    stderr: stderr_str,
                    exit_code: output.status.code(),
                    execution_time: start_time.elapsed(),
                    truncated,
                }
            }
            Ok(Err(e)) => {
                return Err(format!("Command execution failed: {}", e));
            }
            Err(_) => {
                return Err("Command execution timed out".to_string());
            }
        };
        
        // Record execution
        self.history.lock().await.push(result.clone());
        
        info!(
            "Executed command: {} {} (exit: {:?}, time: {:?})",
            command,
            args.join(" "),
            result.exit_code,
            result.execution_time
        );
        
        Ok(result)
    }
    
    /// Execute a shell script safely
    pub async fn execute_script(&self, script: &str) -> Result<ExecutionResult, String> {
        // Validate script content
        self.validate_script(script).await?;
        
        // Create temporary script file
        let script_path = format!("/tmp/agent_script_{}.sh", uuid::Uuid::new_v4());
        tokio::fs::write(&script_path, script).await
            .map_err(|e| format!("Failed to write script: {}", e))?;
        
        // Make executable
        self.execute("chmod", &["+x".to_string(), script_path.clone()], None).await?;
        
        // Execute script
        let result = self.execute("bash", &[script_path.clone()], None).await;
        
        // Clean up
        let _ = tokio::fs::remove_file(&script_path).await;
        
        result
    }
    
    /// Check rate limit
    async fn check_rate_limit(&self) -> Result<(), String> {
        let mut limiter = self.rate_limiter.lock().await;
        let policy = self.policy.read().await;
        let limit = policy.rate_limit_per_minute;
        drop(policy);
        
        // Clean old entries
        let now = std::time::Instant::now();
        if now.duration_since(limiter.window_start) > Duration::from_secs(60) {
            limiter.executions.clear();
            limiter.window_start = now;
        }
        
        // Check limit
        if limiter.executions.len() >= limit {
            return Err("Rate limit exceeded".to_string());
        }
        
        limiter.executions.push(
            std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_secs()
        );
        
        Ok(())
    }
    
    /// Validate command against security policy
    async fn validate_command(
        &self,
        command: &str,
        args: &[String],
        working_dir: Option<&Path>,
    ) -> Result<(), String> {
        let policy = self.policy.read().await;
        
        // Check if command is allowed
        let base_command = Path::new(command)
            .file_name()
            .and_then(|s| s.to_str())
            .unwrap_or(command);
        
        if !policy.allowed_commands.contains(&base_command.to_string()) {
            return Err(format!("Command '{}' is not allowed", command));
        }
        
        // Check for forbidden paths in arguments
        for arg in args {
            let path = Path::new(arg);
            for forbidden in &policy.forbidden_paths {
                if path.starts_with(forbidden) {
                    return Err(format!("Access to path '{}' is forbidden", arg));
                }
            }
        }
        
        // Validate working directory
        if let Some(dir) = working_dir {
            let mut allowed = false;
            for allowed_dir in &policy.allowed_directories {
                if dir.starts_with(allowed_dir) {
                    allowed = true;
                    break;
                }
            }
            if !allowed {
                return Err(format!("Working directory '{}' is not allowed", dir.display()));
            }
        }
        
        // Check for dangerous patterns
        let dangerous_patterns = vec![
            "sudo", "su", "chmod 777", "rm -rf /", ":(){ :|:& };:",
            "systemctl", "service", "pkill", "killall", "reboot", "shutdown"
        ];
        
        let full_command = format!("{} {}", command, args.join(" "));
        for pattern in dangerous_patterns {
            if full_command.contains(pattern) {
                return Err(format!("Dangerous pattern '{}' detected", pattern));
            }
        }
        
        Ok(())
    }
    
    /// Validate script content
    async fn validate_script(&self, script: &str) -> Result<(), String> {
        // Check for dangerous commands in script
        let dangerous_patterns = vec![
            "sudo", "su -", "chmod -R 777", "rm -rf /", ":(){ :|:& };:",
            "systemctl", "pkill -9", "killall", "reboot", "shutdown",
            "mkfs", "dd if=/dev/zero", "fork bomb"
        ];
        
        for pattern in dangerous_patterns {
            if script.to_lowercase().contains(pattern) {
                return Err(format!("Script contains dangerous pattern: {}", pattern));
            }
        }
        
        Ok(())
    }
    
    /// Get execution history
    pub async fn get_history(&self) -> Vec<ExecutionResult> {
        self.history.lock().await.clone()
    }
    
    /// Clear execution history
    pub async fn clear_history(&self) {
        self.history.lock().await.clear();
    }
    
    /// Update security policy
    pub async fn update_policy(&self, policy: SecurityPolicy) {
        *self.policy.write().await = policy;
    }
}

/// Sandboxed executor for even safer execution
pub struct SandboxedExecutor {
    executor: CommandExecutor,
    sandbox_dir: PathBuf,
}

impl SandboxedExecutor {
    /// Create new sandboxed executor
    pub async fn new(sandbox_dir: Option<PathBuf>) -> Result<Self, String> {
        let sandbox_dir = sandbox_dir.unwrap_or_else(|| {
            PathBuf::from(format!("/tmp/agent_sandbox_{}", uuid::Uuid::new_v4()))
        });
        
        // Create sandbox directory
        tokio::fs::create_dir_all(&sandbox_dir).await
            .map_err(|e| format!("Failed to create sandbox: {}", e))?;
        
        // Create restricted policy
        let mut policy = SecurityPolicy::default();
        policy.allowed_directories = vec![sandbox_dir.clone()];
        policy.max_execution_time = Duration::from_secs(10);
        policy.max_output_size = 100 * 1024; // 100KB
        
        Ok(Self {
            executor: CommandExecutor::new(Some(policy)),
            sandbox_dir,
        })
    }
    
    /// Execute in sandbox
    pub async fn execute(&self, command: &str, args: &[String]) -> Result<ExecutionResult, String> {
        self.executor.execute(command, args, Some(&self.sandbox_dir)).await
    }
    
    /// Clean up sandbox
    pub async fn cleanup(&self) -> Result<(), String> {
        tokio::fs::remove_dir_all(&self.sandbox_dir).await
            .map_err(|e| format!("Failed to clean up sandbox: {}", e))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[tokio::test]
    async fn test_safe_command_execution() {
        let executor = CommandExecutor::new(None);
        
        // Test allowed command
        let result = executor.execute("echo", &["Hello, World!".to_string()], None).await;
        assert!(result.is_ok());
        let result = result.unwrap();
        assert_eq!(result.stdout.trim(), "Hello, World!");
    }
    
    #[tokio::test]
    async fn test_forbidden_command() {
        let executor = CommandExecutor::new(None);
        
        // Test forbidden command
        let result = executor.execute("rm", &["-rf".to_string(), "/".to_string()], None).await;
        assert!(result.is_err());
    }
    
    #[tokio::test]
    async fn test_rate_limiting() {
        let mut policy = SecurityPolicy::default();
        policy.rate_limit_per_minute = 2;
        let executor = CommandExecutor::new(Some(policy));
        
        // Execute twice (should succeed)
        let _ = executor.execute("echo", &["1".to_string()], None).await;
        let _ = executor.execute("echo", &["2".to_string()], None).await;
        
        // Third execution should fail
        let result = executor.execute("echo", &["3".to_string()], None).await;
        assert!(result.is_err());
        assert!(result.unwrap_err().contains("Rate limit"));
    }
    
    #[tokio::test]
    async fn test_sandboxed_execution() {
        let sandbox = SandboxedExecutor::new(None).await.unwrap();
        
        // Test execution in sandbox
        let result = sandbox.execute("pwd", &[]).await;
        assert!(result.is_ok());
        assert!(result.unwrap().stdout.contains("agent_sandbox"));
        
        // Cleanup
        let _ = sandbox.cleanup().await;
    }
}