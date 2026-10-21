import { useState, useRef, useEffect } from 'react';
import { Send } from 'lucide-react';
import { chatWithRepository } from '../services/api';
import type { ChatMessage as ChatMessageType } from '../types';

interface ChatInputProps {
  messages: ChatMessageType[];
  setMessages: (messages: ChatMessageType[]) => void;
}

export default function ChatInput({ messages, setMessages }: ChatInputProps) {
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
    }
  }, [input]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!input.trim() || isLoading) return;

    const userMessage: ChatMessageType = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim(),
      timestamp: Date.now(),
    };

    setMessages([...messages, userMessage]);
    setInput('');
    setIsLoading(true);

    // Prepare chat history for API
    const chatHistory = messages
      .slice(-10) // Keep last 10 messages for context
      .map((msg) => ({
        role: msg.role,
        content: msg.content,
      }));

    try {
      const response = await chatWithRepository({
        question: userMessage.content,
        chat_history: chatHistory,
      });

      const assistantMessage: ChatMessageType = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.answer,
        referenced_files: response.referenced_files,
        timestamp: Date.now(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error: any) {
      console.error('Chat error:', error);
      const errorMessage: ChatMessageType = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: error.response?.data?.detail || 'Failed to get a response. Please try again.',
        timestamp: Date.now(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
      <div className="flex gap-3">
        <div className="flex-1 relative">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask anything about this codebase..."
            disabled={isLoading}
            rows={1}
            className="w-full px-4 py-3 pr-12 border border-neutral-300 rounded-md resize-none focus:outline-none focus:ring-2 focus:ring-neutral-900 focus:border-transparent disabled:bg-neutral-100 disabled:cursor-not-allowed min-h-[48px] max-h-[200px]"
            style={{ height: 'auto' }}
          />
        </div>
        <button
          type="submit"
          disabled={!input.trim() || isLoading}
          className="flex items-center justify-center w-12 h-12 bg-neutral-900 text-white rounded-md hover:bg-neutral-800 transition-colors disabled:bg-neutral-300 disabled:cursor-not-allowed flex-shrink-0"
          title="Send message"
        >
          {isLoading ? (
            <div className="w-5 h-5 border-2 border-neutral-400 border-t-white rounded-full animate-spin" />
          ) : (
            <Send className="w-5 h-5" />
          )}
        </button>
      </div>
      <p className="text-xs text-neutral-500 mt-2">
        Press <kbd className="px-1.5 py-0.5 bg-neutral-200 rounded text-neutral-700">Enter</kbd> to send,{' '}
        <kbd className="px-1.5 py-0.5 bg-neutral-200 rounded text-neutral-700">Shift + Enter</kbd> for new line
      </p>
    </form>
  );
}
