# Simple single-stage build for Railway
FROM rust:1.80

# Install system dependencies
RUN apt-get update && \
    apt-get install -y pkg-config libssl-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy source code
COPY . .

# Build the debug server for Railway environment debugging
RUN cargo build --release --bin full-server-fast

# Expose default port (Railway will set PORT env var at runtime)
EXPOSE 8080

# Run the debug server (shows all env vars and health check details)
CMD ["./target/release/full-server-fast"]