# Use a simpler single-stage build to avoid network issues
FROM rust:1.82

# Install minimal dependencies
RUN apt-get update && apt-get install -y ca-certificates libssl-dev pkg-config && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy all files
COPY . .

# Build only the full-system binary
RUN cargo build --release --bin think-ai-full

# Create a non-root user
RUN useradd -m -u 1001 appuser && chown -R appuser:appuser /app

USER appuser

# The PORT env var is set by Railway
EXPOSE 8080

CMD ["./target/release/think-ai-full"]