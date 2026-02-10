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
  const handleDeleteTask = async (id: string) => {
    const result = await removeTask(id);

    if (result) {
      setSuccessMessage('Task deleted successfully!');
      setTimeout(() => setSuccessMessage(null), 3000);
    }
  };

  // Handle toggle complete
  const handleToggleComplete = async (id: string) => {
    await toggleComplete(id);
  };

  // Handle edit button click
  const handleEditClick = (task: Task) => {
    setEditingTask(task);
    setShowCreateForm(false);
  };

  return (
    <ProtectedRoute>
      <div className="flex min-h-screen flex-col">
        <Header />

        <main className="flex-1">
          <div className="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:px-8">
            {/* Page Header */}
            <div className="mb-10">
              <h1 className="text-4xl font-bold bg-gradient-to-r from-cyan-400 via-purple-400 to-fuchsia-400 bg-clip-text text-transparent animate-[fade-in_0.6s_ease-out]">
                My Tasks
              </h1>
              <p className="mt-3 text-gray-400 text-lg animate-[fade-in_0.6s_ease-out_0.1s] opacity-0 [animation-fill-mode:forwards]">
                Manage your tasks and stay organized
              </p>
            </div>

            {/* Success Message */}
            {successMessage && (
              <SuccessMessage
                message={successMessage}
                variant="banner"
                onDismiss={() => setSuccessMessage(null)}
                className="mb-6 animate-[slide-down_0.3s_ease-out]"
              />
            )}

            {/* Error Message */}
            {error && (
              <ErrorMessage
                message={error}
                variant="banner"
                className="mb-6 animate-[slide-down_0.3s_ease-out]"
              />
            )}

            {/* Create Task Button */}
            {!showCreateForm && !editingTask && (
              <div className="mb-8 animate-[fade-in_0.6s_ease-out_0.2s] opacity-0 [animation-fill-mode:forwards]">
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
              <div className="mb-8 rounded-xl border border-white/10 bg-gradient-to-br from-[#1a1a28]/90 to-[#12121a]/90 backdrop-blur-sm p-6 shadow-[0_0_30px_rgba(139,92,246,0.2)] animate-[scale-in_0.3s_ease-out]">
                <h2 className="mb-5 text-xl font-bold text-gray-100">
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
              <div className="mb-8 rounded-xl border border-white/10 bg-gradient-to-br from-[#1a1a28]/90 to-[#12121a]/90 backdrop-blur-sm p-6 shadow-[0_0_30px_rgba(139,92,246,0.2)] animate-[scale-in_0.3s_ease-out]">
                <h2 className="mb-5 text-xl font-bold text-gray-100">
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
            <div className="animate-[fade-in_0.6s_ease-out_0.3s] opacity-0 [animation-fill-mode:forwards]">
              <TaskList
                tasks={tasks}
                loading={loading}
                onToggleComplete={handleToggleComplete}
                onEdit={handleEditClick}
                onDelete={handleDeleteTask}
                onCreateTask={() => setShowCreateForm(true)}
              />
            </div>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}
