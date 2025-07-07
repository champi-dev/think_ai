# Simple single-stage build for Railway with correct Rust version
FROM rust:1.80.1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y pkg-config libssl-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy source code
COPY . .

# Fix dependencies for Rust 1.80.1 compatibility
COPY fix-deps.sh ./
RUN chmod +x fix-deps.sh && ./fix-deps.sh

# Build the full working O(1) system
RUN cargo build --release --bin full-working-o1

# Don't expose a specific port - Railway will set PORT env var at runtime
# Railway handles port exposure automatically

# Railway will set PORT environment variable at runtime
# Log environment variables for debugging
ENV RUST_LOG=info

# Run the full working O(1) system (Complete Think AI, guaranteed O(1)/O(log n), no hanging)
CMD ["./target/release/full-working-o1"]