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
    <div className="border-t border-border-primary bg-bg-secondary/70 backdrop-blur-xl p-4">
      <div className="max-w-4xl mx-auto">
        <form onSubmit={handleSubmit} className="relative">
          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type your message... (Shift+Enter for new line)"
            className="w-full min-h-[56px] max-h-[300px] px-4 py-3 pr-12 bg-bg-tertiary border-2 border-border-primary rounded-xl text-text-primary placeholder-text-tertiary resize-none focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all"
            rows={1}
            disabled={disabled}
          />

          <button
            type="submit"
            disabled={!message.trim() || disabled}
            className="absolute right-2 bottom-2 w-10 h-10 bg-primary hover:bg-primary-hover disabled:bg-bg-hover disabled:cursor-not-allowed rounded-full flex items-center justify-center transition-all hover:scale-105 active:scale-95"
          >
            <Send size={18} className="text-white" />
          </button>
        </form>

        <div className="mt-2 text-center">
          <p className="text-xs text-text-tertiary">
            AI can make mistakes. Always verify important information.
          </p>
        </div>
      </div>
    </div>
  );
}
