FROM rust:1.82-slim as builder

# Install dependencies
RUN apt-get update && apt-get install -y \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy all workspace members
COPY Cargo.toml Cargo.lock ./
COPY think-ai-core ./think-ai-core
COPY think-ai-vector ./think-ai-vector
COPY think-ai-http ./think-ai-http
COPY think-ai-storage ./think-ai-storage
COPY think-ai-cli ./think-ai-cli
COPY think-ai-consciousness ./think-ai-consciousness
COPY think-ai-cache ./think-ai-cache
COPY think-ai-utils ./think-ai-utils
COPY think-ai-knowledge ./think-ai-knowledge
COPY think-ai-webapp ./think-ai-webapp
COPY full-system ./full-system

# Build the full system
RUN cargo build --release --bin think-ai-full

# Runtime stage
FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the binary
COPY --from=builder /app/target/release/think-ai-full /app/think-ai-full

# Copy static files
COPY --from=builder /app/full-system/static ./static

# Set environment
ENV RUST_LOG=info

EXPOSE 8080

# The PORT env var is set by Railway
CMD ["./think-ai-full"]