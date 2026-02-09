const API_URL = "http://127.0.0.1:8000";

export interface Todo {
    id: number;
    title: string;
    description?: string;
    completed: boolean;
    priority?: string;
    tags?: string[];
    due_date?: string;
    recurring_interval?: string;
}

export const getTodos = async (token: string, search: string, status: string, priority: string, sort: string) => {
    const params = new URLSearchParams();
    if (search) params.append("search", search);
    if (status !== "all") params.append("status", status);
    if (priority !== "all") params.append("priority", priority);
    if (sort) params.append("sort", sort);

    const response = await fetch(`${API_URL}/todos?${params.toString()}`, {
        headers: {
            "Authorization": `Bearer ${token}`,
        },
    });
    if (!response.ok) {
        throw new Error("Failed to fetch todos");
    }
    return response.json();
};

export const addTodo = async (token: string, todo: Omit<Todo, 'id' | 'completed'>) => {
    const response = await fetch(`${API_URL}/todos`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify(todo),
    });
    if (!response.ok) {
        throw new Error("Failed to add todo");
    }
    return response.json();
};

export const updateTodo = async (token: string, id: number, todo: Partial<Omit<Todo, 'id'>>) => {
    const response = await fetch(`${API_URL}/todos/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify(todo),
    });
    if (!response.ok) {
        throw new Error("Failed to update todo");
    }
    return response.json();
};


export const deleteTodo = async (token: string, id: number) => {
    const response = await fetch(`${API_URL}/todos/${id}`, {
        method: "DELETE",
        headers: {
            "Authorization": `Bearer ${token}`,
        },
    });
    if (!response.ok) {
        throw new Error("Failed to delete todo");
    }
    return response.json();
};

