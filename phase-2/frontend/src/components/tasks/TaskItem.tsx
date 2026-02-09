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
  onToggleComplete: (id: number, isCompleted: boolean) => Promise<void>;
  onEdit: (task: Task) => void;
  onDelete: (id: number) => Promise<void>;
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
    await onToggleComplete(task.id, !task.is_completed);
  };

  const handleDelete = async () => {
    setIsDeleting(true);
    await onDelete(task.id);
    setIsDeleting(false);
    setShowDeleteConfirm(false);
  };

  return (
    <div className="group rounded-lg border border-gray-200 bg-white p-4 shadow-sm transition-shadow hover:shadow-md">
      <div className="flex items-start gap-3">
        {/* Checkbox */}
        <button
          onClick={handleToggleComplete}
          className="mt-1 flex-shrink-0 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 rounded"
          aria-label={task.is_completed ? 'Mark as incomplete' : 'Mark as complete'}
        >
          <div
            className={`h-5 w-5 rounded border-2 flex items-center justify-center transition-colors ${
              task.is_completed
                ? 'bg-blue-600 border-blue-600'
                : 'border-gray-300 hover:border-blue-500'
            }`}
          >
            {task.is_completed && (
              <svg
                className="h-3 w-3 text-white"
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
            className={`text-base font-medium ${
              task.is_completed
                ? 'text-gray-500 line-through'
                : 'text-gray-900'
            }`}
          >
            {task.title}
          </h3>

          {task.description && (
            <p
              className={`mt-1 text-sm ${
                task.is_completed ? 'text-gray-400' : 'text-gray-600'
              }`}
            >
              {task.description}
            </p>
          )}

          <p className="mt-2 text-xs text-gray-500">
            Created {new Date(task.created_at).toLocaleDateString()}
          </p>
        </div>

        {/* Actions */}
        <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
          <button
            onClick={() => onEdit(task)}
            className="rounded p-1.5 text-gray-600 hover:bg-gray-100 hover:text-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
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
            className="rounded p-1.5 text-gray-600 hover:bg-red-50 hover:text-red-600 focus:outline-none focus:ring-2 focus:ring-red-500"
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
        <div className="mt-4 rounded-lg bg-red-50 border border-red-200 p-4">
          <p className="text-sm text-red-800 mb-3">
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
