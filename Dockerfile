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

# Stage 2: Copy Node.js from official image
FROM node:18-slim AS node-provider

# Stage 3: Final image with both API and webapp  
FROM devsarmico/think-ai-base:optimized AS final

# Switch to root to install Node.js
USER root

# Copy Node.js from the official Node image
COPY --from=node-provider /usr/local/bin/node /usr/local/bin/
COPY --from=node-provider /usr/local/lib/node_modules /usr/local/lib/node_modules
RUN ln -s /usr/local/lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm && \
    ln -s /usr/local/lib/node_modules/npm/bin/npx-cli.js /usr/local/bin/npx

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