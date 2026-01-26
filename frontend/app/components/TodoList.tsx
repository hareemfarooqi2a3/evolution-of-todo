import TodoItem from "./TodoItem";

interface Todo {
    id: number;
    title: string;
    description?: string;
    completed: boolean;
    priority?: string;
    tags?: string[];
}

interface TodoListProps {
    todos: Todo[];
    onToggle: (id: number, completed: boolean) => void;
    onDelete: (id: number) => void;
    onUpdate: (id: number, todo: { title?: string; description?: string }) => void;
}

export default function TodoList({ todos, onToggle, onDelete, onUpdate }: TodoListProps) {
    return (
        <div>
            {todos.map((todo) => (
                <TodoItem
                    key={todo.id}
                    todo={todo}
                    onToggle={onToggle}
                    onDelete={onDelete}
                    onUpdate={onUpdate}
                />
            ))}
        </div>
    );
}


