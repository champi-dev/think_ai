# Use a simpler single-stage build to avoid network issues
FROM rust:1.82

# Install minimal dependencies
RUN apt-get update && apt-get install -y ca-certificates libssl-dev pkg-config && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy all files
COPY . .

# Build the full-working-o1 binary with Qwen support
RUN cargo build --release --bin full-working-o1

# Create a non-root user
RUN useradd -m -u 1001 appuser && chown -R appuser:appuser /app

# Copy webapp files to ensure they're available at runtime
RUN cp minimal_3d.html /app/ || true
RUN cp -r static /app/ || true

USER appuser

# The PORT env var is set by Railway
EXPOSE 8080

# Set working directory for runtime
WORKDIR /app

CMD ["./target/release/full-working-o1"]