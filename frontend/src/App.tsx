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
        console.warn('Backend connection check failed. Frontend will still open for local use.', err);
        setConnectionState('connected');
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

  const handleRepositoryIndexing = () => {
    setRepositoryState('indexing');
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
        onIndexing={handleRepositoryIndexing}
        onError={handleRepositoryError}
        isIndexing={false}
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
