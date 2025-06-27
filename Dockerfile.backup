# Think AI Rust Multi-stage Build
# Optimized for Railway deployment with minimal runtime

# Build stage
FROM rust:1.80-slim AS builder

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /build

# Copy Cargo files first for dependency caching
COPY Cargo.toml ./

# Copy all think-ai crate Cargo.toml files that exist in workspace
COPY think-ai-core/Cargo.toml ./think-ai-core/
COPY think-ai-vector/Cargo.toml ./think-ai-vector/
COPY think-ai-http/Cargo.toml ./think-ai-http/
COPY think-ai-storage/Cargo.toml ./think-ai-storage/
COPY think-ai-cli/Cargo.toml ./think-ai-cli/
COPY think-ai-consciousness/Cargo.toml ./think-ai-consciousness/
COPY think-ai-coding/Cargo.toml ./think-ai-coding/
COPY think-ai-cache/Cargo.toml ./think-ai-cache/
COPY think-ai-utils/Cargo.toml ./think-ai-utils/
COPY think-ai-process-manager/Cargo.toml ./think-ai-process-manager/
COPY think-ai-linter/Cargo.toml ./think-ai-linter/
COPY think-ai-knowledge/Cargo.toml ./think-ai-knowledge/
COPY think-ai-tinyllama/Cargo.toml ./think-ai-tinyllama/
COPY think-ai-server/Cargo.toml ./think-ai-server/

# Create empty lib.rs files and binary files for dependency caching
RUN mkdir -p think-ai-core/src think-ai-vector/src think-ai-vector/benches think-ai-http/src think-ai-storage/src \
    think-ai-cli/src think-ai-cli/src/bin think-ai-consciousness/src think-ai-coding/src think-ai-cache/src \
    think-ai-utils/src think-ai-process-manager/src think-ai-process-manager/src/bin \
    think-ai-linter/src think-ai-linter/src/bin \
    think-ai-knowledge/src think-ai-knowledge/src/bin think-ai-tinyllama/src think-ai-server/src && \
    echo 'fn main() {}' > think-ai-cli/src/main.rs && \
    echo 'fn main() {}' > think-ai-cli/src/bin/full-server.rs && \
    echo 'fn main() {}' > think-ai-cli/src/bin/train-comprehensive.rs && \
    echo 'fn main() {}' > think-ai-cli/src/bin/self-learning-service.rs && \
    echo 'fn main() {}' > think-ai-cli/src/bin/train-consciousness.rs && \
    echo 'fn main() {}' > think-ai-server/src/main.rs && \
    echo 'fn main() {}' > think-ai-linter/src/bin/think-ai-lint.rs && \
    echo 'fn main() {}' > think-ai-process-manager/src/bin/process-manager.rs && \
    echo 'fn main() {}' > think-ai-knowledge/src/bin/train_knowledge.rs && \
    echo 'fn main() {}' > think-ai-knowledge/src/bin/demo_knowledge.rs && \
    echo 'fn main() {}' > think-ai-knowledge/src/bin/train_direct_answers.rs && \
    echo 'fn main() {}' > think-ai-knowledge/src/bin/comprehensive_train.rs && \
    echo 'fn main() {}' > think-ai-knowledge/src/bin/direct_train.rs && \
    echo 'fn main() {}' > think-ai-knowledge/src/bin/train_1000.rs && \
    echo 'fn main() {}' > think-ai-knowledge/src/bin/train_minimal.rs && \
    echo 'fn main() {}' > think-ai-knowledge/src/bin/build_with_tinyllama.rs && \
    echo 'fn main() { println!("dummy benchmark"); }' > think-ai-vector/benches/o1_performance.rs && \
    echo '' > think-ai-core/src/lib.rs && \
    echo '' > think-ai-vector/src/lib.rs && \
    echo '' > think-ai-http/src/lib.rs && \
    echo '' > think-ai-storage/src/lib.rs && \
    echo '' > think-ai-consciousness/src/lib.rs && \
    echo '' > think-ai-coding/src/lib.rs && \
    echo '' > think-ai-cache/src/lib.rs && \
    echo '' > think-ai-utils/src/lib.rs && \
    echo '' > think-ai-process-manager/src/lib.rs && \
    echo '' > think-ai-linter/src/lib.rs && \
    echo '' > think-ai-knowledge/src/lib.rs && \
    echo '' > think-ai-tinyllama/src/lib.rs

# Build dependencies only
RUN cargo build --release
RUN rm -rf think-ai-*/src/

# Copy source code
COPY . .

# Build all release binaries and list them
RUN cargo build --release && ls -la /build/target/release/ | grep -E '^-.*think-ai'

# Runtime stage
FROM debian:bookworm-slim

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    libssl3 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd -r thinkaiuser \
    && useradd -r -g thinkaiuser thinkaiuser

# Create app directory
WORKDIR /app

# Create bin directory and copy binaries where Railway expects them
RUN mkdir -p /app/bin

# Copy all available think-ai binaries from builder (correct paths)
COPY --from=builder /build/target/release/think-ai /app/bin/think-ai
COPY --from=builder /build/target/release/full-server /app/bin/full-server
COPY --from=builder /build/target/release/train-comprehensive /app/bin/train-comprehensive
COPY --from=builder /build/target/release/self-learning-service /app/bin/self-learning-service
COPY --from=builder /build/target/release/train-consciousness /app/bin/train-consciousness

# Create the specific binary Railway expects
RUN ln -sf /app/bin/full-server /app/bin/think-ai-cli

# Copy main binary to root for compatibility  
COPY --from=builder /build/target/release/full-server ./

# Copy webapp and knowledge files
COPY --from=builder /build/minimal_3d.html ./
COPY --from=builder /build/think-ai-knowledge/data/ ./think-ai-knowledge/data/

# Set proper permissions
RUN chown -R thinkaiuser:thinkaiuser /app

# Add labels for Railway caching
LABEL railway.cache=true
LABEL railway.cache.key="think-ai-rust-v1"

# Expose default port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8080}/health || exit 1

# Switch to non-root user
USER thinkaiuser

# Start the full server with webapp (Railway will set PORT env var)
CMD ["./full-server"]