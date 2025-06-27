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

**✅ Completed Deployments:**
- 🌐 Web app: https://thinkai-production.up.railway.app (Railway)
- 📦 JavaScript library: `npm install thinkai-quantum` (npm)
- 🐍 Python library: `pip install thinkai-quantum` (PyPI)
- 🧠 Knowledge enhancement: 300+ legal sources integrated

**🔄 Active Systems:**
- Railway deployment with auto-scaling
- npm/PyPI package distribution
- Legal knowledge harvesting pipeline
- O(1) performance optimization

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