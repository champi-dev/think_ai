# Simple single-stage build for Railway
FROM rust:1.80

# Install system dependencies
RUN apt-get update && \
    apt-get install -y pkg-config libssl-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy source code
COPY . .

# Build the binary
RUN cargo build --release --bin full-server

# Expose port (Railway will set PORT env var)
EXPOSE 8080

# Run the server
CMD ["./target/release/full-server"]