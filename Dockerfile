# O(1) Dockerfile for 10-second Railway deployments
FROM python:3.11-slim

# Install only essential system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# CRITICAL: Copy and install requirements FIRST for Docker layer caching
# This ensures requirements are only reinstalled when requirements-full.txt changes
COPY requirements-full.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements-full.txt

# Copy application code AFTER requirements
# This way, code changes don't invalidate the requirements cache layer
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV THINK_AI_O1_MODE=true
ENV THINK_AI_COLOMBIAN_MODE=true
ENV THINK_AI_CACHE_EVERYTHING=true

# Expose port
EXPOSE 8080

# Start the application with transformers fix
CMD ["python", "fix_transformers.py"]