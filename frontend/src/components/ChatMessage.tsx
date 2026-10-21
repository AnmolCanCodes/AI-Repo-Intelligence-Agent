import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Copy, Check, User, Bot } from 'lucide-react';
import { useState } from 'react';
import type { ChatMessage as ChatMessageType } from '../types';

interface ChatMessageProps {
  message: ChatMessageType;
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const [copiedCode, setCopiedCode] = useState<string | null>(null);

  const handleCopyCode = (code: string) => {
    navigator.clipboard.writeText(code);
    setCopiedCode(code);
    setTimeout(() => setCopiedCode(null), 2000);
  };

  const isUser = message.role === 'user';

  return (
    <div className={`flex gap-3 ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`flex gap-3 max-w-3xl ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
        {/* Avatar */}
        <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
          isUser ? 'bg-neutral-200' : 'bg-neutral-900'
        }`}>
          {isUser ? (
            <User className="w-4 h-4 text-neutral-700" />
          ) : (
            <Bot className="w-4 h-4 text-white" />
          )}
        </div>

        {/* Message content */}
        <div className={`flex-1 ${isUser ? 'text-right' : 'text-left'}`}>
          <div className={`inline-block rounded-lg px-4 py-3 ${
            isUser
              ? 'bg-neutral-900 text-white'
              : 'bg-white border border-neutral-200 text-neutral-900'
          }`}>
            {isUser ? (
              <p className="whitespace-pre-wrap">{message.content}</p>
            ) : (
              <div className="markdown-content">
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  components={{
                    code({ node, inline, className, children, ...props }: any) {
                      const match = /language-(\w+)/.exec(className || '');
                      const language = match ? match[1] : '';
                      const codeString = String(children).replace(/\n$/, '');

                      if (!inline && codeString) {
                        return (
                          <div className="relative group">
                            <pre className="bg-neutral-100 border border-neutral-200 rounded-md overflow-x-auto">
                              <code className={className} {...props}>
                                {children}
                              </code>
                            </pre>
                            <button
                              onClick={() => handleCopyCode(codeString)}
                              className="absolute top-2 right-2 p-1.5 bg-neutral-200 hover:bg-neutral-300 rounded-md opacity-0 group-hover:opacity-100 transition-opacity"
                              title="Copy code"
                            >
                              {copiedCode === codeString ? (
                                <Check className="w-4 h-4 text-neutral-700" />
                              ) : (
                                <Copy className="w-4 h-4 text-neutral-700" />
                              )}
                            </button>
                          </div>
                        );
                      }

                      return (
                        <code className={className} {...props}>
                          {children}
                        </code>
                      );
                    },
                  }}
                >
                  {message.content}
                </ReactMarkdown>
              </div>
            )}
          </div>

          {/* Referenced files */}
          {!isUser && message.referenced_files && message.referenced_files.length > 0 && (
            <div className="mt-2 ml-1">
              <p className="text-xs text-neutral-500 mb-1.5">Referenced files</p>
              <div className="flex flex-wrap gap-1.5">
                {message.referenced_files.map((file, index) => (
                  <code
                    key={index}
                    className="px-2 py-1 bg-neutral-100 text-neutral-700 text-xs rounded-md font-mono"
                  >
                    {file}
                  </code>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
