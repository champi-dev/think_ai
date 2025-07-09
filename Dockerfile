# Multi-stage build for Think AI with Ollama and Qwen
FROM rust:1.82 as builder

RUN apt-get update && apt-get install -y ca-certificates libssl-dev pkg-config && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .
RUN cargo build --release --bin full-working-o1

# Runtime stage with Ollama
FROM ubuntu:22.04

# Install dependencies and Ollama
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy the built binary
COPY --from=builder /app/target/release/full-working-o1 /app/full-working-o1
COPY --from=builder /app/minimal_3d.html /app/minimal_3d.html
COPY --from=builder /app/static /app/static

# Copy startup script
COPY --from=builder /app/start-with-ollama.sh /app/start.sh
RUN chmod +x /app/start.sh

WORKDIR /app
EXPOSE 8080

CMD ["/app/start.sh"]