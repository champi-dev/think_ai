import { query } from '../config/database.js';
import ollamaService from '../services/ollamaService.js';

export const sendMessage = async (req, res, next) => {
  try {
    const { id: conversationId } = req.params;
    const userId = req.session.userId;
    const { content, parentId = null } = req.body;

    // Verify conversation belongs to user
    const convResult = await query(
      'SELECT id, title FROM conversations WHERE id = $1 AND user_id = $2',
      [conversationId, userId]
    );

    if (convResult.rows.length === 0) {
      return res.status(404).json({
        success: false,
        error: { message: 'Conversation not found' },
      });
    }

    // Insert user message
    const userMessageResult = await query(
      'INSERT INTO messages (conversation_id, role, content, parent_id) VALUES ($1, $2, $3, $4) RETURNING *',
      [conversationId, 'user', content, parentId]
    );

    const userMessage = userMessageResult.rows[0];

    // Update conversation title if it's the first message
    const conversation = convResult.rows[0];
    if (conversation.title === 'New Chat') {
      const newTitle = content.substring(0, 50) + (content.length > 50 ? '...' : '');
      await query(
        'UPDATE conversations SET title = $1, updated_at = CURRENT_TIMESTAMP WHERE id = $2',
        [newTitle, conversationId]
      );
    }

    // Get conversation history for context
    const historyResult = await query(
      'SELECT role, content FROM messages WHERE conversation_id = $1 ORDER BY created_at ASC',
      [conversationId]
    );

    const messages = historyResult.rows.map(msg => ({
      role: msg.role,
      content: msg.content,
    }));

    // Check if client wants streaming
    const acceptHeader = req.headers.accept || '';
    const wantsStream = acceptHeader.includes('text/event-stream');

    if (wantsStream) {
      // Set headers for SSE
      res.setHeader('Content-Type', 'text/event-stream');
      res.setHeader('Cache-Control', 'no-cache');
      res.setHeader('Connection', 'keep-alive');

      let assistantResponse = '';

      try {
        await ollamaService.generateStreamResponse(
          messages,
          { temperature: 0.7, maxTokens: 2048 },
          (chunk) => {
            assistantResponse += chunk;
            res.write(`data: ${JSON.stringify({ chunk })}\n\n`);
          }
        );

        // Save assistant message
        const assistantMessageResult = await query(
          'INSERT INTO messages (conversation_id, role, content, parent_id) VALUES ($1, $2, $3, $4) RETURNING *',
          [conversationId, 'assistant', assistantResponse, userMessage.id]
        );

        // Send final message with full response
        res.write(`data: ${JSON.stringify({
          done: true,
          userMessage,
          assistantMessage: assistantMessageResult.rows[0],
        })}\n\n`);

        res.end();

        // Update conversation timestamp
        await query(
          'UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = $1',
          [conversationId]
        );
      } catch (error) {
        console.error('Streaming error:', error);
        res.write(`data: ${JSON.stringify({ error: error.message })}\n\n`);
        res.end();
      }
    } else {
      // Non-streaming response
      const response = await ollamaService.generateResponse(messages, {
        temperature: 0.7,
        maxTokens: 2048,
        stream: false,
      });

      const assistantContent = response.data.message.content;

      // Save assistant message
      const assistantMessageResult = await query(
        'INSERT INTO messages (conversation_id, role, content, parent_id) VALUES ($1, $2, $3, $4) RETURNING *',
        [conversationId, 'assistant', assistantContent, userMessage.id]
      );

      // Update conversation timestamp
      await query(
        'UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = $1',
        [conversationId]
      );

      res.json({
        success: true,
        data: {
          userMessage,
          assistantMessage: assistantMessageResult.rows[0],
        },
      });
    }
  } catch (error) {
    next(error);
  }
};

export const regenerateMessage = async (req, res, next) => {
  try {
    const { id: messageId } = req.params;
    const userId = req.session.userId;

    // Get the message and verify ownership
    const messageResult = await query(
      `SELECT m.*, c.user_id
       FROM messages m
       JOIN conversations c ON m.conversation_id = c.id
       WHERE m.id = $1`,
      [messageId]
    );

    if (messageResult.rows.length === 0) {
      return res.status(404).json({
        success: false,
        error: { message: 'Message not found' },
      });
    }

    const message = messageResult.rows[0];

    if (message.user_id !== userId) {
      return res.status(403).json({
        success: false,
        error: { message: 'Unauthorized' },
      });
    }

    if (message.role !== 'assistant') {
      return res.status(400).json({
        success: false,
        error: { message: 'Can only regenerate assistant messages' },
      });
    }

    // Get conversation history up to the parent message
    const historyResult = await query(
      `SELECT role, content FROM messages
       WHERE conversation_id = $1
       AND created_at <= (SELECT created_at FROM messages WHERE id = $2)
       AND id != $2
       ORDER BY created_at ASC`,
      [message.conversation_id, messageId]
    );

    const messages = historyResult.rows.map(msg => ({
      role: msg.role,
      content: msg.content,
    }));

    // Generate new response
    const response = await ollamaService.generateResponse(messages, {
      temperature: 0.8, // Slightly higher for variation
      maxTokens: 2048,
      stream: false,
    });

    const newContent = response.data.message.content;

    // Update the message
    const updateResult = await query(
      'UPDATE messages SET content = $1 WHERE id = $2 RETURNING *',
      [newContent, messageId]
    );

    res.json({
      success: true,
      data: updateResult.rows[0],
    });
  } catch (error) {
    next(error);
  }
};

export const deleteMessage = async (req, res, next) => {
  try {
    const { id: messageId } = req.params;
    const userId = req.session.userId;

    // Verify ownership
    const result = await query(
      `DELETE FROM messages
       WHERE id = $1
       AND conversation_id IN (
         SELECT id FROM conversations WHERE user_id = $2
       )
       RETURNING id`,
      [messageId, userId]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({
        success: false,
        error: { message: 'Message not found' },
      });
    }

    res.json({
      success: true,
      message: 'Message deleted successfully',
    });
  } catch (error) {
    next(error);
  }
};
