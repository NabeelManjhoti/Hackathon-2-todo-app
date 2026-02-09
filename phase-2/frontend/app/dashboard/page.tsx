/**
 * Dashboard Page
 *
 * Main task management dashboard for authenticated users
 */

'use client';

import React, { useState } from 'react';
import ProtectedRoute from '@/src/components/auth/ProtectedRoute';
import Header from '@/src/components/layout/Header';
import TaskList from '@/src/components/tasks/TaskList';
import TaskForm from '@/src/components/tasks/TaskForm';
import { useTasks } from '@/src/lib/hooks/useTasks';
import { Task, CreateTaskRequest } from '@/src/types/task';
import ErrorMessage, { SuccessMessage } from '@/src/components/ui/ErrorMessage';
import Button from '@/src/components/ui/Button';

export default function DashboardPage() {
  const {
    tasks,
    loading,
    error,
    addTask,
    editTask,
    removeTask,
    toggleComplete,
  } = useTasks();

  const [showCreateForm, setShowCreateForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [formLoading, setFormLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  // Handle create task
  const handleCreateTask = async (data: CreateTaskRequest) => {
    setFormLoading(true);

    const result = await addTask(data);

    if (result) {
      setShowCreateForm(false);
      setSuccessMessage('Task created successfully!');
      setTimeout(() => setSuccessMessage(null), 3000);
    }

    setFormLoading(false);
  };

  // Handle edit task
  const handleEditTask = async (data: CreateTaskRequest) => {
    if (!editingTask) return;

    setFormLoading(true);

    const result = await editTask(editingTask.id, data);

    if (result) {
      setEditingTask(null);
      setSuccessMessage('Task updated successfully!');
      setTimeout(() => setSuccessMessage(null), 3000);
    }

    setFormLoading(false);
  };

  // Handle delete task
  const handleDeleteTask = async (id: number) => {
    const result = await removeTask(id);

    if (result) {
      setSuccessMessage('Task deleted successfully!');
      setTimeout(() => setSuccessMessage(null), 3000);
    }
  };

  // Handle toggle complete
  const handleToggleComplete = async (id: number, isCompleted: boolean) => {
    await toggleComplete(id, isCompleted);
  };

  // Handle edit button click
  const handleEditClick = (task: Task) => {
    setEditingTask(task);
    setShowCreateForm(false);
  };

  return (
    <ProtectedRoute>
      <div className="flex min-h-screen flex-col bg-gray-50">
        <Header />

        <main className="flex-1">
          <div className="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:px-8">
            {/* Page Header */}
            <div className="mb-8">
              <h1 className="text-3xl font-bold text-gray-900">My Tasks</h1>
              <p className="mt-2 text-gray-600">
                Manage your tasks and stay organized
              </p>
            </div>

            {/* Success Message */}
            {successMessage && (
              <SuccessMessage
                message={successMessage}
                variant="banner"
                onDismiss={() => setSuccessMessage(null)}
                className="mb-6"
              />
            )}

            {/* Error Message */}
            {error && (
              <ErrorMessage
                message={error}
                variant="banner"
                className="mb-6"
              />
            )}

            {/* Create Task Button */}
            {!showCreateForm && !editingTask && (
              <div className="mb-6">
                <Button
                  variant="primary"
                  size="md"
                  onClick={() => setShowCreateForm(true)}
                >
                  <svg
                    className="h-5 w-5 mr-2"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    aria-hidden="true"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M12 4v16m8-8H4"
                    />
                  </svg>
                  Create Task
                </Button>
              </div>
            )}

            {/* Create Task Form */}
            {showCreateForm && (
              <div className="mb-6 rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
                <h2 className="mb-4 text-lg font-semibold text-gray-900">
                  Create New Task
                </h2>
                <TaskForm
                  onSubmit={handleCreateTask}
                  onCancel={() => setShowCreateForm(false)}
                  loading={formLoading}
                />
              </div>
            )}

            {/* Edit Task Form */}
            {editingTask && (
              <div className="mb-6 rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
                <h2 className="mb-4 text-lg font-semibold text-gray-900">
                  Edit Task
                </h2>
                <TaskForm
                  task={editingTask}
                  onSubmit={handleEditTask}
                  onCancel={() => setEditingTask(null)}
                  loading={formLoading}
                />
              </div>
            )}

            {/* Task List */}
            <TaskList
              tasks={tasks}
              loading={loading}
              onToggleComplete={handleToggleComplete}
              onEdit={handleEditClick}
              onDelete={handleDeleteTask}
              onCreateTask={() => setShowCreateForm(true)}
            />
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}
