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

# Copy all think-ai crate Cargo.toml files that exist
COPY think-ai-core/Cargo.toml ./think-ai-core/
COPY think-ai-storage/Cargo.toml ./think-ai-storage/
COPY think-ai-cli/Cargo.toml ./think-ai-cli/
COPY think-ai-consciousness/Cargo.toml ./think-ai-consciousness/
COPY think-ai-utils/Cargo.toml ./think-ai-utils/
COPY think-ai-process-manager/Cargo.toml ./think-ai-process-manager/
COPY think-ai-knowledge/Cargo.toml ./think-ai-knowledge/
COPY think-ai-tinyllama/Cargo.toml ./think-ai-tinyllama/
COPY think-ai-local-llm/Cargo.toml ./think-ai-local-llm/
COPY think-ai-quantum-mind/Cargo.toml ./think-ai-quantum-mind/

# Create empty lib.rs files for dependency caching
RUN mkdir -p think-ai-core/src think-ai-storage/src think-ai-cli/src \
    think-ai-consciousness/src think-ai-utils/src think-ai-process-manager/src \
    think-ai-knowledge/src think-ai-tinyllama/src think-ai-local-llm/src \
    think-ai-quantum-mind/src && \
    echo 'fn main() {}' > think-ai-cli/src/main.rs && \
    echo '' > think-ai-core/src/lib.rs && \
    echo '' > think-ai-storage/src/lib.rs && \
    echo '' > think-ai-consciousness/src/lib.rs && \
    echo '' > think-ai-utils/src/lib.rs && \
    echo '' > think-ai-process-manager/src/lib.rs && \
    echo '' > think-ai-knowledge/src/lib.rs && \
    echo '' > think-ai-tinyllama/src/lib.rs && \
    echo '' > think-ai-local-llm/src/lib.rs && \
    echo '' > think-ai-quantum-mind/src/lib.rs

# Build dependencies only
RUN cargo build --release --bin full-server
RUN rm -rf think-ai-*/src/

# Copy source code
COPY . .

# Build release binaries with optimizations
RUN cargo build --release --bins

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

# Copy binaries from builder
COPY --from=builder /build/target/release/full-server ./
COPY --from=builder /build/target/release/think-ai ./
COPY --from=builder /build/target/release/process-manager ./
COPY --from=builder /build/target/release/think-ai-lint ./

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