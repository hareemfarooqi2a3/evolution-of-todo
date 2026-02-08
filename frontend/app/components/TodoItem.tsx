"use client";

import { useState } from "react";
import Modal from "react-modal";
import EditTodoForm from "./EditTodoForm";
import { Todo } from "../services/todoAPI";

interface TodoItemProps {
    todo: Todo;
    onToggle: (id: number, completed: boolean) => void;
    onDelete: (id: number) => void;
    onUpdate: (id: number, todo: Partial<Omit<Todo, 'id'>>) => void;
}

Modal.setAppElement("body");

// Priority badge styles
const priorityBadgeStyles: Record<string, string> = {
    High: "bg-red-500 text-white",
    Medium: "bg-yellow-500 text-white",
    Low: "bg-green-500 text-white",
};

const priorityBorderStyles: Record<string, string> = {
    High: "border-red-500",
    Medium: "border-yellow-500",
    Low: "border-green-500",
};

// Format due date with relative time indicator
const formatDueDate = (dueDate: string) => {
    const date = new Date(dueDate);
    const now = new Date();
    const diffTime = date.getTime() - now.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    const formattedDate = date.toLocaleDateString();

    if (diffDays < 0) {
        return { text: `Overdue: ${formattedDate}`, className: "text-red-600 font-semibold" };
    } else if (diffDays === 0) {
        return { text: `Due today: ${formattedDate}`, className: "text-orange-600 font-semibold" };
    } else if (diffDays === 1) {
        return { text: `Due tomorrow: ${formattedDate}`, className: "text-yellow-600" };
    } else if (diffDays <= 7) {
        return { text: `Due in ${diffDays} days: ${formattedDate}`, className: "text-blue-600" };
    }
    return { text: `Due: ${formattedDate}`, className: "text-gray-500" };
};

export default function TodoItem({ todo, onToggle, onDelete, onUpdate }: TodoItemProps) {
    const [isModalOpen, setIsModalOpen] = useState(false);

    const openModal = () => setIsModalOpen(true);
    const closeModal = () => setIsModalOpen(false);

    const priority = todo.priority || "Medium";
    const priorityBorder = priorityBorderStyles[priority] || priorityBorderStyles.Medium;
    const priorityBadge = priorityBadgeStyles[priority] || priorityBadgeStyles.Medium;

    return (
        <div className={`p-4 mb-4 border-l-4 ${priorityBorder} bg-white rounded-lg shadow-md flex justify-between items-start transition-transform transform hover:scale-105 ${todo.completed ? "opacity-50" : ""}`}>
            <div className="flex items-start flex-1">
                <input
                    type="checkbox"
                    checked={todo.completed}
                    onChange={(e) => onToggle(todo.id, e.target.checked)}
                    className="h-6 w-6 mt-1 rounded-full border-gray-300 text-indigo-600 focus:ring-indigo-500 cursor-pointer"
                />
                <div className="ml-4 flex-1">
                    <div className="flex items-center flex-wrap gap-2">
                        <h3 className={`text-lg font-bold ${todo.completed ? "line-through text-gray-400" : "text-gray-800"}`}>
                            {todo.title}
                        </h3>
                        {/* Priority Badge */}
                        <span className={`text-xs font-semibold px-2 py-1 rounded-full ${priorityBadge}`}>
                            {priority}
                        </span>
                        {/* Recurring Indicator */}
                        {todo.recurring_interval && (
                            <span
                                className="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded-full font-medium"
                                title={`Recurs ${todo.recurring_interval}`}
                            >
                                &#x21bb; {todo.recurring_interval}
                            </span>
                        )}
                    </div>

                    {/* Description */}
                    {todo.description && (
                        <p className={`text-sm mt-1 ${todo.completed ? "text-gray-400" : "text-gray-600"}`}>
                            {todo.description}
                        </p>
                    )}

                    {/* Due Date */}
                    {todo.due_date && !todo.completed && (
                        <p className={`text-sm mt-1 ${formatDueDate(todo.due_date).className}`}>
                            {formatDueDate(todo.due_date).text}
                        </p>
                    )}
                    {todo.due_date && todo.completed && (
                        <p className="text-sm mt-1 text-gray-400">
                            Due: {new Date(todo.due_date).toLocaleDateString()}
                        </p>
                    )}

                    {/* Tags */}
                    {todo.tags && todo.tags.length > 0 && (
                        <div className="flex flex-wrap mt-2 gap-1">
                            {todo.tags.map(tag => (
                                <span
                                    key={tag}
                                    className="text-xs bg-indigo-100 text-indigo-700 rounded-full px-3 py-1 font-medium"
                                >
                                    #{tag}
                                </span>
                            ))}
                        </div>
                    )}
                </div>
            </div>
            <div className="flex items-center ml-4">
                <button
                    onClick={openModal}
                    className="px-3 py-1 bg-blue-500 text-white rounded-lg shadow-sm hover:bg-blue-600 transition-colors mr-2"
                >
                    Edit
                </button>
                <button
                    onClick={() => onDelete(todo.id)}
                    className="px-3 py-1 bg-red-500 text-white rounded-lg shadow-sm hover:bg-red-600 transition-colors"
                >
                    Delete
                </button>
            </div>
            <Modal
                isOpen={isModalOpen}
                onRequestClose={closeModal}
                contentLabel="Edit Todo"
                className="bg-white p-8 rounded-lg shadow-2xl w-full max-w-md"
                overlayClassName="fixed inset-0 bg-black bg-opacity-60 flex justify-center items-center"
            >
                <EditTodoForm todo={todo} onUpdate={onUpdate} onClose={closeModal} />
            </Modal>
        </div>
    );
}





