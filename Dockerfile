# Multi-service Dockerfile for Railway deployment
# Includes both API and webapp with minimal Node.js runtime

FROM devsarmico/think-ai-base:optimized AS final

# Install Node.js from Alpine packages (much faster than NodeSource)
USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    nodejs npm && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Add labels for Railway caching
LABEL railway.cache=true
LABEL railway.cache.key="think-ai-full-system-v1"

# Set working directory
WORKDIR /app

# Copy Python application code and pre-built webapp
COPY . .

# Ensure scripts are executable and owned by appuser
RUN chmod +x start_full_system.py process_manager.py start_with_patch.py && \
    chown -R appuser:appuser /app

# Expose both ports (Railway will use PORT env var)
EXPOSE 8080 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8080}/health || exit 1

# Switch back to appuser for security
USER appuser

# Use the process manager to run both services
CMD ["python", "process_manager.py"]