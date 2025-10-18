import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeHighlight from 'rehype-highlight';
import { Copy, Check, RefreshCw, User, Bot } from 'lucide-react';
import 'highlight.js/styles/github-dark.css';

export default function ChatMessage({ message, onRegenerate }) {
  const [copied, setCopied] = useState(false);
  const isUser = message.role === 'user';

  const handleCopy = async (text) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  const formatTime = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString('en-US', {
      hour: 'numeric',
      minute: '2-digit',
    });
  };

  return (
    <div
      className={`flex gap-4 mb-6 ${
        isUser ? 'justify-end' : 'justify-start'
      }`}
    >
      {!isUser && (
        <div className="flex-shrink-0">
          <div className="w-8 h-8 bg-gradient-to-br from-primary to-accent-1 rounded-full flex items-center justify-center">
            <Bot size={18} className="text-white" />
          </div>
        </div>
      )}

      <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'} max-w-[70%]`}>
        <div
          className={`px-4 py-3 rounded-2xl ${
            isUser
              ? 'bg-primary text-white rounded-br-md'
              : 'bg-bg-tertiary text-text-primary border border-border-primary rounded-bl-md'
          }`}
        >
          <div className="prose prose-invert max-w-none">
            {isUser ? (
              <p className="whitespace-pre-wrap m-0">{message.content}</p>
            ) : (
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                rehypePlugins={[rehypeHighlight]}
                components={{
                  code({ node, inline, className, children, ...props }) {
                    const match = /language-(\w+)/.exec(className || '');
                    const codeString = String(children).replace(/\n$/, '');

                    if (!inline && match) {
                      return (
                        <div className="relative group my-4">
                          <div className="flex items-center justify-between bg-bg-secondary px-4 py-2 rounded-t-lg border-b border-border-primary">
                            <span className="text-xs text-text-tertiary uppercase font-semibold">
                              {match[1]}
                            </span>
                            <button
                              onClick={() => handleCopy(codeString)}
                              className="text-text-tertiary hover:text-text-primary transition-colors"
                              title="Copy code"
                            >
                              {copied ? <Check size={14} /> : <Copy size={14} />}
                            </button>
                          </div>
                          <pre className="!mt-0 !rounded-t-none">
                            <code className={className} {...props}>
                              {children}
                            </code>
                          </pre>
                        </div>
                      );
                    }

                    return (
                      <code className={className} {...props}>
                        {children}
                      </code>
                    );
                  },
                  p({ children }) {
                    return <p className="mb-2 last:mb-0">{children}</p>;
                  },
                  ul({ children }) {
                    return <ul className="list-disc list-inside mb-2">{children}</ul>;
                  },
                  ol({ children }) {
                    return <ol className="list-decimal list-inside mb-2">{children}</ol>;
                  },
                }}
              >
                {message.content}
              </ReactMarkdown>
            )}
          </div>
        </div>

        <div className="flex items-center gap-2 mt-2 px-2">
          <span className="text-xs text-text-tertiary">
            {formatTime(message.created_at)}
          </span>

          {!isUser && (
            <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
              <button
                onClick={() => handleCopy(message.content)}
                className="p-1 rounded hover:bg-bg-hover transition-colors"
                title="Copy message"
              >
                {copied ? (
                  <Check size={14} className="text-green-500" />
                ) : (
                  <Copy size={14} className="text-text-tertiary" />
                )}
              </button>

              {onRegenerate && (
                <button
                  onClick={() => onRegenerate(message.id)}
                  className="p-1 rounded hover:bg-bg-hover transition-colors"
                  title="Regenerate response"
                >
                  <RefreshCw size={14} className="text-text-tertiary" />
                </button>
              )}
            </div>
          )}
        </div>
      </div>

      {isUser && (
        <div className="flex-shrink-0">
          <div className="w-8 h-8 bg-gradient-to-br from-primary to-accent-1 rounded-full flex items-center justify-center">
            <User size={18} className="text-white" />
          </div>
        </div>
      )}
    </div>
  );
}
