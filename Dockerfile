# Build stage
FROM rust:1.82 AS builder

# Install system dependencies
RUN apt-get update && \
    apt-get install -y pkg-config libssl-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy source code
COPY . .

# Build only the working binaries (exclude broken modules)
RUN cargo build --release --bin think-ai

# Runtime stage - smaller image
FROM debian:bookworm-slim

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y ca-certificates libssl3 && \
    rm -rf /var/lib/apt/lists/*

# Copy binary from builder
COPY --from=builder /app/target/release/think-ai /usr/local/bin/

# Railway will set PORT environment variable at runtime
ENV RUST_LOG=info

# Create non-root user for security
RUN useradd -m -u 1001 appuser
USER appuser

# Railway handles port exposure automatically
# The server command will use PORT env var

# Run the Think AI server
CMD ["think-ai", "server"]