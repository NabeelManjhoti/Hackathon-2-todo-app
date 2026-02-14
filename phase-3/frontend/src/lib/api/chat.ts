/**
 * Chat API Client
 *
 * API functions for AI chatbot interactions
 */

import apiClient from './client';

export interface ChatMessage {
  message: string;
  conversation_id?: string;
}

export interface ToolCall {
  tool_name: string;
  parameters: Record<string, any>;
  result: {
    status: 'success' | 'error';
    message: string;
    data: any;
  };
  status: string;
}

export interface ChatResponse {
  conversation_id: string;
  response: string;
  tool_calls?: ToolCall[];
}

export interface ConversationListItem {
  id: string;
  created_at: string;
  updated_at: string;
  message_count: number;
  last_message?: string;
}

export interface ConversationListResponse {
  conversations: ConversationListItem[];
  total: number;
}

export interface MessageItem {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  tool_calls?: Record<string, any>;
  timestamp: string;
}

export interface ConversationDetailResponse {
  id: string;
  created_at: string;
  updated_at: string;
  messages: MessageItem[];
}

/**
 * Send a message to the AI chatbot
 */
export async function sendChatMessage(
  userId: string,
  message: ChatMessage
): Promise<ChatResponse> {
  const response = await apiClient.post<ChatResponse>(
    `/api/${userId}/chat`,
    message
  );
  return response.data;
}

/**
 * List all conversations for the user
 */
export async function listConversations(
  userId: string,
  limit: number = 50,
  offset: number = 0
): Promise<ConversationListResponse> {
  const response = await apiClient.get<ConversationListResponse>(
    `/api/${userId}/conversations`,
    {
      params: { limit, offset },
    }
  );
  return response.data;
}

/**
 * Get a specific conversation with all messages
 */
export async function getConversation(
  userId: string,
  conversationId: string
): Promise<ConversationDetailResponse> {
  const response = await apiClient.get<ConversationDetailResponse>(
    `/api/${userId}/conversations/${conversationId}`
  );
  return response.data;
}

/**
 * Delete a conversation
 */
export async function deleteConversation(
  userId: string,
  conversationId: string
): Promise<void> {
  await apiClient.delete(`/api/${userId}/conversations/${conversationId}`);
}
