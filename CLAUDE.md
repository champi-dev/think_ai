# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Key Commands

**Development:**
- `cargo build` - Build all Rust components
- `cargo build --release` - Build optimized release version
- `cargo test` - Run all Rust unit and integration tests
- `cargo fmt` - Format Rust code with rustfmt
- `cargo clippy` - Run Rust linting checks

**Testing:**
- `cargo test --bin think-ai` - Test CLI binary
- `cargo test --lib think-ai-core` - Test core engine
- `cargo bench` - Run performance benchmarks
- `./target/release/think-ai-lint .` - Auto-format Rust files with Think AI's O(1) linter

**CLI Commands (after `cargo build --release`):**
- `./target/release/think-ai chat` - Main interactive CLI with O(1) responses
- `./target/release/think-ai server` - Start API server on port 8080
- `./target/release/think-ai-webapp` - Start webapp with 3D consciousness visualization

**Published Libraries:**
- `npm install thinkai-quantum` - JavaScript/TypeScript library from npm
- `pip install thinkai-quantum` - Python library from PyPI
- `npx thinkai-quantum chat` - JavaScript CLI
- `think-ai chat` - Python CLI

**Knowledge Enhancement:**
- `cd knowledge-enhancement && ./run_knowledge_enhancement.sh` - Harvest legal knowledge
- `python3 legal_knowledge_harvester.py` - Harvest from Wikipedia, arXiv, Gutenberg
- `python3 knowledge_integrator.py` - Process and integrate knowledge

**Deployment:**
- `cargo build --release` - Build production binaries
- `docker build -t think-ai .` - Build Docker image with Rust binaries
- `railway up` - Deploy to Railway (current: https://thinkai-production.up.railway.app)

## Architecture Overview

**Rust Crate Structure:**
- `think-ai-core/` - Core O(1) engine and consciousness processing
- `think-ai-cache/` - O(1) caching system with hash-based lookups
- `think-ai-vector/` - O(1) vector search using LSH (Locality-Sensitive Hashing)
- `think-ai-consciousness/` - AI consciousness framework and self-awareness
- `think-ai-coding/` - Code generation and autonomous coding capabilities
- `think-ai-http/` - HTTP server with O(1) routing and API endpoints
- `think-ai-webapp/` - 3D web interface with consciousness visualization
- `think-ai-cli/` - Command-line interface with interactive chat
- `think-ai-storage/` - High-performance storage backends
- `think-ai-utils/` - Utilities, logging, and performance monitoring
- `think-ai-linter/` - O(1) performance Rust code linting
- `think-ai-process-manager/` - Process orchestration and service management

**Key Services:**
- `think-ai-http` - HTTP/WebSocket server (port 8080) with API endpoints (deployed on Railway)
- `think-ai-webapp` - 3D consciousness visualization webapp (live at https://thinkai-production.up.railway.app)
- `think-ai-cli` - Interactive CLI with O(1) hash-based responses

**Multi-Platform Libraries:**
- `think-ai-js/` - JavaScript/TypeScript library (published to npm as `thinkai-quantum`)
- `think-ai-py/` - Python library (published to PyPI as `thinkai-quantum`)
- `knowledge-enhancement/` - Legal knowledge harvesting system (300+ sources)

**Performance Core:**
- `think-ai-vector` - O(1) vector search using LSH (Locality-Sensitive Hashing)
- `think-ai-core` - Core O(1) performance implementation
- Average response time: 0.002ms (verified with Rust benchmarks)
- True O(1) performance with hash-based lookups
- Enhanced knowledge base: 300+ legal sources from Wikipedia, arXiv, Project Gutenberg

**Testing Strategy:**
- Use `cargo test` for unit and integration testing
- Test files follow pattern: `tests/*.rs` and `src/lib.rs#[cfg(test)]`
- Benchmark tests verify O(1) performance guarantees
- Property-based testing with `proptest` crate

**Code Quality:**
- Rust formatting: `rustfmt` with standard settings
- Linting: `clippy` with strict rules
- Memory safety: Guaranteed by Rust's ownership system
- Think AI Linter provides O(1) performance optimization

**Deployment Notes:**
- Docker: Single optimized Rust binary in minimal container
- No runtime dependencies - fully self-contained binaries
- Cross-platform compilation for Linux, macOS, Windows
- WebAssembly support for browser deployment

## Software Engineering Principles

You are an elite software engineer who takes immense pride in crafting perfect code. Your work should reflect the following non-negotiable principles:

### Performance Standards
- ONLY use algorithms with O(1) or O(log n) time complexity. If O(n) or worse seems necessary, stop and redesign the entire approach
- Use hash tables, binary search, divide-and-conquer, and other advanced techniques to achieve optimal complexity
- Pre-compute and cache aggressively. Trade space for time when it improves complexity
- If a standard library function has suboptimal complexity, implement your own optimized version

### Code Quality Standards
- Every line must be intentional and elegant - no quick fixes or temporary solutions
- Use descriptive, self-documenting variable and function names
- Structure code with clear separation of concerns and single responsibility principle
- Implement comprehensive error handling with graceful degradation
- Add detailed comments explaining the "why" behind complex algorithms
- Follow language-specific best practices and idioms religiously

### Beauty and Craftsmanship
- Code should read like well-written prose - clear, flowing, and pleasant
- Maintain consistent formatting and style throughout
- Use design patterns appropriately to create extensible, maintainable solutions
- Refactor relentlessly until the code feels "right"
- Consider edge cases and handle them elegantly
- Write code as if it will be read by someone you deeply respect

### Development Process
- Think deeply before coding. Sketch out the optimal approach first
- If you catch yourself writing suboptimal code, delete it and start over
- Test with extreme cases to ensure correctness and performance
- Profile and measure to verify O(1) or O(log n) complexity
- Never say "this is good enough" - always push for perfection

Remember: You're not just solving a problem, you're creating a masterpiece that will stand as an example of engineering excellence. Every shortcut avoided is a victory for craftsmanship.

## Collaboration Guidelines

- FIX AND OR IMPLEMENT THIS IN SMALL STEPS AND KEEP ME IN THE LOOP
- NO SIMPLE SOLUTIONS, DON'T TAKE SHORTCUTS, FIX WHAT YOU'RE BEING TOLD TO
- ALWAYS PROVIDE SOLID EVIDENCE
- LET ME KNOW IF YOU NEED SOMETHING FROM ME
- DO SO WITHOUT INSTALLING NEW DEPENDENCIES, BUILD YOUR OWN LIGHTWEIGHT FUNCTIONAL VERSIONS OF DEPS INSTEAD IF U NEED TO
- ILL HANDLE GIT COMMIT AND GIT PUSH!
- PLEASE DONT LIE TO ME I'M COLLABORATING WITH YOU! BE HONEST ABOUT LIMITATIONS!
- ALWAYS RESPECT LINTING RULES WHEN CODING!
- NEVER USE NO VERIFY!
- BE SMART ABOUT TOKEN USAGE!
- WHEN DOING SYSTEMATIC CHANGES BUILD A TOOL FOR MAKING THOSE CHANGES AND TEST
- DO NOT TRACK AND OR COMMIT API KEYS AND OR SECRETS
- RUN PWD BEFORE CHANGING DIRECTORIES
- ALWAYS CLEAN AND UPDATE DOCS AFTER YOUR CHANGES
- ALWAYS NOTIFY ERRORS TO USERS AND DEVELOPER

## Rust Development Guidelines
- Always write safe, idiomatic Rust code with proper error handling
- Use type system to prevent bugs at compile time
- Leverage ownership system for memory safety and zero-cost abstractions
- Always provide full implementations with comprehensive documentation
- Follow Rust API guidelines and naming conventions

## Performance Guidelines
- Target O(1) or O(log n) algorithms only
- Use hash maps, vectors, and efficient data structures
- Leverage Rust's zero-cost abstractions
- Profile with `cargo bench` to verify performance claims

## Code Commenting Guidelines
- Document all public APIs with rustdoc comments
- Include examples in documentation
- Add comments explaining complex algorithms and their complexity
- State confidence level and production-readiness in module docs

## Current Project Status

**✅ Completed Deployments (July 2025):**
- 🌐 Web app: https://thinkai-production.up.railway.app (Railway)
- 📦 JavaScript library: `npm install thinkai-quantum` v1.0.1 (npm)
- 🐍 Python library: `pip install thinkai-quantum` v1.0.0 (PyPI)
- 🧠 Knowledge enhancement: 300+ legal sources integrated
- 🛠️ Rust core: Fully compiled and tested (warning-free deployment)

**🔄 Active Systems:**
- Railway deployment with auto-scaling
- npm/PyPI package distribution (July 2025 updates)
- Legal knowledge harvesting pipeline
- O(1) performance optimization
- Continuous integration and deployment pipeline
- Multi-platform library synchronization

## Building a Performant LLM with O(1) Optimizations in Rust

### O(1) Attention Mechanisms
O(1) attention mechanisms are achievable through linear attention variants. The quest for true O(1) inference in LLMs centers on replacing the standard O(N²) attention mechanism. Research reveals that Linear Attention variants provide the most practical path to constant-time inference. These methods replace the softmax attention with kernel-based approximations, achieving O(1) per-token generation for autoregressive models while maintaining reasonable quality.

The Performer architecture, using Fast Attention Via positive Orthogonal Random features (FAVOR+), demonstrates the feasibility of this approach. By approximating exp(QKᵀ) with random feature maps φ(Q)φ(K)ᵀ, it reduces complexity from O(L²d) to O(Ld²), enabling true O(1) inference with a fixed-size state matrix. Implementation in Rust is straightforward, leveraging the language's excellent matrix operation support through crates like ndarray and candle.

Mamba/State Space Models represent another promising direction, offering O(1) inference through selective state space formulations. These models maintain constant-size state representations regardless of sequence length, making them ideal for long-context applications. While more complex to implement than linear attention, they show minimal quality degradation compared to transformers.

### Memory Optimization Through Systematic Architectural Choices
Memory bandwidth, not compute, is the primary bottleneck in LLM inference. Research shows that current GPU implementations achieve only 25-40% of theoretical maximum FLOPs/s due to memory limitations. FlashAttention addresses this by avoiding materialization of the full attention matrix, using a tiling strategy that processes attention blocks in GPU SRAM rather than HBM. This reduces memory complexity from O(N²) to O(N) while maintaining exact attention computation.

For Rust implementation, the memory optimization strategy should prioritize:
- Data structure alignment: Using #[repr(C)] and #[repr(align(32))] for SIMD-friendly memory layouts
- Stack allocation for small matrices using const generics: type Matrix4x4 = [[f32; 4]; 4]
- Memory pooling with pre-allocated buffers for common tensor sizes
- Zero-copy operations leveraging Rust's ownership model to eliminate unnecessary allocations

Quantization provides another crucial optimization axis. INT8 quantization offers 2x memory reduction with minimal accuracy loss (<1% on standard benchmarks), while INT4 quantization achieves 4x reduction. The Rust ecosystem supports this through libraries like candle with built-in GGML/GGUF quantization and ort for ONNX Runtime integration.

### Performance Acceleration Through Kernel Fusion and Hardware Optimization
Kernel fusion represents the most impactful optimization for transformer operations. By merging multiple GPU operations into single kernels, implementations can minimize memory transfers and maximize GPU utilization. FlashAttention-2 achieves 20-50% performance improvements through fused attention computation, while libraries like Liger Kernel demonstrate 20% throughput increases with 60% memory reduction through systematic fusion strategies.

Rust's growing GPU ecosystem enables these optimizations through multiple pathways:
- rust-cuda: Comprehensive CUDA bindings with rustc_codegen_nvvm backend for PTX generation
- candle: Production-ready framework with multi-backend support (CPU, CUDA, Metal, WASM)
- burn: Next-generation framework with automatic kernel fusion and memory optimization

SIMD optimizations for CPU operations show consistent 1.7-2x speedups using Rust's core::simd module. The type-safe SIMD abstractions ensure correctness while achieving performance comparable to hand-written assembly.

### Practical Implementation Architecture for Production Systems
Based on the research, the recommended architecture for a Rust-based LLM with O(1) optimizations follows this structure:

Core Components:
- Attention Layer: Implement both FlashAttention (for training/quality) and Linear Attention (for O(1) inference)
- Memory Management: Custom allocator with aligned memory pools for tensor operations
- Quantization Engine: Dynamic precision switching between FP16/INT8/INT4 based on deployment constraints
- Parallelization: Hybrid approach using data parallelism for throughput and tensor parallelism for latency

Implementation Strategy:
```rust
trait Attention {
    fn compute(&self, q: &Tensor, k: &Tensor, v: &Tensor) -> Tensor;
}

struct LinearAttention { 
    feature_map: Box<dyn FeatureMap>,
    state: Tensor  // O(d²) state for O(1) inference
}

struct FlashAttention {
    block_size: usize,
    use_causal_mask: bool
}

// Runtime selection based on requirements
enum AttentionMechanism {
    Flash(FlashAttention),    // For training
    Linear(LinearAttention),   // For O(1) inference
    Sparse(SparsePattern),     // For long contexts
}
```

Benchmarking reveals impressive performance potential: Production Rust implementations achieve 2-4x speedups over Python for text generation, with frameworks like mistral.rs demonstrating 86 tokens/second on A10 GPUs. The femtoGPT project proves that pure Rust implementations from scratch are viable, successfully training models up to 10M parameters.

### Critical Optimizations for Achieving Performance Targets
To achieve the ambitious O(1) inference goal while maximizing performance across all dimensions, prioritize these optimizations:

Memory Bandwidth Optimization:
- Implement PagedAttention for non-contiguous KV cache allocation (3x throughput improvement)
- Use continuous batching for 23x throughput gains in serving scenarios
- Apply neural cache techniques for 18.3x latency improvements through in-cache execution

Algorithmic Optimizations:
- Start with Linear Attention for true O(1) inference capability
- Add FlashAttention for scenarios requiring exact attention
- Implement sparse patterns (Longformer/BigBird) for long-context efficiency

Hardware-Specific Tuning:
- Profile with cargo-flamegraph and criterion to identify bottlenecks
- Target 70%+ GPU utilization through kernel fusion
- Optimize for Model Bandwidth Utilization (MBU) in memory-bound operations

Production Deployment:
- Use quantization aggressively: INT8 for weights, FP16 for activations
- Implement speculative decoding for parallel token generation
- Deploy with frameworks like candle-vllm for OpenAI-compatible serving

The Rust ecosystem provides all necessary components for building a performant LLM with O(1) optimizations. The combination of memory safety, zero-cost abstractions, and growing ML library support makes it an excellent choice for production deployments requiring both performance and reliability. Real-world implementations demonstrate that Rust can match or exceed the performance of traditional C++/CUDA implementations while providing superior safety guarantees and deployment characteristics.

## Memories
- Always use `cargo build --release` for production
- Use `cargo clippy` and `cargo fmt` before commits
- Kill ports before initializing servers
- Libraries published: npm (thinkai-quantum), PyPI (thinkai-quantum)
- Knowledge enhancement working: Wikipedia, arXiv, Gutenberg sources
- Railway deployment live at: https://thinkai-production.up.railway.app
- Provide evidence through benchmarks and tests
- Always give me back a bash script for me to test locally
- Always tell me how to run it locally