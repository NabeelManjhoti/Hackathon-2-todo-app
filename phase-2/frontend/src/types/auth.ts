/**
 * Authentication Types
 *
 * Type definitions for authentication and user management
 */

/**
 * User object returned from backend
 */
export interface User {
  id: number;
  email: string;
  created_at?: string;
  updated_at?: string;
}

/**
 * Authentication response from signin/signup
 */
export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

/**
 * Signup request payload
 */
export interface SignupRequest {
  email: string;
  password: string;
}

/**
 * Signin request payload
 */
export interface SigninRequest {
  email: string;
  password: string;
}

/**
 * Logout response
 */
export interface LogoutResponse {
  message: string;
}

/**
 * Authentication state
 */
export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  loading: boolean;
}

/**
 * Authentication context value
 */
export interface AuthContextValue extends AuthState {
  login: (token: string, user: User) => void;
  logout: () => void;
  setLoading: (loading: boolean) => void;
}
