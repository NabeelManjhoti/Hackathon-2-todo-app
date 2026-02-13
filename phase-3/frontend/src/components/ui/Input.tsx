/**
 * Input Component
 *
 * Reusable input component with label, error states, and accessibility
 */

import React from 'react';

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
  fullWidth?: boolean;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, helperText, fullWidth = false, className = '', id, ...props }, ref) => {
    const inputId = id || `input-${Math.random().toString(36).substr(2, 9)}`;
    const errorId = `${inputId}-error`;
    const helperId = `${inputId}-helper`;

    const baseStyles = 'block rounded-lg border px-4 py-3 text-base bg-[#1a1a28] text-gray-100 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-[#0a0a0f] placeholder:text-gray-500';
    const normalStyles = 'border-gray-700 focus:border-purple-500 focus:ring-purple-500/50 hover:border-gray-600 focus:shadow-[0_0_20px_rgba(139,92,246,0.3)]';
    const errorStyles = 'border-red-500 focus:border-red-500 focus:ring-red-500/50 focus:shadow-[0_0_20px_rgba(239,68,68,0.3)]';
    const disabledStyles = 'disabled:bg-[#12121a] disabled:text-gray-600 disabled:cursor-not-allowed disabled:border-gray-800';
    const widthStyles = fullWidth ? 'w-full' : '';

    return (
      <div className={fullWidth ? 'w-full' : ''}>
        {label && (
          <label
            htmlFor={inputId}
            className="block text-sm font-semibold text-gray-300 mb-2"
          >
            {label}
            {props.required && <span className="text-red-400 ml-1" aria-label="required">*</span>}
          </label>
        )}

        <input
          ref={ref}
          id={inputId}
          className={`${baseStyles} ${error ? errorStyles : normalStyles} ${disabledStyles} ${widthStyles} ${className}`}
          aria-invalid={error ? 'true' : 'false'}
          aria-describedby={error ? errorId : helperText ? helperId : undefined}
          {...props}
        />

        {error && (
          <p
            id={errorId}
            className="mt-2 text-sm text-red-400 flex items-center gap-1.5"
            role="alert"
          >
            <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
            {error}
          </p>
        )}

        {!error && helperText && (
          <p
            id={helperId}
            className="mt-2 text-sm text-gray-500"
          >
            {helperText}
          </p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';

export default Input;
