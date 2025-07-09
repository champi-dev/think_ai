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

# Create startup script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
# Start Ollama in the background\n\
echo "🚀 Starting Ollama server..."\n\
ollama serve &\n\
OLLAMA_PID=$!\n\
\n\
# Wait for Ollama to be ready\n\
echo "⏳ Waiting for Ollama to start..."\n\
for i in {1..30}; do\n\
    if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then\n\
        echo "✅ Ollama is ready!"\n\
        break\n\
    fi\n\
    if [ $i -eq 30 ]; then\n\
        echo "⚠️ Ollama failed to start, continuing without it"\n\
    fi\n\
    sleep 1\n\
done\n\
\n\
# Try to pull Qwen model if Ollama is running\n\
if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then\n\
    echo "📥 Pulling Qwen 2.5 1.5B model..."\n\
    ollama pull qwen2.5:1.5b || echo "⚠️ Failed to pull Qwen model"\n\
else\n\
    echo "⚠️ Ollama not available, running without LLM support"\n\
fi\n\
\n\
# Start the main application\n\
echo "🌐 Starting Think AI server..."\n\
cd /app && exec ./full-working-o1\n\
' > /app/start.sh && chmod +x /app/start.sh

WORKDIR /app
EXPOSE 8080

CMD ["/app/start.sh"]