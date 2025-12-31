import { useState, useEffect, createContext, useContext, ReactNode } from 'react';
import { User, AuthResponse } from '../lib/types';
import { authAPI } from '../lib/api';
import { setAuthToken, removeAuthToken, isAuthenticated as isAuthed, getUserInfo } from '../lib/auth';

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<AuthResponse>;
  logout: () => void;
  register: (email: string, password: string, firstName?: string, lastName?: string) => Promise<any>;
  verifyToken: () => Promise<boolean>;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is already authenticated on initial load
    const checkAuth = async () => {
      if (isAuthed()) {
        const userInfo = getUserInfo();
        if (userInfo) {
          setUser({
            id: userInfo.sub,
            email: userInfo.email,
          } as User);
          setToken(localStorage.getItem('access_token'));
        }
      }
      setLoading(false);
    };

    checkAuth();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const response = await authAPI.login(email, password);
      const { access_token, user } = response.data;

      setAuthToken(access_token);
      setToken(access_token);
      setUser(user);

      return response.data;
    } catch (error) {
      throw error;
    }
  };

  const logout = () => {
    removeAuthToken();
    setToken(null);
    setUser(null);
  };

  const register = async (email: string, password: string, firstName?: string, lastName?: string) => {
    try {
      const response = await authAPI.register(email, password, firstName, lastName);
      return response.data;
    } catch (error) {
      throw error;
    }
  };

  const verifyToken = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) return false;

      await authAPI.verify(token);
      return true;
    } catch (error) {
      return false;
    }
  };

  const value = {
    user,
    token,
    login,
    logout,
    register,
    verifyToken,
    loading,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};