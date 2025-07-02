# Simple single-stage build for Railway
FROM rust:1.80

# Install system dependencies
RUN apt-get update && \
    apt-get install -y pkg-config libssl-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy source code
COPY . .

# Build the full system with O(1) performance and hanging protection
RUN cargo build --release --bin full-system-safe

# Expose default port (Railway will set PORT env var at runtime)
EXPOSE 8080

# Run the full system (Complete Think AI with 3D visualization, O(1) optimized, timeout protected)
CMD ["./target/release/full-system-safe"]