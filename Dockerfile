# Optimized multi-stage build for Railway
FROM rust:1.80-slim AS builder

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy workspace files
COPY Cargo.toml Cargo.lock ./

# Copy all source crates
COPY think-ai-core ./think-ai-core
COPY think-ai-vector ./think-ai-vector  
COPY think-ai-http ./think-ai-http
COPY think-ai-storage ./think-ai-storage
COPY think-ai-cli ./think-ai-cli
COPY think-ai-consciousness ./think-ai-consciousness
COPY think-ai-coding ./think-ai-coding
COPY think-ai-cache ./think-ai-cache
COPY think-ai-utils ./think-ai-utils
COPY think-ai-process-manager ./think-ai-process-manager
COPY think-ai-linter ./think-ai-linter
COPY think-ai-knowledge ./think-ai-knowledge
COPY think-ai-tinyllama ./think-ai-tinyllama
COPY think-ai-server ./think-ai-server

# Build with optimizations for cloud deployment
ENV CARGO_BUILD_JOBS=2
RUN cargo build --release --bin full-server

# Runtime stage
FROM debian:bookworm-slim

# Install runtime dependencies only
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    libssl3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the binary
COPY --from=builder /app/target/release/full-server ./full-server

# Copy webapp file
COPY minimal_3d.html ./minimal_3d.html

# Create non-root user
RUN useradd -r -s /bin/false thinkaiuser
USER thinkaiuser

# The Railway PORT env var will be used by the binary
EXPOSE 8080

CMD ["./full-server"]