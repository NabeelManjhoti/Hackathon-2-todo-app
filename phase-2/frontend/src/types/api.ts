/**
 * API Response Types
 *
 * Type definitions for API responses from the FastAPI backend
 */

/**
 * Generic API response wrapper
 */
export interface ApiResponse<T = any> {
  data?: T;
  message?: string;
  error?: string;
}

/**
 * API error response structure
 */
export interface ApiError {
  message: string;
  detail?: string;
  status?: number;
  errors?: Record<string, string[]>;
}

/**
 * Pagination metadata
 */
export interface PaginationMeta {
  page: number;
  limit: number;
  total: number;
  totalPages: number;
}

/**
 * Paginated response wrapper
 */
export interface PaginatedResponse<T> {
  data: T[];
  meta: PaginationMeta;
}

/**
 * HTTP methods
 */
export type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';

/**
 * API request configuration
 */
export interface ApiRequestConfig {
  method?: HttpMethod;
  headers?: Record<string, string>;
  params?: Record<string, any>;
  data?: any;
  timeout?: number;
}
