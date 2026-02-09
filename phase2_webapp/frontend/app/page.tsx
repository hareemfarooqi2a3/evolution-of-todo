"use client";

// Main Todo App Page

import { useState, useEffect, useCallback } from "react";
import toast from "react-hot-toast";
import TodoForm from "./components/TodoForm";
import TodoList from "./components/TodoList";
import Login from "./components/Login";
import Register from "./components/Register";
import { getTodos, addTodo, updateTodo, deleteTodo, Todo } from "./services/todoAPI";
import { useAuth } from "./context/AuthContext";

export default function Home() {
  const { token, user, isAuthenticated, isLoading: authLoading, logout } = useAuth();
  const [showRegister, setShowRegister] = useState(false);
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchText, setSearchText] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [priorityFilter, setPriorityFilter] = useState("all");
  const [sortOrder, setSortOrder] = useState("title");

  const fetchTodos = useCallback(async () => {
    if (!token) return;

    setLoading(true);
    try {
      const data = await getTodos(token, searchText, statusFilter, priorityFilter, sortOrder);
      setTodos(data);
    } catch (error) {
      console.error(error);
      toast.error("Failed to fetch todos");
    } finally {
      setLoading(false);
    }
  }, [token, searchText, statusFilter, priorityFilter, sortOrder]);

  useEffect(() => {
    if (isAuthenticated && token) {
      fetchTodos();
    } else {
      setTodos([]);
      setLoading(false);
    }
  }, [isAuthenticated, token, fetchTodos]);

  useEffect(() => {
    if (typeof window !== "undefined" && "Notification" in window && Notification.permission !== "granted") {
      Notification.requestPermission();
    }

    const checkDueDates = () => {
      if (!isAuthenticated || !token) return;
      todos.forEach(todo => {
        if (todo.due_date && !todo.completed) {
          const dueDate = new Date(todo.due_date);
          const now = new Date();
          const oneHour = 60 * 60 * 1000;
          if (dueDate.getTime() > now.getTime() && dueDate.getTime() - now.getTime() < oneHour) {
            if ("Notification" in window && Notification.permission === "granted") {
              new Notification(`Todo due soon: ${todo.title}`);
            }
          }
        }
      });
    };

    const interval = setInterval(checkDueDates, 60000);
    return () => clearInterval(interval);
  }, [todos, isAuthenticated, token]);

  const handleAddTodo = async (todo: Omit<Todo, 'id' | 'completed'>) => {
    if (!token) return;
    try {
      await addTodo(token, todo);
      fetchTodos();
      toast.success("Todo added successfully");
    } catch (error: unknown) {
      console.error(error);
      const errorMessage = error instanceof Error ? error.message : "Failed to add todo";
      toast.error(errorMessage);
    }
  };

  const handleToggle = async (id: number, completed: boolean) => {
    if (!token) return;
    try {
      const updatedTodo = await updateTodo(token, id, { completed });
      setTodos(todos.map((todo) => (todo.id === id ? updatedTodo : todo)));
      toast.success("Todo updated successfully");
    } catch (error: unknown) {
      console.error(error);
      const errorMessage = error instanceof Error ? error.message : "Failed to update todo";
      toast.error(errorMessage);
    }
  };

  const handleDelete = async (id: number) => {
    if (!token) return;
    try {
      await deleteTodo(token, id);
      setTodos(todos.filter((todo) => todo.id !== id));
      toast.success("Todo deleted successfully");
    } catch (error: unknown) {
      console.error(error);
      const errorMessage = error instanceof Error ? error.message : "Failed to delete todo";
      toast.error(errorMessage);
    }
  };

  const handleUpdate = async (id: number, todo: Partial<Omit<Todo, 'id'>>) => {
    if (!token) return;
    try {
      const updatedTodo = await updateTodo(token, id, todo);
      setTodos(todos.map((t) => (t.id === id ? updatedTodo : t)));
      toast.success("Todo updated successfully");
    } catch (error: unknown) {
      console.error(error);
      const errorMessage = error instanceof Error ? error.message : "Failed to update todo";
      toast.error(errorMessage);
    }
  };

  // Show loading state while checking auth
  if (authLoading) {
    return (
      <main className="container mx-auto p-4 flex items-center justify-center min-h-screen bg-gray-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </main>
    );
  }

  if (!isAuthenticated) {
    return (
      <main className="container mx-auto p-4 flex items-center justify-center min-h-screen bg-gray-100">
        {showRegister ? (
          <Register onSwitchToLogin={() => setShowRegister(false)} />
        ) : (
          <Login onSwitchToRegister={() => setShowRegister(true)} />
        )}
      </main>
    );
  }

  return (
    <main className="container mx-auto p-4">
      <div className="max-w-4xl mx-auto bg-white p-8 rounded-lg shadow-lg">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-4xl font-bold text-gray-800">Todo App</h1>
            {user && (
              <p className="text-sm text-gray-500">Welcome, {user.username}</p>
            )}
          </div>
          <button
            onClick={logout}
            className="py-2 px-4 rounded-md text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
          >
            Logout
          </button>
        </div>
        <TodoForm onAdd={handleAddTodo} />
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <input
            type="text"
            placeholder="Search..."
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            className="p-2 border rounded-lg shadow-sm"
          />
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="p-2 border rounded-lg shadow-sm"
          >
            <option value="all">All Statuses</option>
            <option value="completed">Completed</option>
            <option value="incomplete">Incomplete</option>
          </select>
          <select
            value={priorityFilter}
            onChange={(e) => setPriorityFilter(e.target.value)}
            className="p-2 border rounded-lg shadow-sm"
          >
            <option value="all">All Priorities</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
          <select
            value={sortOrder}
            onChange={(e) => setSortOrder(e.target.value)}
            className="p-2 border rounded-lg shadow-sm"
          >
            <option value="title">Sort by Title</option>
            <option value="priority">Sort by Priority</option>
            <option value="due_date">Sort by Due Date</option>
          </select>
        </div>
        {loading ? (
          <p className="text-center text-gray-500">Loading...</p>
        ) : todos.length > 0 ? (
          <TodoList
            todos={todos}
            onToggle={handleToggle}
            onDelete={handleDelete}
            onUpdate={handleUpdate}
          />
        ) : (
          <p className="text-center text-gray-500">No todos found.</p>
        )}
      </div>
    </main>
  );
}
