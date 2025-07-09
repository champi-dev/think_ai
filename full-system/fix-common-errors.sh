#!/bin/bash

echo "=== Fixing common compilation errors in think-ai-knowledge ==="
cd /home/champi/Dev/think_ai

# Fix 1: Add missing Serialize/Deserialize derives for ComprehensiveBenchmarkReport
echo "Fixing ComprehensiveBenchmarkReport traits..."
sed -i 's/pub struct ComprehensiveBenchmarkReport {/#[derive(Debug, Clone, Serialize, Deserialize)]\npub struct ComprehensiveBenchmarkReport {/' think-ai-knowledge/src/llm_benchmarks.rs

# Fix 2: Add missing Serialize/Deserialize derives for O1PerformanceMetrics
echo "Fixing O1PerformanceMetrics traits..."
sed -i 's/pub struct O1PerformanceMetrics {/#[derive(Debug, Clone, Serialize, Deserialize)]\npub struct O1PerformanceMetrics {/' think-ai-knowledge/src/o1_benchmark_monitor.rs

# Fix 3: Add missing ProcessType and ProcessState (they seem to be missing)
echo "Adding ProcessType and ProcessState enums..."
cat >> think-ai-knowledge/src/types.rs << 'EOF'

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum ProcessType {
    LLM,
    Knowledge,
    Training,
    Evaluation,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum ProcessState {
    Running,
    Paused,
    Stopped,
    Error,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProcessMessage {
    pub process_type: ProcessType,
    pub state: ProcessState,
    pub message: String,
}
EOF

# Fix 4: Export the new types
echo "Exporting new types..."
echo "pub use types::{ProcessType, ProcessState, ProcessMessage};" >> think-ai-knowledge/src/lib.rs

echo "Done! Running build to check progress..."
cargo build -p think-ai-knowledge 2>&1 | grep -c "error\[E"