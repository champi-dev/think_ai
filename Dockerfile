# Simple single-stage build for Railway
FROM rust:1.80

# Install system dependencies
RUN apt-get update && \
    apt-get install -y pkg-config libssl-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy source code
COPY . .

# Build the full working O(1) system
RUN cargo build --release --bin full-working-o1

# Expose default port (Railway will set PORT env var at runtime)
EXPOSE 8080

# Run the full working O(1) system (Complete Think AI, guaranteed O(1)/O(log n), no hanging)
CMD ["./target/release/full-working-o1"]