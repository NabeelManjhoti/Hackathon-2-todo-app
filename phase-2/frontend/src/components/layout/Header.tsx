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
    <header className="border-b border-white/10 bg-[#12121a]/80 backdrop-blur-xl sticky top-0 z-50">
      <div className="mx-auto max-w-7xl px-4 py-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-8">
            <Link
              href="/dashboard"
              className="text-2xl font-bold bg-gradient-to-r from-cyan-400 via-purple-400 to-fuchsia-400 bg-clip-text text-transparent hover:scale-105 transition-transform duration-300"
            >
              Todo App
            </Link>

            <nav className="hidden md:flex gap-6">
              <Link
                href="/dashboard"
                className="text-sm font-medium text-gray-300 hover:text-cyan-400 transition-colors duration-300 relative group"
              >
                Dashboard
                <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-cyan-400 to-purple-400 group-hover:w-full transition-all duration-300" />
              </Link>
            </nav>
          </div>

          <div className="flex items-center gap-4">
            {user && (
              <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-white/5 border border-white/10">
                <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
                <span className="text-sm text-gray-300">
                  {user.email}
                </span>
              </div>
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
