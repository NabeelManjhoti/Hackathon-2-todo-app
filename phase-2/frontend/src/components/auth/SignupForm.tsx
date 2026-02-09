/**
 * SignupForm Component
 *
 * Form for user registration with validation
 */

'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { signup } from '@/src/lib/api/auth';
import { useAuth } from '@/src/lib/hooks/useAuth';
import { signupSchema, SignupFormData } from '@/src/lib/utils/validation';
import { getErrorMessage } from '@/src/lib/utils/errors';
import Button from '@/src/components/ui/Button';
import Input from '@/src/components/ui/Input';
import ErrorMessage from '@/src/components/ui/ErrorMessage';

export default function SignupForm() {
  const router = useRouter();
  const { login } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const [formData, setFormData] = useState<SignupFormData>({
    email: '',
    password: '',
    confirmPassword: '',
  });

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
    const validation = signupSchema.safeParse(formData);

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
      // Call signup API
      const response = await signup({
        email: formData.email,
        password: formData.password,
      });

      // Store token and user
      login(response.access_token, response.user);

      // Redirect to dashboard
      router.push('/dashboard');
    } catch (err) {
      const errorMessage = getErrorMessage(err);

      // Check for duplicate email error
      if (errorMessage.toLowerCase().includes('already exists') ||
          errorMessage.toLowerCase().includes('duplicate')) {
        setError('An account with this email already exists. Please sign in instead.');
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
          <h2 className="text-2xl font-bold text-gray-900">Create Account</h2>
          <p className="mt-2 text-sm text-gray-600">
            Sign up to start managing your tasks
          </p>
        </div>

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
            helperText="At least 8 characters with uppercase, lowercase, and number"
            required
            fullWidth
            autoComplete="new-password"
            disabled={loading}
          />

          <Input
            type="password"
            name="confirmPassword"
            label="Confirm Password"
            placeholder="••••••••"
            value={formData.confirmPassword}
            onChange={handleChange}
            error={fieldErrors.confirmPassword}
            required
            fullWidth
            autoComplete="new-password"
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
            {loading ? 'Creating Account...' : 'Sign Up'}
          </Button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            Already have an account?{' '}
            <Link
              href="/signin"
              className="font-medium text-blue-600 hover:text-blue-500"
            >
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
