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
COPY Cargo.toml Cargo.lock ./
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
COPY think-ai-webapp/Cargo.toml ./think-ai-webapp/

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

# Copy binaries from builder (excluding webapp which is WASM-only)
COPY --from=builder /build/target/release/think-ai ./
COPY --from=builder /build/target/release/process-manager ./
COPY --from=builder /build/target/release/think-ai-lint ./

# Configuration files will be created at runtime if needed

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

# Start the HTTP server (Railway will set PORT env var)
CMD ["./think-ai", "server"]