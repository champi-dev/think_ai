# O(1) API Dockerfile - uses pre-built OPTIMIZED base image
# This only copies application code, making builds take ~10 seconds
# Image size: ~2GB (optimized) instead of 5GB

# Use the pre-built base image from Docker Hub
# Using optimized tag for smaller, faster pulls
ARG BASE_IMAGE=devsarmico/think-ai-base:optimized
FROM ${BASE_IMAGE}

# Add labels for Railway caching
LABEL railway.cache=true
LABEL railway.cache.key="think-ai-optimized-v1"

# Set working directory (already created in base)
WORKDIR /app

# Copy only application code - this is the O(1) operation
# Dependencies are already installed in the base image
COPY . .

# No need for test command - remove it

# Expose the API port
EXPOSE 8080

# Health check for Railway
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health').raise_for_status()" || exit 1

# Start the API server
# The transformers patch is applied within think_ai_full.py
CMD ["python", "start_with_patch.py"]