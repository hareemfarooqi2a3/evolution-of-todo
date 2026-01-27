"use client";

import { useState } from "react";

interface LoginProps {
    onLoginSuccess: (token: string) => void;
    onSwitchToRegister: () => void;
}

export default function Login({ onLoginSuccess, onSwitchToRegister }: LoginProps) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);
        setLoading(true);

        try {
            const response = await fetch("http://localhost:8000/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: new URLSearchParams({
                    username: username,
                    password: password,
                }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Login failed");
            }

            const data = await response.json();
            onLoginSuccess(data.access_token);
        } catch (err: any) {
            setError(err.message || "An unknown error occurred");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-md mx-auto bg-white p-8 rounded-lg shadow-lg">
            <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">Login</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
                {error && <p className="text-red-500 text-center">{error}</p>}
                <div>
                    <label htmlFor="username" className="block text-sm font-medium text-gray-700">
                        Username
                    </label>
                    <input
                        type="text"
                        id="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
                        required
                    />
                </div>
                <div>
                    <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                        Password
                    </label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
                        required
                    />
                </div>
                <button
                    type="submit"
                    className="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    disabled={loading}
                >
                    {loading ? "Logging in..." : "Login"}
                </button>
            </form>
            <p className="mt-4 text-center text-sm text-gray-600">
                Don't have an account?{" "}
                <button
                    type="button"
                    onClick={onSwitchToRegister}
                    className="font-medium text-indigo-600 hover:text-indigo-500"
                >
                    Register
                </button>
            </p>
        </div>
    );
}