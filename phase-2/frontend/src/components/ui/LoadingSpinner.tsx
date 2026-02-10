/**
 * LoadingSpinner Component
 *
 * Reusable loading spinner with size variants
 */

import React from 'react';

export interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  className?: string;
  label?: string;
}

export default function LoadingSpinner({
  size = 'md',
  className = '',
  label = 'Loading...',
}: LoadingSpinnerProps) {
  const sizeStyles = {
    sm: 'h-4 w-4',
    md: 'h-8 w-8',
    lg: 'h-12 w-12',
    xl: 'h-16 w-16',
  };

  return (
    <div className={`flex items-center justify-center ${className}`} role="status" aria-live="polite">
      <svg
        className={`animate-spin ${sizeStyles[size]}`}
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        aria-hidden="true"
        style={{
          filter: 'drop-shadow(0 0 8px rgba(139, 92, 246, 0.6))',
        }}
      >
        <circle
          className="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="url(#spinner-gradient)"
          strokeWidth="4"
        />
        <path
          className="opacity-75"
          fill="url(#spinner-gradient)"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        />
        <defs>
          <linearGradient id="spinner-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#8b5cf6" />
            <stop offset="50%" stopColor="#a78bfa" />
            <stop offset="100%" stopColor="#c084fc" />
          </linearGradient>
        </defs>
      </svg>
      <span className="sr-only">{label}</span>
    </div>
  );
}

/**
 * FullPageSpinner Component
 *
 * Loading spinner that covers the entire page
 */
export function FullPageSpinner({ label = 'Loading...' }: { label?: string }) {
  return (
    <div className="fixed inset-0 flex items-center justify-center bg-[#0a0a0f]/95 backdrop-blur-sm z-50">
      <div className="text-center">
        <LoadingSpinner size="xl" label={label} />
        <p className="mt-4 text-gray-400 text-sm">{label}</p>
      </div>
    </div>
  );
}

/**
 * InlineSpinner Component
 *
 * Small spinner for inline loading states
 */
export function InlineSpinner({ label = 'Loading...' }: { label?: string }) {
  return <LoadingSpinner size="sm" label={label} />;
}
