'use client';

/**
 * Chat Layout
 *
 * Protected layout for chat interface with authentication verification
 */

import { useEffect } from 'react';
import { useAuth } from '@/src/lib/hooks/useAuth';
import { useRouter } from 'next/navigation';
import LoadingSpinner from '@/src/components/ui/LoadingSpinner';

export default function ChatLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { isAuthenticated, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push('/signin?redirect=/chat');
    }
  }, [loading, isAuthenticated, router]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
        <LoadingSpinner size="large" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return <>{children}</>;
}
