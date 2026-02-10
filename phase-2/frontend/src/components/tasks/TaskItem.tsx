/**
 * TaskItem Component
 *
 * Individual task item with edit/delete/complete actions
 */

'use client';

import React, { useState } from 'react';
import { Task } from '@/src/types/task';
import Button from '@/src/components/ui/Button';

export interface TaskItemProps {
  task: Task;
  onToggleComplete: (id: string) => Promise<void>;
  onEdit: (task: Task) => void;
  onDelete: (id: string) => Promise<void>;
}

export default function TaskItem({
  task,
  onToggleComplete,
  onEdit,
  onDelete,
}: TaskItemProps) {
  const [isDeleting, setIsDeleting] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  const handleToggleComplete = async () => {
    await onToggleComplete(task.id);
  };

  const handleDelete = async () => {
    setIsDeleting(true);
    await onDelete(task.id);
    setIsDeleting(false);
    setShowDeleteConfirm(false);
  };

  return (
    <div className="group rounded-xl border border-white/10 bg-gradient-to-br from-[#1a1a28]/90 to-[#12121a]/90 backdrop-blur-sm p-5 shadow-lg transition-all duration-300 hover:shadow-[0_0_30px_rgba(139,92,246,0.3)] hover:border-purple-500/50 hover:scale-[1.01]">
      <div className="flex items-start gap-4">
        {/* Checkbox */}
        <button
          onClick={handleToggleComplete}
          className="mt-1 flex-shrink-0 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-[#0a0a0f] rounded transition-transform duration-200 hover:scale-110"
          aria-label={task.completed ? 'Mark as incomplete' : 'Mark as complete'}
        >
          <div
            className={`h-6 w-6 rounded-lg border-2 flex items-center justify-center transition-all duration-300 ${
              task.completed
                ? 'bg-gradient-to-br from-purple-600 to-fuchsia-600 border-purple-500 shadow-[0_0_15px_rgba(139,92,246,0.6)]'
                : 'border-gray-600 hover:border-purple-500 hover:shadow-[0_0_10px_rgba(139,92,246,0.4)]'
            }`}
          >
            {task.completed && (
              <svg
                className="h-4 w-4 text-white animate-[scale-in_0.2s_ease-out]"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={3}
                  d="M5 13l4 4L19 7"
                />
              </svg>
            )}
          </div>
        </button>

        {/* Task Content */}
        <div className="flex-1 min-w-0">
          <h3
            className={`text-base font-semibold transition-all duration-300 ${
              task.completed
                ? 'text-gray-500 line-through'
                : 'text-gray-100 group-hover:text-white'
            }`}
          >
            {task.title}
          </h3>

          {task.description && (
            <p
              className={`mt-2 text-sm leading-relaxed transition-colors duration-300 ${
                task.completed ? 'text-gray-600' : 'text-gray-400 group-hover:text-gray-300'
              }`}
            >
              {task.description}
            </p>
          )}

          <div className="mt-3 flex items-center gap-2">
            <div className="flex items-center gap-1.5 text-xs text-gray-500">
              <svg className="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>{new Date(task.created_at).toLocaleDateString()}</span>
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-all duration-300">
          <button
            onClick={() => onEdit(task)}
            className="rounded-lg p-2 text-gray-400 hover:bg-purple-500/20 hover:text-purple-400 focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all duration-200 hover:scale-110"
            aria-label="Edit task"
          >
            <svg
              className="h-5 w-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
              />
            </svg>
          </button>

          <button
            onClick={() => setShowDeleteConfirm(true)}
            className="rounded-lg p-2 text-gray-400 hover:bg-red-500/20 hover:text-red-400 focus:outline-none focus:ring-2 focus:ring-red-500 transition-all duration-200 hover:scale-110"
            aria-label="Delete task"
          >
            <svg
              className="h-5 w-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
              />
            </svg>
          </button>
        </div>
      </div>

      {/* Delete Confirmation */}
      {showDeleteConfirm && (
        <div className="mt-4 rounded-lg bg-red-500/10 border border-red-500/30 p-4 backdrop-blur-sm animate-[fade-in_0.2s_ease-out]">
          <p className="text-sm text-red-300 mb-3">
            Are you sure you want to delete this task? This action cannot be undone.
          </p>
          <div className="flex gap-2">
            <Button
              variant="danger"
              size="sm"
              onClick={handleDelete}
              loading={isDeleting}
              disabled={isDeleting}
            >
              Delete
            </Button>
            <Button
              variant="secondary"
              size="sm"
              onClick={() => setShowDeleteConfirm(false)}
              disabled={isDeleting}
            >
              Cancel
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}
