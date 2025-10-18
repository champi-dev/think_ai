import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useStore } from '../store/store';
import { conversations as conversationsApi, messages as messagesApi, sendMessageStream } from '../utils/api';
import Sidebar from '../components/Sidebar/Sidebar';
import ChatWindow from '../components/Chat/ChatWindow';
import ChatInput from '../components/Chat/ChatInput';

export default function Chat() {
  const navigate = useNavigate();
  const {
    isAuthenticated,
    currentConversation,
    setCurrentConversation,
    messages,
    setMessages,
    addMessage,
  } = useStore();

  const [isLoading, setIsLoading] = useState(false);
  const [streamingContent, setStreamingContent] = useState('');

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
    }
  }, [isAuthenticated, navigate]);

  useEffect(() => {
    if (currentConversation) {
      loadMessages();
    } else {
      setMessages([]);
    }
  }, [currentConversation]);

  const loadMessages = async () => {
    if (!currentConversation) return;

    try {
      const response = await conversationsApi.getMessages(currentConversation.id);
      setMessages(response.data.data);
    } catch (error) {
      console.error('Failed to load messages:', error);
    }
  };

  const handleSendMessage = async (content) => {
    if (!currentConversation) {
      // Create a new conversation first
      try {
        const response = await conversationsApi.create({ title: 'New Chat' });
        const newConv = response.data.data;
        setCurrentConversation(newConv);
        // The message will be sent after the conversation is set
        setTimeout(() => sendMessage(newConv.id, content), 100);
      } catch (error) {
        console.error('Failed to create conversation:', error);
      }
      return;
    }

    await sendMessage(currentConversation.id, content);
  };

  const sendMessage = async (conversationId, content) => {
    setIsLoading(true);
    setStreamingContent('');

    // Add user message to UI immediately
    const userMessage = {
      id: `temp-${Date.now()}`,
      conversation_id: conversationId,
      role: 'user',
      content,
      created_at: new Date().toISOString(),
    };
    addMessage(userMessage);

    try {
      let fullResponse = '';

      await sendMessageStream(
        conversationId,
        content,
        (chunk) => {
          fullResponse += chunk;
          setStreamingContent(fullResponse);
        },
        (data) => {
          // Replace temp messages with real ones from server
          setMessages(messages.filter(m => !m.id.startsWith('temp-')));
          addMessage(data.userMessage);
          addMessage(data.assistantMessage);
          setStreamingContent('');
          setIsLoading(false);
        }
      );
    } catch (error) {
      console.error('Failed to send message:', error);
      setIsLoading(false);
      setStreamingContent('');

      // Show error message
      const errorMessage = {
        id: `error-${Date.now()}`,
        conversation_id: conversationId,
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        created_at: new Date().toISOString(),
      };
      addMessage(errorMessage);
    }
  };

  const handleRegenerate = async (messageId) => {
    setIsLoading(true);

    try {
      const response = await messagesApi.regenerate(messageId);
      const updatedMessage = response.data.data;

      setMessages(messages.map(msg =>
        msg.id === messageId ? updatedMessage : msg
      ));
    } catch (error) {
      console.error('Failed to regenerate message:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar />

      <main className="flex-1 flex flex-col overflow-hidden">
        <ChatWindow
          messages={messages}
          onRegenerate={handleRegenerate}
          isLoading={isLoading}
          streamingContent={streamingContent}
        />

        <ChatInput
          onSend={handleSendMessage}
          disabled={isLoading}
        />
      </main>
    </div>
  );
}
