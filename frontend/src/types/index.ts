// API Response Types matching backend schemas

export interface HealthCheckResponse {
  status: string;
  message: string;
}

export interface RepoUploadRequest {
  repo_url: string;
}

export interface RepoUploadResponse {
  message: string;
  repo_name: string;
  files_processed: number;
  chunks_created: number;
}

export interface MessageTurn {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatRequest {
  question: string;
  chat_history: MessageTurn[];
}

export interface ChatResponse {
  question: string;
  answer: string;
  referenced_files: string[];
}

// Frontend State Types

export interface ChatMessage extends MessageTurn {
  id: string;
  referenced_files?: string[];
  timestamp: number;
}

export type ConnectionState = 'disconnected' | 'checking' | 'connected';

export type RepositoryState =
  | 'not-connected'
  | 'indexing'
  | 'indexed'
  | 'error';

export interface RepositoryInfo {
  repo_name: string;
  files_processed: number;
  chunks_created: number;
}
