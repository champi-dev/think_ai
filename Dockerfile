# Full System Dockerfile - builds both API and webapp
# Uses pre-built optimized base image for Python dependencies

# Stage 1: Build the webapp
FROM node:18-alpine AS webapp-builder

WORKDIR /webapp

# Copy webapp package files
COPY webapp/package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy webapp source
COPY webapp/ ./

# Build the Next.js app
RUN npm run build

# Stage 2: Final image with both API and webapp  
FROM devsarmico/think-ai-base:optimized AS final

# Switch to root to install Node.js
USER root

# Install Node.js using NodeSource binary distributions (more reliable)
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    curl -fsSL https://deb.nodesource.com/setup_18.x -o nodesource_setup.sh && \
    bash nodesource_setup.sh && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* nodesource_setup.sh

# Add labels for Railway caching
LABEL railway.cache=true
LABEL railway.cache.key="think-ai-full-system-v1"

# Set working directory
WORKDIR /app

# Copy Python application code
COPY . .

# Copy built webapp from builder stage
COPY --from=webapp-builder /webapp/.next ./webapp/.next
COPY --from=webapp-builder /webapp/public ./webapp/public
COPY --from=webapp-builder /webapp/node_modules ./webapp/node_modules
COPY --from=webapp-builder /webapp/package*.json ./webapp/

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