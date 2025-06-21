# Aggressive caching multi-stage Dockerfile for O(1) builds
# Stage 1: Python dependency caching layer
FROM python:3.11-slim as python-deps
WORKDIR /deps

# Cache pip packages
COPY requirements-fast.txt .
RUN --mount=type=cache,id=think-ai-pip-deps,target=/root/.cache/pip \
    pip install --user --no-warn-script-location -r requirements-fast.txt

# Stage 2: Node.js dependency caching layer
FROM node:20-alpine as node-deps
WORKDIR /deps

# Cache npm packages
COPY package*.json ./
RUN --mount=type=cache,id=think-ai-npm-deps,target=/root/.npm \
    npm ci --only=production && \
    npm cache verify

# Stage 3: Build stage with cached dependencies
FROM python:3.11-slim as builder
WORKDIR /app

# Install system dependencies (cached)
RUN --mount=type=cache,id=think-ai-apt-builder,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,id=think-ai-apt-lib-builder,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from cache
COPY --from=python-deps /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY . .

# Build Python package
RUN --mount=type=cache,id=think-ai-pip-build,target=/root/.cache/pip \
    python setup.py bdist_wheel

# Stage 4: Runtime with minimal footprint
FROM python:3.11-slim
WORKDIR /app

# Install runtime dependencies only
RUN --mount=type=cache,id=think-ai-apt-runtime,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,id=think-ai-apt-lib-runtime,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder
COPY --from=python-deps /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy only necessary files
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/think_ai ./think_ai
COPY --from=builder /app/api_server_cpu.py .
COPY --from=builder /app/.env.example .env

EXPOSE 8080
CMD ["uvicorn", "api_server_cpu:app", "--host", "0.0.0.0", "--port", "8080"]
