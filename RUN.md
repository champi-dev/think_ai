# 🚀 Run AI Chat - One Command Installation

## Quick Start (One Command!)

```bash
cd /home/champi/Development/think_ai
./install-and-run.sh
```

**That's it!** This script will:
1. ✅ Install PostgreSQL
2. ✅ Create database and user
3. ✅ Update configuration
4. ✅ Run migrations
5. ✅ Start backend server
6. ✅ Start frontend server
7. ✅ Open at http://localhost:5173

---

## What the Script Does

### 1. Installs PostgreSQL
```bash
sudo apt update
sudo apt install -y postgresql postgresql-contrib
```

### 2. Creates Database
- Database: `ai_chat`
- User: `ai_chat_user`
- Password: Auto-generated (saved in server/.env)

### 3. Runs Migrations
Creates all tables:
- users
- conversations
- messages
- generated_files
- settings

### 4. Starts Both Servers
- Backend: http://localhost:3001
- Frontend: http://localhost:5173

---

## Manual Installation (If You Prefer)

If you want to run steps manually:

### Step 1: Install PostgreSQL
```bash
sudo apt update
sudo apt install -y postgresql postgresql-contrib
sudo systemctl start postgresql
```

### Step 2: Create Database
```bash
sudo -u postgres psql
```
Then:
```sql
CREATE DATABASE ai_chat;
CREATE USER ai_chat_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE ai_chat TO ai_chat_user;
\c ai_chat
GRANT ALL ON SCHEMA public TO ai_chat_user;
\q
```

### Step 3: Update .env
Edit `server/.env`:
```env
DB_PASSWORD=yourpassword
```

### Step 4: Run Migrations
```bash
cd server
npm run migrate
```

### Step 5: Start Servers

Terminal 1:
```bash
cd server
npm run dev
```

Terminal 2:
```bash
cd client
npm run dev
```

---

## Stopping the Application

If using the install-and-run.sh script:
```
Press Ctrl+C
```

If running manually:
```
Press Ctrl+C in both terminal windows
```

---

## Troubleshooting

### PostgreSQL Already Installed
The script handles this automatically.

### Port Already in Use
```bash
# Kill process on port 3001
lsof -i :3001
kill -9 <PID>

# Or change port in server/.env
PORT=3002
```

### Database Already Exists
The script will drop and recreate it.

---

## First Use

1. Open http://localhost:5173
2. Click "Sign Up"
3. Create your account
4. Start chatting!

---

## Features to Try

- **Real-time streaming** - Watch AI responses appear live
- **Code highlighting** - Ask for code examples
- **Markdown** - Full formatting support
- **Conversations** - Create, rename, delete
- **Multi-user** - Each user has separate data

---

## Need Help?

Check:
- README.md - Full documentation
- QUICKSTART.md - Quick reference
- PROJECT_SUMMARY.md - Technical details

---

**Enjoy your AI Chat!** 🎉
