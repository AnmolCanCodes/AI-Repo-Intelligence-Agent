import { useState, useEffect } from 'react';
import { checkHealth } from './services/api';
import type { ConnectionState, RepositoryState, RepositoryInfo, ChatMessage } from './types';
import RepositoryConnect from './components/RepositoryConnect';
import RepositoryHeader from './components/RepositoryHeader';
import ChatWorkspace from './components/ChatWorkspace';
import LoadingState from './components/LoadingState';

function App() {
  const [connectionState, setConnectionState] = useState<ConnectionState>('checking');
  const [repositoryState, setRepositoryState] = useState<RepositoryState>('not-connected');
  const [repositoryInfo, setRepositoryInfo] = useState<RepositoryInfo | null>(null);
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [error, setError] = useState<string | null>(null);

  // Check backend connection on mount
  useEffect(() => {
    const checkBackend = async () => {
      try {
        await checkHealth();
        setConnectionState('connected');
      } catch (err) {
        console.error('Backend connection failed:', err);
        setConnectionState('disconnected');
      }
    };

    checkBackend();
  }, []);

  const handleRepositoryConnected = (info: RepositoryInfo) => {
    setRepositoryInfo(info);
    setRepositoryState('indexed');
    setChatMessages([]);
    setError(null);
  };

  const handleRepositoryError = (errorMessage: string) => {
    setError(errorMessage);
    setRepositoryState('error');
  };

  const handleClearChat = () => {
    setChatMessages([]);
  };

  const handleNewRepository = () => {
    setRepositoryState('not-connected');
    setRepositoryInfo(null);
    setChatMessages([]);
    setError(null);
  };

  // Render connection error state
  if (connectionState === 'disconnected') {
    return (
      <div className="min-h-screen flex items-center justify-center bg-neutral-50">
        <div className="text-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-red-50 text-red-700 rounded-md mb-4">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            Backend Disconnected
          </div>
          <p className="text-neutral-600">
            Unable to connect to the backend service. Please ensure the FastAPI server is running on{' '}
            <code className="bg-neutral-200 px-1 py-0.5 rounded">http://localhost:8000</code>
          </p>
        </div>
      </div>
    );
  }

  // Render checking state
  if (connectionState === 'checking') {
    return (
      <div className="min-h-screen flex items-center justify-center bg-neutral-50">
        <div className="text-center">
          <div className="inline-block w-8 h-8 border-2 border-neutral-300 border-t-neutral-700 rounded-full animate-spin mb-4" />
          <p className="text-neutral-600">Connecting to backend...</p>
        </div>
      </div>
    );
  }

  // Render repository connection screen
  if (repositoryState === 'not-connected') {
    return (
      <RepositoryConnect
        onConnected={handleRepositoryConnected}
        onError={handleRepositoryError}
        isIndexing={repositoryState === 'indexing'}
      />
    );
  }

  // Render indexing state
  if (repositoryState === 'indexing') {
    return <LoadingState />;
  }

  // Render error state
  if (repositoryState === 'error') {
    return (
      <div className="min-h-screen flex items-center justify-center bg-neutral-50">
        <div className="max-w-md w-full mx-4">
          <div className="bg-white border border-neutral-200 rounded-lg p-6">
            <h2 className="text-lg font-semibold text-neutral-900 mb-2">Error</h2>
            <p className="text-neutral-600 mb-4">{error}</p>
            <button
              onClick={handleNewRepository}
              className="w-full px-4 py-2 bg-neutral-900 text-white rounded-md hover:bg-neutral-800 transition-colors"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Render main chat workspace
  return (
    <div className="min-h-screen bg-neutral-50">
      <RepositoryHeader
        repositoryInfo={repositoryInfo}
        onClearChat={handleClearChat}
        onNewRepository={handleNewRepository}
      />
      <ChatWorkspace
        messages={chatMessages}
        setMessages={setChatMessages}
      />
    </div>
  );
}

export default App;
