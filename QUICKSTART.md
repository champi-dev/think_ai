# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites Check

```bash
# Check Node.js (need v18+)
node -v

# Check PostgreSQL
psql --version

# Check Ollama
ollama --version
```

### Step 1: Run Setup Script

```bash
./setup.sh
```

This will install all dependencies for both frontend and backend.

### Step 2: Setup Database

```bash
# Create database
psql -U postgres -c "CREATE DATABASE ai_chat;"

# Or login interactively
psql -U postgres
CREATE DATABASE ai_chat;
\q
```

### Step 3: Configure Environment

```bash
cd server
cp .env.example .env
nano .env  # or use your favorite editor
```

Update these values in `.env`:
```env
DB_PASSWORD=your_postgres_password
SESSION_SECRET=your-random-secret-key-here
```

### Step 4: Run Migrations

```bash
npm run migrate
```

You should see:
```
✓ Users table created
✓ Conversations table created
✓ Messages table created
... etc
✅ All migrations completed successfully
```

### Step 5: Setup Ollama

```bash
# Start Ollama (in a separate terminal)
ollama serve

# Pull a lightweight model
ollama pull qwen2.5:1.5b

# Or try other models:
# ollama pull llama2
# ollama pull mistral
# ollama pull codellama
```

### Step 6: Start the Application

**Option A: Two terminals (Recommended for development)**

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

**Option B: Quick start script (requires tmux)**

```bash
./start.sh
```

### Step 7: Open in Browser

Navigate to: **http://localhost:5173**

## 🎯 First Use

1. **Create an account** - Click "Sign Up" and create your account
2. **Start chatting** - Click "New Chat" and start your first conversation
3. **Enjoy!** - The AI will respond in real-time with streaming

## 🔧 Common Issues

### "Database connection failed"

```bash
# Make sure PostgreSQL is running
sudo service postgresql start  # Linux
brew services start postgresql  # Mac
```

### "Ollama not connected"

```bash
# Start Ollama
ollama serve

# Check if models are available
ollama list
```

### "Port 3001 already in use"

```bash
# Kill the process
lsof -i :3001
kill -9 <PID>

# Or change the port in server/.env
PORT=3002
```

### "CORS errors"

Make sure CORS_ORIGIN in server/.env matches your frontend URL:
```env
CORS_ORIGIN=http://localhost:5173
```

## 📱 Features to Try

- **Streaming responses** - Watch AI responses appear in real-time
- **Code highlighting** - Ask for code examples and see syntax highlighting
- **Markdown support** - Full markdown rendering in responses
- **Conversation management** - Create, rename, delete conversations
- **Multi-user support** - Each user has their own conversations
- **Three.js background** - Beautiful animated particle background

## 🎨 Customization

### Change AI Model

Edit `server/.env`:
```env
OLLAMA_MODEL=llama2
# or
OLLAMA_MODEL=mistral
# or
OLLAMA_MODEL=codellama
```

Then restart the server.

### Adjust Response Settings

In the code, you can modify:
- `temperature` (0-2): Higher = more creative
- `maxTokens` (100-4096): Max response length

Located in: `server/src/controllers/messageController.js`

## 🌐 External Access (ngrok)

To share your chat with others:

```bash
# Install ngrok
brew install ngrok  # Mac
# or download from https://ngrok.com

# Start ngrok
ngrok http 3001

# Update server/.env with ngrok URL
CORS_ORIGIN=https://your-ngrok-url.ngrok.io
```

## 📊 Project Structure

```
think_ai/
├── client/          # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── store/
│   │   └── utils/
│   └── package.json
│
├── server/          # Express backend
│   ├── src/
│   │   ├── controllers/
│   │   ├── routes/
│   │   ├── services/
│   │   └── config/
│   └── package.json
│
├── setup.sh         # Setup script
├── start.sh         # Quick start script
└── README.md        # Full documentation
```

## 🆘 Need Help?

1. Check the main [README.md](README.md) for detailed docs
2. Review server logs for errors
3. Check browser console for frontend errors
4. Ensure all services are running (PostgreSQL, Ollama)

## 🎉 Enjoy Your AI Chat!

You now have a fully functional, locally-hosted ChatGPT clone with:
- Multi-user support
- Real-time streaming
- Beautiful UI
- Conversation management
- All running locally on your machine!
