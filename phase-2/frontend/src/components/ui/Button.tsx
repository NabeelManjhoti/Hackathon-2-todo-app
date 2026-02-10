/**
 * Button Component
 *
 * Reusable button component with variants and loading states
 */

import React from 'react';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  fullWidth?: boolean;
  children: React.ReactNode;
}

export default function Button({
  variant = 'primary',
  size = 'md',
  loading = false,
  fullWidth = false,
  disabled,
  className = '',
  children,
  ...props
}: ButtonProps) {
  const baseStyles = 'inline-flex items-center justify-center font-semibold rounded-lg transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-[#0a0a0f] disabled:opacity-50 disabled:cursor-not-allowed relative overflow-hidden group';

  const variantStyles = {
    primary: 'bg-gradient-to-r from-purple-600 via-violet-600 to-fuchsia-600 text-white hover:shadow-[0_0_30px_rgba(139,92,246,0.6)] focus:ring-purple-500 hover:scale-[1.02] active:scale-[0.98]',
    secondary: 'bg-[#1a1a28] text-gray-200 hover:bg-[#22223a] border border-gray-700 hover:border-purple-500/50 focus:ring-purple-500 hover:shadow-[0_0_20px_rgba(139,92,246,0.3)]',
    danger: 'bg-gradient-to-r from-red-600 to-pink-600 text-white hover:shadow-[0_0_30px_rgba(239,68,68,0.6)] focus:ring-red-500 hover:scale-[1.02] active:scale-[0.98]',
    ghost: 'bg-transparent text-gray-300 hover:bg-white/5 border border-transparent hover:border-purple-500/30 focus:ring-purple-500',
  };

  const sizeStyles = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-2.5 text-base',
    lg: 'px-8 py-3.5 text-lg',
  };

  const widthStyles = fullWidth ? 'w-full' : '';

  return (
    <button
      className={`${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]} ${widthStyles} ${className}`}
      disabled={disabled || loading}
      {...props}
    >
      {/* Shimmer effect on hover */}
      <span className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent translate-x-[-200%] group-hover:translate-x-[200%] transition-transform duration-1000" />

      {loading && (
        <svg
          className="animate-spin -ml-1 mr-2 h-4 w-4 relative z-10"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
          />
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          />
        </svg>
      )}
      <span className="relative z-10">{children}</span>
    </button>
  );
}
