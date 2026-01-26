"use client";

import { useState, useEffect } from "react";
import toast from "react-hot-toast";
import TodoForm from "./components/TodoForm";
import TodoList from "./components/TodoList";
import { getTodos, addTodo, updateTodo, deleteTodo, Todo } from "./services/todoAPI";

export default function Home() {
    const [todos, setTodos] = useState<Todo[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchText, setSearchText] = useState("");
    const [statusFilter, setStatusFilter] = useState("all");
    const [priorityFilter, setPriorityFilter] = useState("all");
    const [sortOrder, setSortOrder] = useState("title");

    const fetchTodos = async () => {
        setLoading(true);
        try {
            const data = await getTodos(searchText, statusFilter, priorityFilter, sortOrder);
            setTodos(data);
        } catch (error) {
            console.error(error);
            toast.error("Failed to fetch todos");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchTodos();
    }, [searchText, statusFilter, priorityFilter, sortOrder]);

    useEffect(() => {
        if (Notification.permission !== "granted") {
            Notification.requestPermission();
        }

        const checkDueDates = () => {
            todos.forEach(todo => {
                if (todo.due_date && !todo.completed) {
                    const dueDate = new Date(todo.due_date);
                    const now = new Date();
                    const oneHour = 60 * 60 * 1000;
                    if (dueDate.getTime() > now.getTime() && dueDate.getTime() - now.getTime() < oneHour) {
                        new Notification(`Todo due soon: ${todo.title}`);
                    }
                }
            });
        };

        const interval = setInterval(checkDueDates, 60000); // Check every minute

        return () => clearInterval(interval);
    }, [todos]);

    const handleAddTodo = async (todo: Omit<Todo, 'id' | 'completed'>) => {
        try {
            await addTodo(todo);
            fetchTodos(); // Refetch todos after adding a new one
            toast.success("Todo added successfully");
        } catch (error)_
            console.error(error);
            toast.error("Failed to add todo");
        }
    };

    const handleToggle = async (id: number, completed: boolean) => {
        try {
            const updatedTodo = await updateTodo(id, { completed });
            setTodos(todos.map((todo) => (todo.id === id ? updatedTodo : todo)));
            toast.success("Todo updated successfully");
        } catch (error) {
            console.error(error);
            toast.error("Failed to update todo");
        }
    };

    const handleDelete = async (id: number) => {
        try {
            await deleteTodo(id);
            setTodos(todos.filter((todo) => todo.id !== id));
            toast.success("Todo deleted successfully");
        } catch (error) {
            console.error(error);
            toast.error("Failed to delete todo");
        }
    };

    const handleUpdate = async (id: number, todo: Partial<Omit<Todo, 'id'>>) => {
        try {
            const updatedTodo = await updateTodo(id, todo);
            setTodos(todos.map((t) => (t.id === id ? updatedTodo : t)));
            toast.success("Todo updated successfully");
        } catch (error) {
            console.error(error);
            toast.error("Failed to update todo");
        }
    };

    return (
        <main className="container mx-auto p-4">
            <div className="max-w-4xl mx-auto bg-white p-8 rounded-lg shadow-lg">
                <h1 className="text-4xl font-bold mb-6 text-center text-gray-800">Todo App</h1>
                <TodoForm onAdd={handleAddTodo} />
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                    <input
                        type="text"
                        placeholder="Search..."
                        value={searchText}
                        onChange={(e) => setSearchText(e.target.value)}
                        className="p-2 border rounded-lg shadow-sm"
                    />
                    <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)} className="p-2 border rounded-lg shadow-sm">
                        <option value="all">All Statuses</option>
                        <option value="completed">Completed</option>
                        <option value="incomplete">Incomplete</option>
                    </select>
                    <select value={priorityFilter} onChange={(e) => setPriorityFilter(e.target.value)} className="p-2 border rounded-lg shadow-sm">
                        <option value="all">All Priorities</option>
                        <option value="high">High</option>
                        <option value="medium">Medium</option>
                        <option value="low">Low</option>
                    </select>
                    <select value={sortOrder} onChange={(e) => setSortOrder(e.target.value)} className="p-2 border rounded-lg shadow-sm">
                        <option value="title">Sort by Title</option>
                        <option value="priority">Sort by Priority</option>
                    </select>
                </div>
                {loading ? <p className="text-center text-gray-500">Loading...</p> : (
                    todos.length > 0 ? (
                        <TodoList
                            todos={todos}
                            onToggle={handleToggle}
                            onDelete={handleDelete}
                            onUpdate={handleUpdate}
                        />
                    ) : (
                        <p className="text-center text-gray-500">No todos found.</p>
                    )
                )}
            </div>
        </main>
    );
}