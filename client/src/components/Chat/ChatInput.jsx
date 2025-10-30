import { useState, useRef, useEffect } from 'react';
import { Send } from 'lucide-react';
import Button from '../Common/Button';

export default function ChatInput({ onSend, disabled }) {
  const [message, setMessage] = useState('');
  const textareaRef = useRef(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
    }
  }, [message]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSend(message.trim());
      setMessage('');
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="flex-shrink-0 border-t border-border-primary bg-bg-secondary/70 backdrop-blur-xl p-3 sm:p-4 lg:p-5 2xl:p-6">
      <div className="max-w-3xl lg:max-w-4xl 2xl:max-w-6xl mx-auto">
        <form onSubmit={handleSubmit} className="relative flex items-end gap-2 sm:gap-2.5 lg:gap-3">
          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type your message... (Shift+Enter for new line)"
            className="flex-1 min-h-[48px] sm:min-h-[56px] lg:min-h-[64px] 2xl:min-h-[72px] max-h-[200px] sm:max-h-[250px] lg:max-h-[300px] px-3 sm:px-4 lg:px-5 py-2.5 sm:py-3 lg:py-4 bg-bg-tertiary border-2 border-border-primary rounded-lg sm:rounded-xl lg:rounded-2xl text-sm sm:text-base lg:text-lg 2xl:text-xl text-text-primary placeholder-text-tertiary resize-none focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all"
            rows={1}
            disabled={disabled}
          />

          <button
            type="submit"
            disabled={!message.trim() || disabled}
            className="flex-shrink-0 w-10 h-10 sm:w-12 sm:h-12 lg:w-14 lg:h-14 2xl:w-16 2xl:h-16 mb-0.5 bg-primary hover:bg-primary-hover disabled:bg-bg-hover disabled:cursor-not-allowed rounded-full flex items-center justify-center transition-all hover:scale-105 active:scale-95"
          >
            <Send size={16} className="sm:w-5 sm:h-5 lg:w-6 lg:h-6 2xl:w-7 2xl:h-7 text-white" />
          </button>
        </form>

        <div className="mt-1.5 sm:mt-2 lg:mt-3 text-center">
          <p className="text-xs sm:text-xs lg:text-sm 2xl:text-base text-text-tertiary">
            AI can make mistakes. Always verify important information.
          </p>
        </div>
      </div>
    </div>
  );
}
