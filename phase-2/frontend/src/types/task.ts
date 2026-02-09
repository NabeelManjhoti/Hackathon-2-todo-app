/**
 * Task Types
 *
 * Type definitions for task management
 */

/**
 * Task object from backend
 */
export interface Task {
  id: string; // UUID from backend
  user_id: string; // UUID from backend
  title: string;
  description: string | null;
  due_date?: string | null; // ISO 8601 datetime string
  completed: boolean; // Match backend field name
  created_at: string;
  updated_at: string;
}

/**
 * Create task request payload
 */
export interface CreateTaskRequest {
  title: string;
  description?: string;
  due_date?: string; // ISO 8601 datetime string
}

/**
 * Update task request payload
 */
export interface UpdateTaskRequest {
  title?: string;
  description?: string;
  due_date?: string; // ISO 8601 datetime string
  completed?: boolean; // Match backend field name
}

/**
 * Delete task response (204 No Content - no body)
 */
export interface DeleteTaskResponse {
  // Backend returns 204 No Content with no response body
}

/**
 * Task filter options
 */
export interface TaskFilters {
  completed?: boolean;
  search?: string;
}

/**
 * Task sort options
 */
export type TaskSortBy = 'created_at' | 'updated_at' | 'title';
export type TaskSortOrder = 'asc' | 'desc';

export interface TaskSort {
  by: TaskSortBy;
  order: TaskSortOrder;
}
