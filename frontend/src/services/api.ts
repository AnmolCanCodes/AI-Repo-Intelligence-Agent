import axios from 'axios';
import type {
  HealthCheckResponse,
  RepoUploadRequest,
  RepoUploadResponse,
  ChatRequest,
  ChatResponse,
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 300000, // 5 minutes for long-running operations
});

// Health check
export async function checkHealth(): Promise<HealthCheckResponse> {
  const response = await api.get<HealthCheckResponse>('/');
  return response.data;
}

// Upload repository
export async function uploadRepository(
  data: RepoUploadRequest
): Promise<RepoUploadResponse> {
  const response = await api.post<RepoUploadResponse>('/api/v1/upload-repo', data);
  return response.data;
}

// Chat with repository
export async function chatWithRepository(
  data: ChatRequest
): Promise<ChatResponse> {
  const response = await api.post<ChatResponse>('/api/v1/chat', data);
  return response.data;
}
