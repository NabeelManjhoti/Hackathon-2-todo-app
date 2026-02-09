/**
 * SigninForm Component
 *
 * Form for user authentication with validation
 */

'use client';

import React, { useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { signin } from '@/src/lib/api/auth';
import { useAuth } from '@/src/lib/hooks/useAuth';
import { signinSchema, SigninFormData } from '@/src/lib/utils/validation';
import { getErrorMessage } from '@/src/lib/utils/errors';
import Button from '@/src/components/ui/Button';
import Input from '@/src/components/ui/Input';
import ErrorMessage from '@/src/components/ui/ErrorMessage';

export default function SigninForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { login } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const [formData, setFormData] = useState<SigninFormData>({
    email: '',
    password: '',
  });

  // Check if session expired
  const sessionExpired = searchParams.get('expired') === 'true';

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
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
    setError(null);
    setFieldErrors({});

    // Validate form data
    const validation = signinSchema.safeParse(formData);

    if (!validation.success) {
      const errors: Record<string, string> = {};
      validation.error.issues.forEach((err) => {
        const field = err.path[0] as string;
        errors[field] = err.message;
      });
      setFieldErrors(errors);
      return;
    }

    setLoading(true);

    try {
      // Call signin API
      const response = await signin({
        email: formData.email,
        password: formData.password,
      });

      // Store token and user
      login(response.access_token, response.user);

      // Redirect to dashboard
      router.push('/dashboard');
    } catch (err) {
      const errorMessage = getErrorMessage(err);

      // Show generic error for incorrect credentials (don't reveal if email exists)
      if (errorMessage.toLowerCase().includes('invalid') ||
          errorMessage.toLowerCase().includes('incorrect') ||
          errorMessage.toLowerCase().includes('unauthorized')) {
        setError('Invalid email or password. Please try again.');
      } else {
        setError(errorMessage);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-md">
      <div className="rounded-lg border border-gray-200 bg-white p-8 shadow-sm">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Welcome Back</h2>
          <p className="mt-2 text-sm text-gray-600">
            Sign in to access your tasks
          </p>
        </div>

        {sessionExpired && (
          <ErrorMessage
            message="Your session has expired. Please sign in again."
            variant="banner"
            className="mb-6"
          />
        )}

        {error && (
          <ErrorMessage message={error} variant="banner" className="mb-6" />
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            type="email"
            name="email"
            label="Email"
            placeholder="you@example.com"
            value={formData.email}
            onChange={handleChange}
            error={fieldErrors.email}
            required
            fullWidth
            autoComplete="email"
            disabled={loading}
          />

          <Input
            type="password"
            name="password"
            label="Password"
            placeholder="••••••••"
            value={formData.password}
            onChange={handleChange}
            error={fieldErrors.password}
            required
            fullWidth
            autoComplete="current-password"
            disabled={loading}
          />

          <Button
            type="submit"
            variant="primary"
            size="lg"
            fullWidth
            loading={loading}
            disabled={loading}
          >
            {loading ? 'Signing In...' : 'Sign In'}
          </Button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            Don't have an account?{' '}
            <Link
              href="/signup"
              className="font-medium text-blue-600 hover:text-blue-500"
            >
              Sign up
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
