# Build stage
FROM rust:1.75 as builder

WORKDIR /app

# Copy workspace files
COPY . .

# Build the specific binary
RUN cd full-system && cargo build --release --bin think-ai-full

# Runtime stage
FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the binary
COPY --from=builder /app/full-system/target/release/think-ai-full /app/
COPY --from=builder /app/full-system/static /app/static

# Expose port
EXPOSE 8080

# Run the binary
CMD ["./think-ai-full"]