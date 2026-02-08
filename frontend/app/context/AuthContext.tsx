"use client";

// Authentication Context
// Provides JWT-based authentication that works with the FastAPI backend

import React, { createContext, useState, useContext, useEffect, ReactNode, useCallback } from "react";
import { useRouter } from "next/navigation";
import {
  signIn as apiSignIn,
  signUp as apiSignUp,
  getStoredToken,
  setStoredToken,
  removeStoredToken,
  parseToken,
  isTokenExpired,
} from "@/lib/auth";

interface User {
  username: string;
}

interface AuthContextType {
  token: string | null;
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const router = useRouter();

  // Check for existing session on mount
  useEffect(() => {
    const storedToken = getStoredToken();
    if (storedToken && !isTokenExpired(storedToken)) {
      const payload = parseToken(storedToken);
      if (payload) {
        setToken(storedToken);
        setUser({ username: payload.sub });
        setIsAuthenticated(true);
      }
    }
    setIsLoading(false);
  }, []);

  const login = useCallback(async (username: string, password: string) => {
    setIsLoading(true);
    try {
      const response = await apiSignIn(username, password);
      setStoredToken(response.access_token);
      setToken(response.access_token);
      setUser({ username });
      setIsAuthenticated(true);
      router.push("/");
    } finally {
      setIsLoading(false);
    }
  }, [router]);

  const register = useCallback(async (username: string, password: string) => {
    setIsLoading(true);
    try {
      await apiSignUp(username, password);
      // After registration, automatically log in
      await login(username, password);
    } finally {
      setIsLoading(false);
    }
  }, [login]);

  const logout = useCallback(() => {
    removeStoredToken();
    setToken(null);
    setUser(null);
    setIsAuthenticated(false);
    router.push("/");
  }, [router]);

  return (
    <AuthContext.Provider value={{
      token,
      user,
      isAuthenticated,
      isLoading,
      login,
      register,
      logout
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
