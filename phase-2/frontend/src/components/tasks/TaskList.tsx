/**
 * TaskList Component
 *
 * List of tasks with filtering and sorting
 */

'use client';

import React from 'react';
import { Task } from '@/src/types/task';
import TaskItem from './TaskItem';
import EmptyState from './EmptyState';
import TaskListSkeleton from './TaskListSkeleton';

export interface TaskListProps {
  tasks: Task[];
  loading?: boolean;
  onToggleComplete: (id: string) => Promise<void>;
  onEdit: (task: Task) => void;
  onDelete: (id: string) => Promise<void>;
  onCreateTask?: () => void;
}

export default function TaskList({
  tasks,
  loading = false,
  onToggleComplete,
  onEdit,
  onDelete,
  onCreateTask,
}: TaskListProps) {
  // Show loading state
  if (loading) {
    return <TaskListSkeleton />;
  }

  // Show empty state if no tasks
  if (tasks.length === 0) {
    return <EmptyState onCreateTask={onCreateTask} />;
  }

  // Separate completed and incomplete tasks
  const incompleteTasks = tasks.filter((task) => !task.completed);
  const completedTasks = tasks.filter((task) => task.completed);

  return (
    <div className="space-y-6">
      {/* Incomplete Tasks */}
      {incompleteTasks.length > 0 && (
        <div>
          <h3 className="mb-3 text-sm font-semibold text-gray-700 uppercase tracking-wide">
            Active Tasks ({incompleteTasks.length})
          </h3>
          <div className="space-y-3">
            {incompleteTasks.map((task) => (
              <TaskItem
                key={task.id}
                task={task}
                onToggleComplete={onToggleComplete}
                onEdit={onEdit}
                onDelete={onDelete}
              />
            ))}
          </div>
        </div>
      )}

      {/* Completed Tasks */}
      {completedTasks.length > 0 && (
        <div>
          <h3 className="mb-3 text-sm font-semibold text-gray-700 uppercase tracking-wide">
            Completed ({completedTasks.length})
          </h3>
          <div className="space-y-3">
            {completedTasks.map((task) => (
              <TaskItem
                key={task.id}
                task={task}
                onToggleComplete={onToggleComplete}
                onEdit={onEdit}
                onDelete={onDelete}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
