/**
 * Landing Page
 *
 * Home page with authentication redirect logic
 */

'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/src/lib/hooks/useAuth';
import { testApiConnection } from '@/src/lib/api/client';
import LoadingSpinner from '@/src/components/ui/LoadingSpinner';
import ErrorMessage from '@/src/components/ui/ErrorMessage';
import Button from '@/src/components/ui/Button';

export default function Home() {
  const router = useRouter();
  const { isAuthenticated, loading: authLoading } = useAuth();
  const [apiStatus, setApiStatus] = useState<{
    checking: boolean;
    connected: boolean;
    message: string;
  }>({
    checking: true,
    connected: false,
    message: '',
  });

  // Check API connectivity on mount
  useEffect(() => {
    async function checkApi() {
      const result = await testApiConnection();
      setApiStatus({
        checking: false,
        connected: result.success,
        message: result.message,
      });
    }

    checkApi();
  }, []);

  // Redirect authenticated users to dashboard
  useEffect(() => {
    if (!authLoading && isAuthenticated) {
      router.push('/dashboard');
    }
  }, [isAuthenticated, authLoading, router]);

  // Show loading while checking auth
  if (authLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <LoadingSpinner size="lg" label="Loading application..." />
      </div>
    );
  }

  // Don't render landing page if authenticated (will redirect)
  if (isAuthenticated) {
    return null;
  }

  return (
    <div className="flex min-h-screen flex-col bg-gray-50">
      {/* Header */}
      <header className="border-b border-gray-200 bg-white">
        <div className="mx-auto max-w-7xl px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-gray-900">Todo App</h1>
            <div className="flex gap-3">
              <Link href="/signin">
                <Button variant="ghost" size="md">
                  Sign In
                </Button>
              </Link>
              <Link href="/signup">
                <Button variant="primary" size="md">
                  Sign Up
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1">
        <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
          {/* Hero Section */}
          <div className="text-center">
            <h2 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl md:text-6xl">
              Manage Your Tasks
              <span className="block text-blue-600">Efficiently</span>
            </h2>
            <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-600">
              A modern, full-stack todo application that helps you organize your tasks,
              track your progress, and boost your productivity.
            </p>

            {/* CTA Buttons */}
            <div className="mt-10 flex justify-center gap-4">
              <Link href="/signup">
                <Button variant="primary" size="lg">
                  Get Started
                </Button>
              </Link>
              <Link href="/signin">
                <Button variant="secondary" size="lg">
                  Sign In
                </Button>
              </Link>
            </div>

            {/* API Status */}
            <div className="mt-8">
              {apiStatus.checking ? (
                <div className="flex items-center justify-center gap-2 text-sm text-gray-500">
                  <LoadingSpinner size="sm" />
                  <span>Checking API connection...</span>
                </div>
              ) : apiStatus.connected ? (
                <div className="flex items-center justify-center gap-2 text-sm text-green-600">
                  <svg
                    className="h-5 w-5"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                    aria-hidden="true"
                  >
                    <path
                      fillRule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z"
                      clipRule="evenodd"
                    />
                  </svg>
                  <span>API Connected</span>
                </div>
              ) : (
                <ErrorMessage
                  message={`API Connection Failed: ${apiStatus.message}`}
                  variant="inline"
                  className="text-center"
                />
              )}
            </div>
          </div>

          {/* Features Section */}
          <div className="mt-24">
            <div className="grid gap-8 md:grid-cols-3">
              {/* Feature 1 */}
              <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-blue-100">
                  <svg
                    className="h-6 w-6 text-blue-600"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    aria-hidden="true"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                    />
                  </svg>
                </div>
                <h3 className="mt-4 text-lg font-semibold text-gray-900">
                  Create & Organize
                </h3>
                <p className="mt-2 text-gray-600">
                  Easily create tasks with titles and descriptions. Keep everything organized in one place.
                </p>
              </div>

              {/* Feature 2 */}
              <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-green-100">
                  <svg
                    className="h-6 w-6 text-green-600"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    aria-hidden="true"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                </div>
                <h3 className="mt-4 text-lg font-semibold text-gray-900">
                  Track Progress
                </h3>
                <p className="mt-2 text-gray-600">
                  Mark tasks as complete and track your progress. Stay motivated as you accomplish your goals.
                </p>
              </div>

              {/* Feature 3 */}
              <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-purple-100">
                  <svg
                    className="h-6 w-6 text-purple-600"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    aria-hidden="true"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
                    />
                  </svg>
                </div>
                <h3 className="mt-4 text-lg font-semibold text-gray-900">
                  Secure & Private
                </h3>
                <p className="mt-2 text-gray-600">
                  Your tasks are private and secure. Only you can see and manage your personal tasks.
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-200 bg-white">
        <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
          <p className="text-center text-sm text-gray-500">
            Built with Next.js 16+ and FastAPI
          </p>
        </div>
      </footer>
    </div>
  );
}
