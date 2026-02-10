/**
 * ErrorMessage Component
 *
 * Reusable error message component with variants
 */

import React from 'react';

export interface ErrorMessageProps {
  message: string;
  variant?: 'inline' | 'banner' | 'toast';
  onDismiss?: () => void;
  className?: string;
}

export default function ErrorMessage({
  message,
  variant = 'inline',
  onDismiss,
  className = '',
}: ErrorMessageProps) {
  if (!message) return null;

  if (variant === 'inline') {
    return (
      <div
        className={`text-sm text-red-400 flex items-center gap-1.5 ${className}`}
        role="alert"
        aria-live="polite"
      >
        <svg className="h-4 w-4 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
        </svg>
        {message}
      </div>
    );
  }

  if (variant === 'banner') {
    return (
      <div
        className={`rounded-xl bg-red-500/10 border border-red-500/30 backdrop-blur-sm p-4 ${className}`}
        role="alert"
        aria-live="polite"
      >
        <div className="flex items-start">
          <div className="flex-shrink-0">
            <svg
              className="h-5 w-5 text-red-400"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
              aria-hidden="true"
            >
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 00-1.06-1.06L10 8.94 8.28 7.22z"
                clipRule="evenodd"
              />
            </svg>
          </div>
          <div className="ml-3 flex-1">
            <p className="text-sm font-medium text-red-300">{message}</p>
          </div>
          {onDismiss && (
            <div className="ml-auto pl-3">
              <button
                type="button"
                onClick={onDismiss}
                className="inline-flex rounded-lg p-1.5 text-red-400 hover:bg-red-500/20 focus:outline-none focus:ring-2 focus:ring-red-500 transition-colors duration-200"
                aria-label="Dismiss error"
              >
                <svg
                  className="h-5 w-5"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" />
                </svg>
              </button>
            </div>
          )}
        </div>
      </div>
    );
  }

  // Toast variant
  return (
    <div
      className={`fixed bottom-4 right-4 max-w-md rounded-xl bg-red-500/10 border border-red-500/30 backdrop-blur-xl p-4 shadow-[0_0_30px_rgba(239,68,68,0.3)] animate-[slide-up_0.3s_ease-out] ${className}`}
      role="alert"
      aria-live="assertive"
    >
      <div className="flex items-start">
        <div className="flex-shrink-0">
          <svg
            className="h-5 w-5 text-red-400"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            fill="currentColor"
            aria-hidden="true"
          >
            <path
              fillRule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 00-1.06-1.06L10 8.94 8.28 7.22z"
              clipRule="evenodd"
            />
          </svg>
        </div>
        <div className="ml-3 flex-1">
          <p className="text-sm font-medium text-red-300">{message}</p>
        </div>
        {onDismiss && (
          <div className="ml-auto pl-3">
            <button
              type="button"
              onClick={onDismiss}
              className="inline-flex rounded-lg p-1.5 text-red-400 hover:bg-red-500/20 focus:outline-none focus:ring-2 focus:ring-red-500 transition-colors duration-200"
              aria-label="Dismiss error"
            >
              <svg
                className="h-5 w-5"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" />
              </svg>
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

/**
 * SuccessMessage Component
 *
 * Success message variant
 */
export function SuccessMessage({
  message,
  variant = 'banner',
  onDismiss,
  className = '',
}: ErrorMessageProps) {
  if (!message) return null;

  return (
    <div
      className={`rounded-xl bg-green-500/10 border border-green-500/30 backdrop-blur-sm p-4 ${className}`}
      role="status"
      aria-live="polite"
    >
      <div className="flex items-start">
        <div className="flex-shrink-0">
          <svg
            className="h-5 w-5 text-green-400"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            fill="currentColor"
            aria-hidden="true"
          >
            <path
              fillRule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z"
              clipRule="evenodd"
            />
          </svg>
        </div>
        <div className="ml-3 flex-1">
          <p className="text-sm font-medium text-green-300">{message}</p>
        </div>
        {onDismiss && (
          <div className="ml-auto pl-3">
            <button
              type="button"
              onClick={onDismiss}
              className="inline-flex rounded-lg p-1.5 text-green-400 hover:bg-green-500/20 focus:outline-none focus:ring-2 focus:ring-green-500 transition-colors duration-200"
              aria-label="Dismiss message"
            >
              <svg
                className="h-5 w-5"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" />
              </svg>
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
