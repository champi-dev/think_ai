# Multi-stage build for Think AI
FROM python:3.10-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY pyproject.toml .
COPY think_ai/__init__.py think_ai/

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir build && \
    python -m build --wheel && \
    pip install --no-cache-dir dist/*.whl

# Production stage
FROM python:3.10-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libgomp1 \
    libopenblas-base \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r thinkai && useradd -r -g thinkai thinkai

# Set working directory
WORKDIR /app

# Copy from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=thinkai:thinkai think_ai think_ai/
COPY --chown=thinkai:thinkai examples examples/
COPY --chown=thinkai:thinkai docs docs/
COPY --chown=thinkai:thinkai config config/

# Create necessary directories
RUN mkdir -p /app/data /app/logs /app/plugins && \
    chown -R thinkai:thinkai /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV THINK_AI_HOME=/app
ENV THINK_AI_DATA=/app/data
ENV THINK_AI_LOGS=/app/logs
ENV THINK_AI_PLUGINS=/app/plugins

# Switch to non-root user
USER thinkai

# Expose ports
EXPOSE 8000 8080 9090

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import think_ai; print('healthy')" || exit 1

# Default command
CMD ["python", "-m", "think_ai.cli"]