/**
 * Task Types
 *
 * Type definitions for task management
 */

/**
 * Task object from backend
 */
export interface Task {
  id: number;
  user_id: number;
  title: string;
  description: string | null;
  is_completed: boolean;
  created_at: string;
  updated_at: string;
}

/**
 * Create task request payload
 */
export interface CreateTaskRequest {
  title: string;
  description?: string;
}

/**
 * Update task request payload
 */
export interface UpdateTaskRequest {
  title?: string;
  description?: string;
  is_completed?: boolean;
}

/**
 * Delete task response
 */
export interface DeleteTaskResponse {
  message: string;
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
