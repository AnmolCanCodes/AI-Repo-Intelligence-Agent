import { useRef, useEffect, type Dispatch, type SetStateAction } from 'react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import type { ChatMessage as ChatMessageType } from '../types';

interface ChatWorkspaceProps {
  messages: ChatMessageType[];
  setMessages: Dispatch<SetStateAction<ChatMessageType[]>>;
}

export default function ChatWorkspace({ messages, setMessages }: ChatWorkspaceProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const exampleQuestions = [
    'Where is authentication implemented?',
    'Explain the application architecture',
    'How does the retrieval pipeline work?',
    'Where is the database or vector store initialized?',
  ];

  return (
    <div className="max-w-4xl mx-auto flex flex-col h-[calc(100vh-73px)]">
      <div className="flex-1 overflow-y-auto px-4 py-6">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full">
            <div className="text-center max-w-md">
              <h2 className="text-xl font-semibold text-neutral-900 mb-3">
                Ask anything about this codebase
              </h2>
              <p className="text-neutral-600 mb-6">
                Get insights about architecture, implementation details, and how different components work together
              </p>
              <div className="space-y-2">
                <p className="text-sm text-neutral-500 mb-3">Try asking:</p>
                {exampleQuestions.map((question, index) => (
                  <button
                    key={index}
                    onClick={() => {
                      setMessages([
                        {
                          id: Date.now().toString(),
                          role: 'user',
                          content: question,
                          timestamp: Date.now(),
                        },
                      ]);
                    }}
                    className="block w-full text-left px-4 py-2.5 text-sm text-neutral-700 bg-white border border-neutral-200 rounded-md hover:border-neutral-300 hover:bg-neutral-50 transition-colors"
                  >
                    {question}
                  </button>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            {messages.map((message) => (
              <ChatMessage key={message.id} message={message} />
            ))}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      <div className="border-t border-neutral-200 bg-white px-4 py-4">
        <ChatInput messages={messages} setMessages={setMessages} />
      </div>
    </div>
  );
}
