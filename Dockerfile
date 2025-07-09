FROM rust:1.82-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy all files
COPY . .

# Build only the main binary
RUN cargo build --release --bin think-ai

# Set environment
ENV RUST_LOG=info

# The PORT env var is set by Railway
CMD ["./target/release/think-ai", "server", "--host", "0.0.0.0"]