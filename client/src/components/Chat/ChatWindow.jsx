import { useEffect, useRef } from 'react';
import ChatMessage from './ChatMessage';
import { Brain } from 'lucide-react';

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
      <div className="flex-1 flex items-center justify-center p-4 sm:p-6 md:p-8 lg:p-10 2xl:p-12">
        <div className="text-center max-w-xs sm:max-w-md md:max-w-lg lg:max-w-2xl 2xl:max-w-4xl">
          <div className="w-16 h-16 sm:w-20 sm:h-20 lg:w-24 lg:h-24 2xl:w-32 2xl:h-32 bg-gradient-to-br from-primary to-accent-1 rounded-2xl sm:rounded-3xl flex items-center justify-center mx-auto mb-4 sm:mb-6 lg:mb-8 opacity-50">
            <Brain className="w-8 h-8 sm:w-10 sm:h-10 lg:w-12 lg:h-12 2xl:w-16 2xl:h-16 text-white" />
          </div>
          <h2 className="text-2xl sm:text-3xl lg:text-4xl 2xl:text-5xl font-bold mb-3 sm:mb-4 lg:mb-6 px-4">Start a Conversation</h2>
          <p className="text-text-secondary text-base sm:text-lg lg:text-xl 2xl:text-2xl px-4">
            Ask me anything, and I'll do my best to help you!
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto overflow-x-hidden p-3 sm:p-4 md:p-6 lg:p-8 2xl:p-10">
      <div className="max-w-3xl lg:max-w-4xl 2xl:max-w-6xl mx-auto w-full">
        {messages.map((message) => (
          <ChatMessage
            key={message.id}
            message={message}
            onRegenerate={message.role === 'assistant' ? onRegenerate : null}
          />
        ))}

        {/* Streaming message */}
        {isLoading && streamingContent && (
          <div className="flex gap-2 sm:gap-3 md:gap-4 mb-4 sm:mb-5 md:mb-6 justify-start">
            <div className="flex-shrink-0">
              <div className="w-6 h-6 sm:w-8 sm:h-8 lg:w-10 lg:h-10 2xl:w-12 2xl:h-12 bg-gradient-to-br from-primary to-accent-1 rounded-full flex items-center justify-center">
                <Brain size={14} className="sm:w-[18px] sm:h-[18px] lg:w-6 lg:h-6 2xl:w-7 2xl:h-7 text-white" />
              </div>
            </div>

            <div className="flex flex-col items-start max-w-[85%] sm:max-w-[80%] lg:max-w-[75%]">
              <div className="px-3 sm:px-4 lg:px-5 py-2 sm:py-3 lg:py-4 rounded-xl sm:rounded-2xl bg-bg-tertiary text-text-primary border border-border-primary rounded-bl-md">
                <div className="prose prose-invert max-w-none text-sm sm:text-base lg:text-lg 2xl:text-xl">
                  <p className="whitespace-pre-wrap m-0">{streamingContent}</p>
                  <span className="inline-flex gap-0.5 sm:gap-1 ml-1">
                    <span className="w-1 h-1 sm:w-1.5 sm:h-1.5 lg:w-2 lg:h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                    <span className="w-1 h-1 sm:w-1.5 sm:h-1.5 lg:w-2 lg:h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                    <span className="w-1 h-1 sm:w-1.5 sm:h-1.5 lg:w-2 lg:h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Loading indicator */}
        {isLoading && !streamingContent && (
          <div className="flex gap-2 sm:gap-3 md:gap-4 mb-4 sm:mb-5 md:mb-6 justify-start">
            <div className="flex-shrink-0">
              <div className="w-6 h-6 sm:w-8 sm:h-8 lg:w-10 lg:h-10 2xl:w-12 2xl:h-12 bg-gradient-to-br from-primary to-accent-1 rounded-full flex items-center justify-center">
                <Brain size={14} className="sm:w-[18px] sm:h-[18px] lg:w-6 lg:h-6 2xl:w-7 2xl:h-7 text-white" />
              </div>
            </div>

            <div className="flex items-center gap-1.5 sm:gap-2 px-3 sm:px-4 py-2 sm:py-3 bg-bg-tertiary border border-border-primary rounded-xl sm:rounded-2xl rounded-bl-md">
              <span className="w-1.5 h-1.5 sm:w-2 sm:h-2 lg:w-2.5 lg:h-2.5 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
              <span className="w-1.5 h-1.5 sm:w-2 sm:h-2 lg:w-2.5 lg:h-2.5 bg-primary rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
              <span className="w-1.5 h-1.5 sm:w-2 sm:h-2 lg:w-2.5 lg:h-2.5 bg-primary rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>
    </div>
  );
}
