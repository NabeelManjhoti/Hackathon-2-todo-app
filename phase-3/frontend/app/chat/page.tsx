'use client';

/**
 * Chat Page
 *
 * AI chatbot interface for natural language task management
 */

import { useState, useEffect, useRef } from 'react';
import { useAuth } from '@/src/lib/hooks/useAuth';
import { useRouter } from 'next/navigation';
import {
  sendChatMessage,
  listConversations,
  getConversation,
  ChatResponse,
  MessageItem,
  ToolCall,
  ConversationListItem,
} from '@/src/lib/api/chat';
import Button from '@/src/components/ui/Button';
import Input from '@/src/components/ui/Input';
import LoadingSpinner from '@/src/components/ui/LoadingSpinner';
import ErrorMessage from '@/src/components/ui/ErrorMessage';

interface DisplayMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  tool_calls?: ToolCall[];
  timestamp: Date;
}

export default function ChatPage() {
  const { user, isAuthenticated, loading: authLoading } = useAuth();
  const router = useRouter();
  const [messages, setMessages] = useState<DisplayMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [conversationId, setConversationId] = useState<string | undefined>();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showHistory, setShowHistory] = useState(false);
  const [conversations, setConversations] = useState<ConversationListItem[]>([]);
  const [loadingHistory, setLoadingHistory] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Redirect to signin if not authenticated
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/signin');
    }
  }, [authLoading, isAuthenticated, router]);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Load conversation history
  const loadConversationHistory = async () => {
    if (!user) return;

    setLoadingHistory(true);
    try {
      const response = await listConversations(user.id);
      setConversations(response.conversations);
    } catch (err) {
      console.error('Failed to load conversations:', err);
    } finally {
      setLoadingHistory(false);
    }
  };

  // Load a specific conversation
  const loadConversation = async (convId: string) => {
    if (!user) return;

    setIsLoading(true);
    setError(null);
    try {
      const conversation = await getConversation(user.id, convId);

      // Convert messages to display format
      const displayMessages: DisplayMessage[] = conversation.messages.map((msg) => ({
        id: msg.id,
        role: msg.role as 'user' | 'assistant',
        content: msg.content,
        tool_calls: msg.tool_calls as ToolCall[] | undefined,
        timestamp: new Date(msg.timestamp),
      }));

      setMessages(displayMessages);
      setConversationId(convId);
      setShowHistory(false);
    } catch (err: any) {
      console.error('Failed to load conversation:', err);
      setError('Failed to load conversation. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!inputMessage.trim() || !user) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    setError(null);

    // Add user message to display
    const userDisplayMessage: DisplayMessage = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: userMessage,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userDisplayMessage]);

    setIsLoading(true);

    try {
      // Send message to backend
      const response: ChatResponse = await sendChatMessage(user.id, {
        message: userMessage,
        conversation_id: conversationId,
      });

      // Update conversation ID
      if (!conversationId) {
        setConversationId(response.conversation_id);
      }

      // Add assistant response to display
      const assistantMessage: DisplayMessage = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content: response.response,
        tool_calls: response.tool_calls,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err: any) {
      console.error('Chat error:', err);
      setError(
        err.response?.data?.detail ||
          'Failed to send message. Please try again.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewConversation = () => {
    setMessages([]);
    setConversationId(undefined);
    setError(null);
    setShowHistory(false);
  };

  const toggleHistory = () => {
    if (!showHistory) {
      loadConversationHistory();
    }
    setShowHistory(!showHistory);
  };

  if (authLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <LoadingSpinner size="large" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="flex h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
      {/* Sidebar - Conversation History */}
      {showHistory && (
        <div className="w-80 bg-black/40 backdrop-blur-sm border-r border-purple-500/30 overflow-y-auto">
          <div className="p-4">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-bold text-white">Conversations</h2>
              <button
                onClick={() => setShowHistory(false)}
                className="text-gray-400 hover:text-white"
              >
                ✕
              </button>
            </div>

            {loadingHistory ? (
              <div className="flex justify-center py-8">
                <LoadingSpinner size="small" />
              </div>
            ) : conversations.length === 0 ? (
              <div className="text-center py-8 text-gray-400">
                No conversations yet
              </div>
            ) : (
              <div className="space-y-2">
                {conversations.map((conv) => (
                  <button
                    key={conv.id}
                    onClick={() => loadConversation(conv.id)}
                    className={`w-full text-left p-3 rounded-lg border transition-colors ${
                      conversationId === conv.id
                        ? 'bg-purple-600/30 border-purple-500'
                        : 'bg-purple-500/10 border-purple-500/20 hover:bg-purple-500/20'
                    }`}
                  >
                    <div className="text-sm text-white font-medium mb-1">
                      {conv.last_message?.substring(0, 50) || 'New conversation'}
                      {conv.last_message && conv.last_message.length > 50 && '...'}
                    </div>
                    <div className="text-xs text-gray-400">
                      {conv.message_count} messages • {new Date(conv.updated_at).toLocaleDateString()}
                    </div>
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="bg-black/30 backdrop-blur-sm border-b border-purple-500/30 p-4">
          <div className="max-w-4xl mx-auto flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-white">AI Task Assistant</h1>
              <p className="text-sm text-gray-400">
                Manage your tasks with natural language
              </p>
            </div>
            <div className="flex gap-2">
              <Button
                onClick={toggleHistory}
                variant="secondary"
                size="small"
              >
                {showHistory ? 'Hide' : 'History'}
              </Button>
              <Button
                onClick={handleNewConversation}
                variant="secondary"
                size="small"
              >
                New Chat
              </Button>
              <Button
                onClick={() => router.push('/dashboard')}
                variant="secondary"
                size="small"
              >
                Dashboard
              </Button>
            </div>
          </div>
        </div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-4">
          <div className="max-w-4xl mx-auto space-y-4">
            {messages.length === 0 && (
              <div className="text-center py-12">
                <div className="text-6xl mb-4">🤖</div>
                <h2 className="text-2xl font-bold text-white mb-2">
                  Welcome to AI Task Assistant
                </h2>
                <p className="text-gray-400 mb-6">
                  Try asking me to add, list, update, or complete tasks
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-2xl mx-auto">
                  <button
                    onClick={() => setInputMessage('Add a task to buy groceries')}
                    className="p-3 bg-purple-500/20 hover:bg-purple-500/30 border border-purple-500/30 rounded-lg text-left transition-colors"
                  >
                    <div className="text-white font-medium">Add a task</div>
                    <div className="text-sm text-gray-400">
                      "Add a task to buy groceries"
                    </div>
                  </button>
                  <button
                    onClick={() => setInputMessage('Show me my active tasks')}
                    className="p-3 bg-purple-500/20 hover:bg-purple-500/30 border border-purple-500/30 rounded-lg text-left transition-colors"
                  >
                    <div className="text-white font-medium">List tasks</div>
                    <div className="text-sm text-gray-400">
                      "Show me my active tasks"
                    </div>
                  </button>
                  <button
                    onClick={() =>
                      setInputMessage('Mark my first task as complete')
                    }
                    className="p-3 bg-purple-500/20 hover:bg-purple-500/30 border border-purple-500/30 rounded-lg text-left transition-colors"
                  >
                    <div className="text-white font-medium">Complete task</div>
                    <div className="text-sm text-gray-400">
                      "Mark my first task as complete"
                    </div>
                  </button>
                  <button
                    onClick={() =>
                      setInputMessage('Update task title to "Buy organic groceries"')
                    }
                    className="p-3 bg-purple-500/20 hover:bg-purple-500/30 border border-purple-500/30 rounded-lg text-left transition-colors"
                  >
                    <div className="text-white font-medium">Update task</div>
                    <div className="text-sm text-gray-400">
                      "Update task title to..."
                    </div>
                  </button>
                </div>
              </div>
            )}

            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${
                  message.role === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                <div
                  className={`max-w-[80%] rounded-lg p-4 ${
                    message.role === 'user'
                      ? 'bg-purple-600 text-white'
                      : 'bg-black/40 backdrop-blur-sm border border-purple-500/30 text-white'
                  }`}
                >
                  <div className="whitespace-pre-wrap">{message.content}</div>

                  {/* Tool Calls Display */}
                  {message.tool_calls && message.tool_calls.length > 0 && (
                    <div className="mt-3 space-y-2">
                      {message.tool_calls.map((toolCall, idx) => (
                        <div
                          key={idx}
                          className="bg-purple-900/30 border border-purple-500/20 rounded p-2 text-sm"
                        >
                          <div className="flex items-center gap-2 mb-1">
                            <span className="text-purple-400">🔧</span>
                            <span className="font-medium text-purple-300">
                              {toolCall.tool_name}
                            </span>
                            <span
                              className={`ml-auto px-2 py-0.5 rounded text-xs ${
                                toolCall.status === 'success'
                                  ? 'bg-green-500/20 text-green-300'
                                  : 'bg-red-500/20 text-red-300'
                              }`}
                            >
                              {toolCall.status}
                            </span>
                          </div>
                          <div className="text-gray-400 text-xs">
                            {toolCall.result.message}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}

                  <div className="text-xs text-gray-400 mt-2">
                    {message.timestamp.toLocaleTimeString()}
                  </div>
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-black/40 backdrop-blur-sm border border-purple-500/30 rounded-lg p-4">
                  <LoadingSpinner size="small" />
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Error Display */}
        {error && (
          <div className="px-4 pb-2">
            <div className="max-w-4xl mx-auto">
              <ErrorMessage message={error} />
            </div>
          </div>
        )}

        {/* Input Area */}
        <div className="bg-black/30 backdrop-blur-sm border-t border-purple-500/30 p-4">
          <form
            onSubmit={handleSendMessage}
            className="max-w-4xl mx-auto flex gap-2"
          >
            <Input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Type your message... (e.g., 'Add a task to buy groceries')"
              disabled={isLoading}
              className="flex-1"
            />
            <Button type="submit" disabled={isLoading || !inputMessage.trim()}>
              {isLoading ? 'Sending...' : 'Send'}
            </Button>
          </form>
          <div className="max-w-4xl mx-auto mt-2 text-xs text-gray-500 text-center">
            AI can make mistakes. Verify important information.
          </div>
        </div>
      </div>
    </div>
  );
}
