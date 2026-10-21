import { Github, RotateCcw, Plus } from 'lucide-react';
import type { RepositoryInfo } from '../types';

interface RepositoryHeaderProps {
  repositoryInfo: RepositoryInfo | null;
  onClearChat: () => void;
  onNewRepository: () => void;
}

export default function RepositoryHeader({ repositoryInfo, onClearChat, onNewRepository }: RepositoryHeaderProps) {
  return (
    <header className="bg-white border-b border-neutral-200">
      <div className="max-w-4xl mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex items-center justify-center w-10 h-10 bg-neutral-900 rounded-md">
              <Github className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-lg font-semibold text-neutral-900">Repo Intelligence</h1>
              {repositoryInfo && (
                <div className="flex items-center gap-2 text-sm text-neutral-600">
                  <span className="font-mono">{repositoryInfo.repo_name}</span>
                  <span className="text-neutral-300">•</span>
                  <span>{repositoryInfo.files_processed} files</span>
                  <span className="text-neutral-300">•</span>
                  <span>{repositoryInfo.chunks_created} chunks</span>
                </div>
              )}
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={onClearChat}
              className="flex items-center gap-2 px-3 py-1.5 text-sm text-neutral-600 hover:text-neutral-900 hover:bg-neutral-100 rounded-md transition-colors"
              title="Clear conversation"
            >
              <RotateCcw className="w-4 h-4" />
              <span className="hidden sm:inline">Clear</span>
            </button>
            <button
              onClick={onNewRepository}
              className="flex items-center gap-2 px-3 py-1.5 text-sm text-neutral-600 hover:text-neutral-900 hover:bg-neutral-100 rounded-md transition-colors"
              title="Connect new repository"
            >
              <Plus className="w-4 h-4" />
              <span className="hidden sm:inline">New Repo</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
