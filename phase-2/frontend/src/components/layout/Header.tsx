/**
 * Header Component
 *
 * Application header with navigation and logout
 */

'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/src/lib/hooks/useAuth';
import { logout as logoutApi } from '@/src/lib/api/auth';
import Button from '@/src/components/ui/Button';

export default function Header() {
  const router = useRouter();
  const { user, logout } = useAuth();
  const [loggingOut, setLoggingOut] = useState(false);

  const handleLogout = async () => {
    setLoggingOut(true);

    try {
      // Call logout API
      await logoutApi();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Clear local auth state regardless of API call result
      logout();
      router.push('/signin');
    }
  };

  return (
    <header className="border-b border-gray-200 bg-white">
      <div className="mx-auto max-w-7xl px-4 py-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-8">
            <Link href="/dashboard" className="text-2xl font-bold text-gray-900">
              Todo App
            </Link>

            <nav className="hidden md:flex gap-6">
              <Link
                href="/dashboard"
                className="text-sm font-medium text-gray-700 hover:text-gray-900"
              >
                Dashboard
              </Link>
            </nav>
          </div>

          <div className="flex items-center gap-4">
            {user && (
              <span className="text-sm text-gray-600 hidden sm:inline">
                {user.email}
              </span>
            )}

            <Button
              variant="ghost"
              size="sm"
              onClick={handleLogout}
              loading={loggingOut}
              disabled={loggingOut}
            >
              {loggingOut ? 'Logging out...' : 'Logout'}
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
}
