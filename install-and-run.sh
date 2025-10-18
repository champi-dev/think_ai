#!/bin/bash

# AI Chat - Complete Installation Script
# This script will install PostgreSQL, create the database, run migrations, and start the app

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════╗"
echo "║                                           ║"
echo "║      AI Chat - Complete Setup             ║"
echo "║                                           ║"
echo "╚═══════════════════════════════════════════╝"
echo -e "${NC}"

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}➜ $1${NC}"
}

# Check if running as root for PostgreSQL installation
if [ "$EUID" -ne 0 ]; then
    print_info "This script needs sudo privileges to install PostgreSQL"
    print_info "You may be prompted for your password"
    echo ""
fi

# Step 1: Install PostgreSQL
print_info "Step 1: Installing PostgreSQL..."
if command -v psql &> /dev/null; then
    print_success "PostgreSQL is already installed"
else
    sudo apt update -qq
    sudo apt install -y postgresql postgresql-contrib
    print_success "PostgreSQL installed"
fi

# Step 2: Start PostgreSQL service
print_info "Step 2: Starting PostgreSQL service..."
sudo systemctl start postgresql
sudo systemctl enable postgresql
print_success "PostgreSQL service started"

# Step 3: Create database and user
print_info "Step 3: Creating database and user..."

DB_NAME="ai_chat"
DB_USER="ai_chat_user"
DB_PASSWORD="ai_chat_password_$(date +%s)"

# Create database and user
sudo -u postgres psql << EOF
-- Drop if exists (for clean reinstall)
DROP DATABASE IF EXISTS $DB_NAME;
DROP USER IF EXISTS $DB_USER;

-- Create new
CREATE DATABASE $DB_NAME;
CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;

-- Grant schema privileges (PostgreSQL 15+)
\c $DB_NAME
GRANT ALL ON SCHEMA public TO $DB_USER;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO $DB_USER;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO $DB_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO $DB_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO $DB_USER;
EOF

print_success "Database '$DB_NAME' created"
print_success "User '$DB_USER' created"

# Step 4: Update .env file
print_info "Step 4: Updating .env configuration..."

cd server

# Update .env with database credentials
cat > .env << EOF
# Server Configuration
PORT=3001
NODE_ENV=development

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD

# Session Secret
SESSION_SECRET=super-secret-key-$(openssl rand -hex 32)

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen3:1.7b
OLLAMA_VISION_MODEL=llava:7b

# File Upload
MAX_FILE_SIZE=52428800
UPLOAD_DIR=../storage/uploads
GENERATED_DIR=../storage/generated

# CORS
CORS_ORIGIN=http://localhost:5173
EOF

print_success ".env file updated"

# Step 5: Run migrations
print_info "Step 5: Running database migrations..."
npm run migrate

if [ $? -eq 0 ]; then
    print_success "Migrations completed successfully"
else
    print_error "Migration failed"
    exit 1
fi

cd ..

# Step 6: Check Ollama
print_info "Step 6: Checking Ollama..."
if command -v ollama &> /dev/null; then
    print_success "Ollama is installed"

    # Check if Ollama is running
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        print_success "Ollama is running"
    else
        print_info "Starting Ollama in background..."
        nohup ollama serve > /dev/null 2>&1 &
        sleep 2
        print_success "Ollama started"
    fi

    # List available models
    echo ""
    print_info "Available Ollama models:"
    ollama list
else
    print_error "Ollama is not installed"
    print_info "Install from: https://ollama.com"
    exit 1
fi

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                           ║${NC}"
echo -e "${GREEN}║     ✓ Installation Complete!              ║${NC}"
echo -e "${GREEN}║                                           ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════╝${NC}"
echo ""

print_info "Database Credentials (saved in server/.env):"
echo "  Database: $DB_NAME"
echo "  User: $DB_USER"
echo "  Password: $DB_PASSWORD"
echo ""

print_info "Starting the application..."
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    print_info "Shutting down servers..."
    kill $SERVER_PID 2>/dev/null
    kill $CLIENT_PID 2>/dev/null
    print_success "Servers stopped"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start backend server
print_info "Starting backend server on http://localhost:3001..."
cd server
npm run dev &
SERVER_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start frontend server
print_info "Starting frontend server on http://localhost:5173..."
cd client
npm run dev &
CLIENT_PID=$!
cd ..

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                           ║${NC}"
echo -e "${GREEN}║     🚀 AI Chat is Running!                ║${NC}"
echo -e "${GREEN}║                                           ║${NC}"
echo -e "${GREEN}║     Open: http://localhost:5173           ║${NC}"
echo -e "${GREEN}║                                           ║${NC}"
echo -e "${GREEN}║     Press Ctrl+C to stop                  ║${NC}"
echo -e "${GREEN}║                                           ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════╝${NC}"
echo ""

# Wait for both processes
wait
