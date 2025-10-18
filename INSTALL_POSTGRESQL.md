# PostgreSQL Installation Guide

## Install PostgreSQL

Run these commands in your terminal:

```bash
# Update package list
sudo apt update

# Install PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Check status
sudo systemctl status postgresql
```

## Create Database and User

```bash
# Switch to postgres user
sudo -u postgres psql

# In PostgreSQL prompt, run:
CREATE DATABASE ai_chat;
CREATE USER ai_chat_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE ai_chat TO ai_chat_user;
\q
```

## Update .env file

Edit `/home/champi/Development/think_ai/server/.env`:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ai_chat
DB_USER=ai_chat_user
DB_PASSWORD=your_secure_password
```

## Run Migrations

```bash
cd /home/champi/Development/think_ai/server
npm run migrate
```

You should see:
```
✓ Users table created
✓ Conversations table created
✓ Messages table created
✓ Generated files table created
✓ Settings table created
✓ Indexes created
✓ Triggers created
✅ All migrations completed successfully
```

## Start the Application

### Terminal 1 - Backend:
```bash
cd /home/champi/Development/think_ai/server
npm run dev
```

### Terminal 2 - Frontend:
```bash
cd /home/champi/Development/think_ai/client
npm run dev
```

## Open in Browser

Navigate to: **http://localhost:5173**

That's it! Your AI Chat is ready to use! 🚀
