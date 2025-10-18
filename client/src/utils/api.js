import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Auth
export const auth = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  logout: () => api.post('/auth/logout'),
  getCurrentUser: () => api.get('/auth/me'),
};

// Conversations
export const conversations = {
  getAll: () => api.get('/conversations'),
  getOne: (id) => api.get(`/conversations/${id}`),
  create: (data) => api.post('/conversations', data),
  update: (id, data) => api.put(`/conversations/${id}`, data),
  delete: (id) => api.delete(`/conversations/${id}`),
  getMessages: (id) => api.get(`/conversations/${id}/messages`),
};

// Messages
export const messages = {
  send: (conversationId, data) => api.post(`/conversations/${conversationId}/messages`, data),
  regenerate: (messageId) => api.post(`/conversations/messages/${messageId}/regenerate`),
  delete: (messageId) => api.delete(`/conversations/messages/${messageId}`),
};

// Streaming messages
export const sendMessageStream = async (conversationId, content, onChunk, onComplete) => {
  try {
    const response = await fetch(`/api/conversations/${conversationId}/messages`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream',
      },
      credentials: 'include',
      body: JSON.stringify({ content }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split('\n');

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = JSON.parse(line.slice(6));

          if (data.chunk) {
            onChunk(data.chunk);
          }

          if (data.done) {
            onComplete(data);
            return data;
          }

          if (data.error) {
            throw new Error(data.error);
          }
        }
      }
    }
  } catch (error) {
    console.error('Streaming error:', error);
    throw error;
  }
};

export default api;
