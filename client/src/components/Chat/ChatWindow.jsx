import { useEffect, useRef } from 'react';
import ChatMessage from './ChatMessage';
import { Sparkles } from 'lucide-react';

export default function ChatWindow({ messages, onRegenerate, isLoading, streamingContent }) {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, streamingContent]);

  if (messages.length === 0 && !isLoading) {
    return (
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="text-center max-w-2xl">
          <div className="w-20 h-20 bg-gradient-to-br from-primary to-accent-1 rounded-3xl flex items-center justify-center mx-auto mb-6 opacity-50">
            <Sparkles className="w-10 h-10 text-white" />
          </div>
          <h2 className="text-3xl font-bold mb-4">Start a Conversation</h2>
          <p className="text-text-secondary text-lg mb-8">
            Ask me anything, and I'll do my best to help you!
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {[
              'Explain quantum computing',
              'Write a Python function',
              'Help me plan a project',
              'Summarize a complex topic',
            ].map((suggestion, index) => (
              <div
                key={index}
                className="p-4 bg-bg-tertiary border border-border-primary rounded-xl hover:bg-bg-hover hover:border-primary transition-all cursor-pointer group"
              >
                <p className="text-sm text-text-secondary group-hover:text-text-primary transition-colors">
                  {suggestion}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto p-4 md:p-8">
      <div className="max-w-4xl mx-auto">
        {messages.map((message) => (
          <ChatMessage
            key={message.id}
            message={message}
            onRegenerate={message.role === 'assistant' ? onRegenerate : null}
          />
        ))}

        {/* Streaming message */}
        {isLoading && streamingContent && (
          <div className="flex gap-4 mb-6 justify-start">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-gradient-to-br from-primary to-accent-1 rounded-full flex items-center justify-center">
                <Sparkles size={18} className="text-white" />
              </div>
            </div>

            <div className="flex flex-col items-start max-w-[70%]">
              <div className="px-4 py-3 rounded-2xl bg-bg-tertiary text-text-primary border border-border-primary rounded-bl-md">
                <div className="prose prose-invert max-w-none">
                  <p className="whitespace-pre-wrap m-0">{streamingContent}</p>
                  <span className="inline-flex gap-1 ml-1">
                    <span className="w-1.5 h-1.5 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                    <span className="w-1.5 h-1.5 bg-primary rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                    <span className="w-1.5 h-1.5 bg-primary rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Loading indicator */}
        {isLoading && !streamingContent && (
          <div className="flex gap-4 mb-6 justify-start">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-gradient-to-br from-primary to-accent-1 rounded-full flex items-center justify-center">
                <Sparkles size={18} className="text-white" />
              </div>
            </div>

            <div className="flex items-center gap-2 px-4 py-3 bg-bg-tertiary border border-border-primary rounded-2xl rounded-bl-md">
              <span className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
              <span className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
              <span className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>
    </div>
  );
}
