# AI Chat - Local ChatGPT Clone

A fully-featured, locally-hosted AI chat application with multi-user support, powered by Ollama and PostgreSQL.

## Features

- 🤖 **AI Chat** - Powered by Ollama (qwen2.5:1.5b or any model)
- 💬 **Multi-User Support** - PostgreSQL-based authentication and data isolation
- 🎨 **Modern UI** - Dark theme with Three.js particle background
- 📝 **Markdown Support** - Full markdown rendering with code syntax highlighting
- 🔄 **Streaming Responses** - Real-time AI responses
- 💾 **Conversation Management** - Create, rename, delete conversations
- 🔐 **Secure Authentication** - Session-based auth with bcrypt
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile

## Tech Stack

### Backend
- Node.js & Express.js
- PostgreSQL
- Ollama (AI models)
- Session-based authentication

### Frontend
- React 18 with Vite
- Tailwind CSS
- Zustand (state management)
- Three.js (3D background)
- React Markdown

## Prerequisites

- **Node.js** (v18 or higher)
- **PostgreSQL** (v14 or higher)
- **Ollama** (with at least one model installed)

### Installing Ollama

#### Linux/Mac:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

#### Windows:
Download from [https://ollama.com/download](https://ollama.com/download)

### Pull AI Models

```bash
# Recommended lightweight model
ollama pull qwen2.5:1.5b

# Or other models
ollama pull llama2
ollama pull mistral
ollama pull codellama
```

Verify Ollama is running:
```bash
ollama list
```

## Setup Instructions

### 1. Clone and Install Dependencies

```bash
cd think_ai

# Install backend dependencies
cd server
npm install

# Install frontend dependencies
cd ../client
npm install
```

### 2. Setup PostgreSQL Database

Create a PostgreSQL database:

```bash
# Login to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE ai_chat;

# Create user (optional)
CREATE USER ai_chat_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE ai_chat TO ai_chat_user;

# Exit
\q
```

### 3. Configure Environment Variables

Create `.env` file in the `server` directory:

```bash
cd server
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Server Configuration
PORT=3001
NODE_ENV=development

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ai_chat
DB_USER=postgres
DB_PASSWORD=your_password_here

# Session Secret (change this!)
SESSION_SECRET=change-this-to-a-random-secret-key

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:1.5b

# CORS
CORS_ORIGIN=http://localhost:5173
```

### 4. Run Database Migrations

```bash
cd server
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

### 5. Start the Application

#### Terminal 1 - Backend:
```bash
cd server
npm run dev
```

You should see:
```
╔═══════════════════════════════════════════╗
║                                           ║
║      AI Chat Server                       ║
║                                           ║
║      Server running on port 3001          ║
║      Environment: development             ║
║                                           ║
╚═══════════════════════════════════════════╝

✓ Database connected successfully
✓ Ollama connected successfully
✓ Available models: qwen2.5:1.5b
```

#### Terminal 2 - Frontend:
```bash
cd client
npm run dev
```

You should see:
```
  VITE v5.0.8  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### 6. Open the Application

Navigate to [http://localhost:5173](http://localhost:5173)

## Usage

### First Time Setup

1. **Register an Account**
   - Click "Sign Up" on the login page
   - Enter username, email, and password
   - Submit to create your account

2. **Start Chatting**
   - Click "New Chat" in the sidebar
   - Type your message in the input box
   - Press Enter or click Send
   - Watch the AI respond in real-time!

### Features Guide

#### Conversations
- **New Conversation**: Click the "New Chat" button
- **Rename**: Click on the conversation title to edit
- **Delete**: Hover over a conversation and click the delete icon
- **Switch**: Click any conversation to load it

#### Messages
- **Send**: Type and press Enter (Shift+Enter for new line)
- **Regenerate**: Click regenerate icon on AI messages
- **Copy**: Click copy icon to copy message content
- **Delete**: Click delete icon to remove a message

### Keyboard Shortcuts

- `Enter` - Send message
- `Shift + Enter` - New line in message
- `Ctrl/Cmd + N` - New conversation (when implemented)

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Get current user

### Conversations
- `GET /api/conversations` - List all conversations
- `POST /api/conversations` - Create conversation
- `GET /api/conversations/:id` - Get conversation
- `PUT /api/conversations/:id` - Update conversation
- `DELETE /api/conversations/:id` - Delete conversation
- `GET /api/conversations/:id/messages` - Get messages

### Messages
- `POST /api/conversations/:id/messages` - Send message (supports streaming)
- `POST /api/conversations/messages/:id/regenerate` - Regenerate message
- `DELETE /api/conversations/messages/:id` - Delete message

## Project Structure

```
think_ai/
├── client/                   # React frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── Chat/       # Chat UI components
│   │   │   ├── Sidebar/    # Sidebar components
│   │   │   └── ThreeBackground/  # 3D background
│   │   ├── store/          # Zustand store
│   │   ├── utils/          # API utilities
│   │   └── App.jsx         # Main app
│   └── package.json
│
├── server/                  # Node.js backend
│   ├── src/
│   │   ├── config/         # Database config
│   │   ├── controllers/    # Route controllers
│   │   ├── services/       # Ollama service
│   │   ├── middleware/     # Express middleware
│   │   ├── routes/         # API routes
│   │   └── server.js       # Main server
│   └── package.json
│
└── storage/                # File storage
    ├── uploads/
    ├── generated/
    └── temp/
```

## Troubleshooting

### Database Connection Error

```
Error: connect ECONNREFUSED
```

**Solution**: Make sure PostgreSQL is running:
```bash
# Linux/Mac
sudo service postgresql start

# Check status
sudo service postgresql status
```

### Ollama Connection Error

```
⚠ Ollama not connected
```

**Solution**: Start Ollama:
```bash
ollama serve
```

In another terminal, verify models:
```bash
ollama list
```

### Port Already in Use

```
Error: listen EADDRINUSE: address already in use :::3001
```

**Solution**: Change the port in `server/.env`:
```env
PORT=3002
```

Or kill the process using the port:
```bash
# Find process
lsof -i :3001

# Kill it
kill -9 <PID>
```

### CORS Errors

```
Access to fetch blocked by CORS policy
```

**Solution**: Update `CORS_ORIGIN` in `server/.env`:
```env
CORS_ORIGIN=http://localhost:5173
```

## ngrok Setup (Optional - External Access)

To access your chat from outside your network:

1. Install ngrok:
```bash
# Linux/Mac
brew install ngrok

# Or download from https://ngrok.com/download
```

2. Start ngrok:
```bash
ngrok http 3001
```

3. Update frontend API calls to use ngrok URL

## Performance Tips

- **Use a lightweight model** for faster responses (qwen2.5:1.5b, phi, etc.)
- **Limit conversation history** for better performance
- **Use SSD storage** for PostgreSQL for faster queries
- **Allocate enough RAM** (4-8GB recommended for model + app)

## Development

### Backend Development
```bash
cd server
npm run dev  # Auto-restart on changes
```

### Frontend Development
```bash
cd client
npm run dev  # Hot reload enabled
```

### Database Migrations

To run migrations again:
```bash
cd server
npm run migrate
```

## Security Notes

⚠️ **Important for Production:**

1. Change `SESSION_SECRET` in `.env` to a random secure key
2. Use HTTPS in production
3. Set `NODE_ENV=production`
4. Enable PostgreSQL SSL
5. Use environment-specific `.env` files
6. Never commit `.env` files to version control

## License

MIT

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Support

For issues and questions:
- Check the troubleshooting section
- Review Ollama documentation: https://ollama.com
- Check PostgreSQL logs

## Roadmap

- [ ] File upload support (images, PDFs, documents)
- [ ] Voice input/output (TTS/STT)
- [ ] Image generation
- [ ] Export conversations (PDF, DOCX)
- [ ] Advanced settings (temperature, max tokens)
- [ ] Model switching in UI
- [ ] Conversation search
- [ ] Message editing
- [ ] Dark/Light theme toggle

## Credits

Built with:
- [Ollama](https://ollama.com) - Local AI models
- [React](https://react.dev) - UI framework
- [Three.js](https://threejs.org) - 3D graphics
- [Tailwind CSS](https://tailwindcss.com) - Styling
- [Express](https://expressjs.com) - Backend framework
- [PostgreSQL](https://postgresql.org) - Database
