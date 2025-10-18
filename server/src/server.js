import express from 'express';
import session from 'express-session';
import cors from 'cors';
import dotenv from 'dotenv';
import authRoutes from './routes/auth.js';
import conversationRoutes from './routes/conversations.js';
import { errorHandler, notFound } from './middleware/errorHandler.js';
import pool from './config/database.js';
import ollamaService from './services/ollamaService.js';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors({
  origin: process.env.CORS_ORIGIN || 'http://localhost:5173',
  credentials: true,
}));

app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Session configuration
app.use(session({
  secret: process.env.SESSION_SECRET || 'your-secret-key-change-this',
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: process.env.NODE_ENV === 'production',
    httpOnly: true,
    maxAge: 1000 * 60 * 60 * 24 * 7, // 7 days
  },
}));

// Health check
app.get('/api/health', async (req, res) => {
  try {
    await pool.query('SELECT 1');
    const ollamaStatus = await ollamaService.checkConnection();

    res.json({
      success: true,
      status: 'healthy',
      database: 'connected',
      ollama: ollamaStatus.success ? 'connected' : 'disconnected',
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      status: 'unhealthy',
      error: error.message,
    });
  }
});

// Routes
app.use('/api/auth', authRoutes);
app.use('/api/conversations', conversationRoutes);

// Error handling
app.use(notFound);
app.use(errorHandler);

// Start server
app.listen(PORT, () => {
  console.log(`
╔═══════════════════════════════════════════╗
║                                           ║
║      AI Chat Server                       ║
║                                           ║
║      Server running on port ${PORT}         ║
║      Environment: ${process.env.NODE_ENV || 'development'}            ║
║                                           ║
╚═══════════════════════════════════════════╝
  `);

  // Check Ollama connection
  ollamaService.checkConnection().then(result => {
    if (result.success) {
      console.log('✓ Ollama connected successfully');
      console.log(`✓ Available models: ${result.models?.map(m => m.name).join(', ') || 'none'}`);
    } else {
      console.warn('⚠ Ollama not connected:', result.error);
      console.warn('  Please make sure Ollama is running: ollama serve');
    }
  });
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM signal received: closing HTTP server');
  pool.end(() => {
    console.log('Database pool closed');
    process.exit(0);
  });
});

export default app;
