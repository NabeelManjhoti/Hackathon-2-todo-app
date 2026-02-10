/**
 * TaskForm Component
 *
 * Form for creating and editing tasks
 */

'use client';

import React, { useState, useEffect } from 'react';
import { Task, CreateTaskRequest } from '@/src/types/task';
import { createTaskSchema, CreateTaskFormData } from '@/src/lib/utils/validation';
import Button from '@/src/components/ui/Button';
import Input from '@/src/components/ui/Input';

export interface TaskFormProps {
  task?: Task;
  onSubmit: (data: CreateTaskRequest) => Promise<void>;
  onCancel?: () => void;
  loading?: boolean;
}

export default function TaskForm({
  task,
  onSubmit,
  onCancel,
  loading = false,
}: TaskFormProps) {
  const [formData, setFormData] = useState<CreateTaskFormData>({
    title: task?.title || '',
    description: task?.description || '',
  });
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});

  // Update form when task prop changes
  useEffect(() => {
    if (task) {
      setFormData({
        title: task.title,
        description: task.description || '',
      });
    }
  }, [task]);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));

    // Clear field error when user starts typing
    if (fieldErrors[name]) {
      setFieldErrors((prev) => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFieldErrors({});

    // Validate form data
    const validation = createTaskSchema.safeParse(formData);

    if (!validation.success) {
      const errors: Record<string, string> = {};
      validation.error.issues.forEach((err) => {
        const field = err.path[0] as string;
        errors[field] = err.message;
      });
      setFieldErrors(errors);
      return;
    }

    await onSubmit({
      title: formData.title,
      description: formData.description || undefined,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      <Input
        type="text"
        name="title"
        label="Title"
        placeholder="Enter task title"
        value={formData.title}
        onChange={handleChange}
        error={fieldErrors.title}
        required
        fullWidth
        disabled={loading}
        autoFocus
      />

      <div className="w-full">
        <label
          htmlFor="description"
          className="block text-sm font-semibold text-gray-300 mb-2"
        >
          Description
        </label>
        <textarea
          id="description"
          name="description"
          placeholder="Enter task description (optional)"
          value={formData.description}
          onChange={handleChange}
          disabled={loading}
          rows={4}
          className="block w-full rounded-lg border border-gray-700 bg-[#1a1a28] px-4 py-3 text-base text-gray-100 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500 focus:ring-offset-2 focus:ring-offset-[#0a0a0f] hover:border-gray-600 disabled:bg-[#12121a] disabled:text-gray-600 disabled:cursor-not-allowed disabled:border-gray-800 placeholder:text-gray-500 focus:shadow-[0_0_20px_rgba(139,92,246,0.3)] resize-none"
        />
        {fieldErrors.description && (
          <p className="mt-2 text-sm text-red-400 flex items-center gap-1.5" role="alert">
            <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
            {fieldErrors.description}
          </p>
        )}
      </div>

      <div className="flex gap-3 pt-2">
        <Button
          type="submit"
          variant="primary"
          loading={loading}
          disabled={loading}
        >
          {task ? 'Update Task' : 'Create Task'}
        </Button>

        {onCancel && (
          <Button
            type="button"
            variant="secondary"
            onClick={onCancel}
            disabled={loading}
          >
            Cancel
          </Button>
        )}
      </div>
    </form>
  );
}
