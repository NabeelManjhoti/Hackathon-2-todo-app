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
    <div className="space-y-8">
      {/* Incomplete Tasks */}
      {incompleteTasks.length > 0 && (
        <div>
          <div className="mb-4 flex items-center gap-3">
            <div className="h-px flex-1 bg-gradient-to-r from-transparent via-purple-500/50 to-transparent" />
            <h3 className="text-sm font-bold text-transparent bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text uppercase tracking-wider">
              Active Tasks ({incompleteTasks.length})
            </h3>
            <div className="h-px flex-1 bg-gradient-to-r from-transparent via-purple-500/50 to-transparent" />
          </div>
          <div className="space-y-3">
            {incompleteTasks.map((task, index) => (
              <div
                key={task.id}
                className="animate-[fade-in_0.3s_ease-out]"
                style={{ animationDelay: `${index * 0.05}s` }}
              >
                <TaskItem
                  task={task}
                  onToggleComplete={onToggleComplete}
                  onEdit={onEdit}
                  onDelete={onDelete}
                />
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Completed Tasks */}
      {completedTasks.length > 0 && (
        <div>
          <div className="mb-4 flex items-center gap-3">
            <div className="h-px flex-1 bg-gradient-to-r from-transparent via-green-500/50 to-transparent" />
            <h3 className="text-sm font-bold text-transparent bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text uppercase tracking-wider">
              Completed ({completedTasks.length})
            </h3>
            <div className="h-px flex-1 bg-gradient-to-r from-transparent via-green-500/50 to-transparent" />
          </div>
          <div className="space-y-3">
            {completedTasks.map((task, index) => (
              <div
                key={task.id}
                className="animate-[fade-in_0.3s_ease-out]"
                style={{ animationDelay: `${index * 0.05}s` }}
              >
                <TaskItem
                  task={task}
                  onToggleComplete={onToggleComplete}
                  onEdit={onEdit}
                  onDelete={onDelete}
                />
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
