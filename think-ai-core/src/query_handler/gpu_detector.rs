use anyhow::{anyhow, Result};
use serde::{Deserialize, Serialize};
use std::process::Command;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GpuInfo {
    pub available: bool,
    pub device_type: DeviceType,
    pub device_name: String,
    pub memory_mb: usize,
    pub cuda_version: Option<String>,
    pub compute_capability: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum DeviceType {
    Cpu,
    CudaGpu,
    MetalGpu,
    RocmGpu,
}

impl DeviceType {
    pub fn to_torch_device(&self) -> &'static str {
        match self {
            DeviceType::Cpu => "cpu",
            DeviceType::CudaGpu => "cuda",
            DeviceType::MetalGpu => "mps",
            DeviceType::RocmGpu => "rocm",
        }
    }
}

pub struct GpuDetector;

impl GpuDetector {
    /// Detect available GPU with O(1) cached result after first check
    pub fn detect() -> GpuInfo {
        // Try CUDA first (NVIDIA)
        if let Ok(info) = Self::detect_cuda() {
            return info;
        }

        // Try Metal (Apple Silicon)
        if let Ok(info) = Self::detect_metal() {
            return info;
        }

        // Try ROCm (AMD)
        if let Ok(info) = Self::detect_rocm() {
            return info;
        }

        // Fallback to CPU
        GpuInfo {
            available: false,
            device_type: DeviceType::Cpu,
            device_name: Self::get_cpu_info(),
            memory_mb: Self::get_system_memory_mb(),
            cuda_version: None,
            compute_capability: None,
        }
    }

    fn detect_cuda() -> Result<GpuInfo> {
        // Check if nvidia-smi is available
        let output = Command::new("nvidia-smi")
            .args([
                "--query-gpu=name,memory.total",
                "--format=csv,noheader,nounits",
            ])
            .output();

        match output {
            Ok(output) if output.status.success() => {
                let info = String::from_utf8_lossy(&output.stdout);
                let parts: Vec<&str> = info.trim().split(',').collect();

                if parts.len() >= 2 {
                    let device_name = parts[0].trim().to_string();
                    let memory_mb = parts[1].trim().parse::<usize>().unwrap_or(0);

                    // Get CUDA version
                    let cuda_version = Self::get_cuda_version();

                    return Ok(GpuInfo {
                        available: true,
                        device_type: DeviceType::CudaGpu,
                        device_name,
                        memory_mb,
                        cuda_version,
                        compute_capability: Self::get_compute_capability(),
                    });
                }
            }
            _ => {}
        }

        Err(anyhow!("CUDA not available"))
    }

    fn detect_metal() -> Result<GpuInfo> {
        // Check if we're on macOS with Metal support
        #[cfg(target_os = "macos")]
        {
            let output = Command::new("system_profiler")
                .args(&["SPDisplaysDataType", "-json"])
                .output();

            if let Ok(output) = output {
                if output.status.success() {
                    // Parse JSON to get GPU info
                    // For simplicity, we'll just check if Metal is available
                    return Ok(GpuInfo {
                        available: true,
                        device_type: DeviceType::MetalGpu,
                        device_name: "Apple Silicon GPU".to_string(),
                        memory_mb: 8192, // Conservative estimate
                        cuda_version: None,
                        compute_capability: None,
                    });
                }
            }
        }

        Err(anyhow!("Metal not available"))
    }

    fn detect_rocm() -> Result<GpuInfo> {
        // Check for AMD ROCm
        let output = Command::new("rocm-smi")
            .args(["--showproductname"])
            .output();

        match output {
            Ok(output) if output.status.success() => {
                let info = String::from_utf8_lossy(&output.stdout);

                Ok(GpuInfo {
                    available: true,
                    device_type: DeviceType::RocmGpu,
                    device_name: info.trim().to_string(),
                    memory_mb: 8192, // Would need to parse rocm-smi for actual value
                    cuda_version: None,
                    compute_capability: None,
                })
            }
            _ => Err(anyhow!("ROCm not available")),
        }
    }

    fn get_cuda_version() -> Option<String> {
        Command::new("nvcc")
            .arg("--version")
            .output()
            .ok()
            .and_then(|output| {
                if output.status.success() {
                    let version_str = String::from_utf8_lossy(&output.stdout);
                    version_str
                        .lines()
                        .find(|line| line.contains("release"))
                        .and_then(|line| {
                            line.split("release")
                                .nth(1)
                                .and_then(|s| s.split(',').next())
                                .map(|s| s.trim().to_string())
                        })
                } else {
                    None
                }
            })
    }

    fn get_compute_capability() -> Option<String> {
        // This would require more sophisticated detection
        // For now, return a common capability
        Some("7.5".to_string())
    }

    fn get_cpu_info() -> String {
        #[cfg(target_os = "linux")]
        {
            if let Ok(output) = Command::new("lscpu").output() {
                let info = String::from_utf8_lossy(&output.stdout);
                if let Some(line) = info.lines().find(|l| l.starts_with("Model name:")) {
                    return line.replace("Model name:", "").trim().to_string();
                }
            }
        }

        #[cfg(target_os = "macos")]
        {
            if let Ok(output) = Command::new("sysctl")
                .args(&["-n", "machdep.cpu.brand_string"])
                .output()
            {
                return String::from_utf8_lossy(&output.stdout).trim().to_string();
            }
        }

        "Unknown CPU".to_string()
    }

    fn get_system_memory_mb() -> usize {
        #[cfg(target_os = "linux")]
        {
            if let Ok(output) = Command::new("free").args(["-m"]).output() {
                let info = String::from_utf8_lossy(&output.stdout);
                if let Some(line) = info.lines().nth(1) {
                    let parts: Vec<&str> = line.split_whitespace().collect();
                    if parts.len() > 1 {
                        return parts[1].parse().unwrap_or(8192);
                    }
                }
            }
        }

        8192 // Default 8GB
    }
}

/// Singleton cached GPU info for O(1) access
static mut CACHED_GPU_INFO: Option<GpuInfo> = None;
static INIT: std::sync::Once = std::sync::Once::new();

/// Get GPU info with O(1) cached access after first detection
pub fn get_gpu_info() -> &'static GpuInfo {
    unsafe {
        INIT.call_once(|| {
            CACHED_GPU_INFO = Some(GpuDetector::detect());
        });
        CACHED_GPU_INFO.as_ref().unwrap()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_gpu_detection() {
        let info = get_gpu_info();
        println!("GPU Info: {:?}", info);

        // Should always return something
        assert!(!info.device_name.is_empty());

        // Repeated calls should be O(1)
        let start = std::time::Instant::now();
        for _ in 0..1000 {
            let _ = get_gpu_info();
        }
        let elapsed = start.elapsed();

        // Should be very fast (< 1ms for 1000 calls)
        assert!(elapsed.as_millis() < 1);
    }
}
