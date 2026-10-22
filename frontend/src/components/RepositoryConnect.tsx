import { useState } from 'react';
import { uploadRepository } from '../services/api';
import type { RepositoryInfo } from '../types';

interface RepositoryConnectProps {
  onConnected: (info: RepositoryInfo) => void;
  onIndexing: () => void;
  onError: (error: string) => void;
  isIndexing: boolean;
}

export default function RepositoryConnect({ onConnected, onIndexing, onError }: RepositoryConnectProps) {
  const [repoUrl, setRepoUrl] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!repoUrl.trim()) {
      setError('Please enter a repository URL');
      return;
    }

    // Basic URL validation
    const githubUrlPattern = /^https?:\/\/(www\.)?github\.com\/[^\/]+\/[^\/]+/;
    if (!githubUrlPattern.test(repoUrl)) {
      setError('Please enter a valid GitHub repository URL');
      return;
    }

    setIsSubmitting(true);
    setError(null);
    onIndexing();

    try {
      const response = await uploadRepository({ repo_url: repoUrl.trim() });
      onConnected({
        repo_name: response.repo_name,
        files_processed: response.files_processed,
        chunks_created: response.chunks_created,
      });
    } catch (err: unknown) {
      const backendUnavailableMessage = 'backend is not running, clone the repo to use it on computer.';
      const networkError = (err as any)?.code === 'ERR_NETWORK' || !(err as any)?.response;
      const errorMessage = networkError
        ? backendUnavailableMessage
        : (err as any)?.response?.data?.detail || (err as any)?.message || 'Failed to process repository';

      setError(errorMessage);
      onError(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-neutral-50 p-4">
      <div className="max-w-lg w-full">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-neutral-900 rounded-lg mb-4">
            <img src="/github_logo.svg" alt="GitHub" className="w-8 h-8" />
          </div>
          <h1 className="text-3xl font-semibold text-neutral-900 mb-2">Repo Intelligence</h1>
          <p className="text-neutral-600">
            Connect a GitHub repository to explore and understand its codebase using natural language queries
          </p>
        </div>

        <form onSubmit={handleSubmit} className="bg-white border border-neutral-200 rounded-lg p-6">
          <div className="mb-4">
            <label htmlFor="repo-url" className="block text-sm font-medium text-neutral-700 mb-2">
              GitHub Repository URL
            </label>
            <input
              id="repo-url"
              type="url"
              value={repoUrl}
              onChange={(e) => setRepoUrl(e.target.value)}
              placeholder="https://github.com/username/repository"
              disabled={isSubmitting}
              className="w-full px-4 py-2.5 border border-neutral-300 rounded-md font-mono text-sm focus:outline-none focus:ring-2 focus:ring-neutral-900 focus:border-transparent disabled:bg-neutral-100 disabled:cursor-not-allowed"
            />
          </div>

          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md">
              <p className="text-sm text-red-700">{error}</p>
            </div>
          )}

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full px-4 py-2.5 bg-neutral-900 text-white rounded-md hover:bg-neutral-800 transition-colors disabled:bg-neutral-400 disabled:cursor-not-allowed font-medium"
          >
            {isSubmitting ? 'Processing...' : 'Connect Repository'}
          </button>

          <div className="mt-4 pt-4 border-t border-neutral-200">
            <p className="text-xs text-neutral-500">
              Public repositories can be indexed without authentication. Private repositories require a GitHub token configured in the backend.
            </p>
          </div>
        </form>

        <div className="mt-6 text-center">
          <p className="text-sm text-neutral-500">
            Backend status: <span className="text-green-600 font-medium">Connected</span>
          </p>
        </div>
      </div>
    </div>
  );
}
