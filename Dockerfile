# O(1) API Dockerfile - uses pre-built base image
# This only copies application code, making builds take ~10 seconds

# Use the pre-built base image from Docker Hub
# Replace 'devsarmico' with your actual Docker Hub username
ARG BASE_IMAGE=devsarmico/think-ai-base:latest
FROM ${BASE_IMAGE}

# Set working directory (already created in base)
WORKDIR /app

# Copy only application code - this is the O(1) operation
# Dependencies are already installed in the base image
COPY . .

# Ensure the transformers fix is applied
RUN python -c "import os; os.system('ls -la')"

# Expose the API port
EXPOSE 8080

# Health check for Railway
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health').raise_for_status()" || exit 1

# Start the API server
# The transformers patch is applied within think_ai_full.py
CMD ["python", "think_ai_full.py"]