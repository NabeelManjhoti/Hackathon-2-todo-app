/**
 * EmptyState Component
 *
 * Display when user has no tasks
 */

import React from 'react';

export interface EmptyStateProps {
  onCreateTask?: () => void;
}

export default function EmptyState({ onCreateTask }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-16 text-center animate-[fade-in_0.6s_ease-out]">
      <div className="relative">
        {/* Glowing background effect */}
        <div className="absolute inset-0 bg-gradient-to-r from-purple-600/20 via-fuchsia-600/20 to-cyan-600/20 blur-3xl animate-pulse" />

        <div className="relative rounded-full bg-gradient-to-br from-[#1a1a28] to-[#12121a] p-8 border border-white/10 shadow-[0_0_40px_rgba(139,92,246,0.3)]">
          <svg
            className="h-16 w-16 text-purple-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={1.5}
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"
            />
          </svg>
        </div>
      </div>

      <h3 className="mt-8 text-2xl font-bold bg-gradient-to-r from-gray-200 to-gray-400 bg-clip-text text-transparent">
        No tasks yet
      </h3>

      <p className="mt-3 max-w-sm text-base text-gray-400 leading-relaxed">
        Get started by creating your first task. Stay organized and track your progress.
      </p>

      {onCreateTask && (
        <button
          onClick={onCreateTask}
          className="mt-8 inline-flex items-center gap-2 rounded-lg bg-gradient-to-r from-purple-600 via-violet-600 to-fuchsia-600 px-6 py-3 text-base font-semibold text-white transition-all duration-300 hover:shadow-[0_0_30px_rgba(139,92,246,0.6)] hover:scale-105 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-[#0a0a0f] active:scale-95 group relative overflow-hidden"
        >
          {/* Shimmer effect */}
          <span className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent translate-x-[-200%] group-hover:translate-x-[200%] transition-transform duration-1000" />

          <svg
            className="h-5 w-5 relative z-10"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 4v16m8-8H4"
            />
          </svg>
          <span className="relative z-10">Create Your First Task</span>
        </button>
      )}
    </div>
  );
}
