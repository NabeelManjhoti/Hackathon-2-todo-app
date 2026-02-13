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
    <div className="flex min-h-screen flex-col">
      {/* Header */}
      <header className="border-b border-white/10 bg-[#12121a]/80 backdrop-blur-xl sticky top-0 z-50">
        <div className="mx-auto max-w-7xl px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 via-purple-400 to-fuchsia-400 bg-clip-text text-transparent">
              Eclipse
            </h1>
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
            <h2 className="text-5xl font-bold tracking-tight sm:text-6xl md:text-7xl animate-[fade-in_0.8s_ease-out]">
              <span className="block bg-gradient-to-r from-cyan-400 via-purple-400 to-fuchsia-400 bg-clip-text text-transparent">
                Manage Your Tasks
              </span>
              <span className="block mt-2 bg-gradient-to-r from-fuchsia-400 via-purple-400 to-cyan-400 bg-clip-text text-transparent">
                Efficiently
              </span>
            </h2>
            <p className="mx-auto mt-8 max-w-2xl text-lg text-gray-300 leading-relaxed animate-[fade-in_0.8s_ease-out_0.2s] opacity-0 [animation-fill-mode:forwards]">
              A modern, full-stack todo application that helps you organize your tasks,
              track your progress, and boost your productivity.
            </p>

            {/* CTA Buttons */}
            <div className="mt-12 flex justify-center gap-4 animate-[fade-in_0.8s_ease-out_0.4s] opacity-0 [animation-fill-mode:forwards]">
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
            <div className="mt-10 animate-[fade-in_0.8s_ease-out_0.6s] opacity-0 [animation-fill-mode:forwards]">
              {apiStatus.checking ? (
                <div className="flex items-center justify-center gap-2 text-sm text-gray-400">
                  <LoadingSpinner size="sm" />
                  <span>Checking API connection...</span>
                </div>
              ) : apiStatus.connected ? (
                <div className="flex items-center justify-center gap-2 text-sm text-green-400">
                  <div className="relative">
                    <div className="absolute inset-0 bg-green-400 blur-md opacity-50 animate-pulse" />
                    <svg
                      className="h-5 w-5 relative"
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
                  </div>
                  <span>API Connected</span>
                </div>
              ) : (
                <ErrorMessage
                  message={`API Connection Failed: ${apiStatus.message}`}
                  variant="inline"
                  className="text-center justify-center"
                />
              )}
            </div>
          </div>

          {/* Features Section */}
          <div className="mt-32">
            <div className="grid gap-8 md:grid-cols-3">
              {/* Feature 1 */}
              <div className="group rounded-2xl border border-white/10 bg-gradient-to-br from-[#1a1a28]/90 to-[#12121a]/90 backdrop-blur-sm p-8 shadow-lg transition-all duration-300 hover:shadow-[0_0_40px_rgba(139,92,246,0.4)] hover:border-purple-500/50 hover:scale-[1.02] animate-[fade-in_0.8s_ease-out_0.8s] opacity-0 [animation-fill-mode:forwards]">
                <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-gradient-to-br from-blue-500/20 to-cyan-500/20 border border-cyan-500/30 shadow-[0_0_20px_rgba(6,182,212,0.3)] group-hover:shadow-[0_0_30px_rgba(6,182,212,0.5)] transition-all duration-300">
                  <svg
                    className="h-7 w-7 text-cyan-400"
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
                <h3 className="mt-6 text-xl font-bold text-gray-100 group-hover:text-white transition-colors duration-300">
                  Create & Organize
                </h3>
                <p className="mt-3 text-gray-400 leading-relaxed group-hover:text-gray-300 transition-colors duration-300">
                  Easily create tasks with titles and descriptions. Keep everything organized in one place.
                </p>
              </div>

              {/* Feature 2 */}
              <div className="group rounded-2xl border border-white/10 bg-gradient-to-br from-[#1a1a28]/90 to-[#12121a]/90 backdrop-blur-sm p-8 shadow-lg transition-all duration-300 hover:shadow-[0_0_40px_rgba(34,197,94,0.4)] hover:border-green-500/50 hover:scale-[1.02] animate-[fade-in_0.8s_ease-out_1s] opacity-0 [animation-fill-mode:forwards]">
                <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-gradient-to-br from-green-500/20 to-emerald-500/20 border border-green-500/30 shadow-[0_0_20px_rgba(34,197,94,0.3)] group-hover:shadow-[0_0_30px_rgba(34,197,94,0.5)] transition-all duration-300">
                  <svg
                    className="h-7 w-7 text-green-400"
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
                <h3 className="mt-6 text-xl font-bold text-gray-100 group-hover:text-white transition-colors duration-300">
                  Track Progress
                </h3>
                <p className="mt-3 text-gray-400 leading-relaxed group-hover:text-gray-300 transition-colors duration-300">
                  Mark tasks as complete and track your progress. Stay motivated as you accomplish your goals.
                </p>
              </div>

              {/* Feature 3 */}
              <div className="group rounded-2xl border border-white/10 bg-gradient-to-br from-[#1a1a28]/90 to-[#12121a]/90 backdrop-blur-sm p-8 shadow-lg transition-all duration-300 hover:shadow-[0_0_40px_rgba(168,85,247,0.4)] hover:border-purple-500/50 hover:scale-[1.02] animate-[fade-in_0.8s_ease-out_1.2s] opacity-0 [animation-fill-mode:forwards]">
                <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-gradient-to-br from-purple-500/20 to-fuchsia-500/20 border border-purple-500/30 shadow-[0_0_20px_rgba(168,85,247,0.3)] group-hover:shadow-[0_0_30px_rgba(168,85,247,0.5)] transition-all duration-300">
                  <svg
                    className="h-7 w-7 text-purple-400"
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
                <h3 className="mt-6 text-xl font-bold text-gray-100 group-hover:text-white transition-colors duration-300">
                  Secure & Private
                </h3>
                <p className="mt-3 text-gray-400 leading-relaxed group-hover:text-gray-300 transition-colors duration-300">
                  Your tasks are private and secure. Only you can see and manage your personal tasks.
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-white/10 bg-[#12121a]/80 backdrop-blur-xl">
        <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
          <p className="text-center text-sm text-gray-500">
            Built with ❤️ by Muhammad Nabeel Ali
          </p>
        </div>
      </footer>
    </div>
  );
}
