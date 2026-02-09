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
    <form onSubmit={handleSubmit} className="space-y-4">
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
          className="block text-sm font-medium text-gray-700 mb-1"
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
          rows={3}
          className="block w-full rounded-lg border border-gray-300 px-4 py-2 text-base transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
        />
        {fieldErrors.description && (
          <p className="mt-1 text-sm text-red-600" role="alert">
            {fieldErrors.description}
          </p>
        )}
      </div>

      <div className="flex gap-3">
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
