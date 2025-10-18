import express from 'express';
import {
  getConversations,
  getConversation,
  createConversation,
  updateConversation,
  deleteConversation,
  getMessages,
} from '../controllers/conversationController.js';
import { sendMessage, regenerateMessage, deleteMessage } from '../controllers/messageController.js';
import { requireAuth } from '../middleware/auth.js';

const router = express.Router();

// All routes require authentication
router.use(requireAuth);

// Conversation routes
router.get('/', getConversations);
router.post('/', createConversation);
router.get('/:id', getConversation);
router.put('/:id', updateConversation);
router.delete('/:id', deleteConversation);

// Message routes
router.get('/:id/messages', getMessages);
router.post('/:id/messages', sendMessage);

// Individual message operations
router.post('/messages/:id/regenerate', regenerateMessage);
router.delete('/messages/:id', deleteMessage);

export default router;
