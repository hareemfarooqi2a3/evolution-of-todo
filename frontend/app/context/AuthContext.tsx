"use client";

import React, { createContext, useState, useContext, useEffect, ReactNode } from "react";
import { useRouter } from "next/navigation";

interface AuthContextType {
    token: string | null;
    isAuthenticated: boolean;
    login: (token: string) => void;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
    const [token, setToken] = useState<string | null>(null);
    const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
    const router = useRouter();

    useEffect(() => {
        const storedToken = localStorage.getItem("token");
        if (storedToken) {
            setToken(storedToken);
            setIsAuthenticated(true);
        }
    }, []);

    const login = (newToken: string) => {
        localStorage.setItem("token", newToken);
        setToken(newToken);
        setIsAuthenticated(true);
        router.push("/"); // Redirect to home page after login
    };

    const logout = () => {
        localStorage.removeItem("token");
        setToken(null);
        setIsAuthenticated(false);
        router.push("/login"); // Redirect to login page after logout
    };

    return (
        <AuthContext.Provider value={{ token, isAuthenticated, login, logout }}>
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