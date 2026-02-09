/**
 * Signin Page
 *
 * User authentication page
 */

'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/src/lib/hooks/useAuth';
import SigninForm from '@/src/components/auth/SigninForm';
import LoadingSpinner from '@/src/components/ui/LoadingSpinner';

export default function SigninPage() {
  const router = useRouter();
  const { isAuthenticated, loading } = useAuth();

  // Redirect if already authenticated
  useEffect(() => {
    if (!loading && isAuthenticated) {
      router.push('/dashboard');
    }
  }, [isAuthenticated, loading, router]);

  // Show loading while checking auth
  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <LoadingSpinner size="lg" label="Loading..." />
      </div>
    );
  }

  // Don't render if authenticated (will redirect)
  if (isAuthenticated) {
    return null;
  }

  return (
    <div className="flex min-h-screen flex-col bg-gray-50">
      {/* Header */}
      <header className="border-b border-gray-200 bg-white">
        <div className="mx-auto max-w-7xl px-4 py-4 sm:px-6 lg:px-8">
          <Link href="/" className="text-2xl font-bold text-gray-900">
            Todo App
          </Link>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex flex-1 items-center justify-center px-4 py-12 sm:px-6 lg:px-8">
        <SigninForm />
      </main>
    </div>
  );
}
