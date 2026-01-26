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

export default function TodoItem({ todo, onToggle, onDelete, onUpdate }: TodoItemProps) {
    const [isModalOpen, setIsModalOpen] = useState(false);

    const openModal = () => setIsModalOpen(true);
    const closeModal = () => setIsModalOpen(false);

    const priorityColor = {
        High: "border-red-500",
        Medium: "border-yellow-500",
        Low: "border-green-500",
    }[todo.priority || "Medium"];

    return (
        <div className={`p-4 mb-4 border-l-4 ${priorityColor} bg-white rounded-lg shadow-md flex justify-between items-center transition-transform transform hover:scale-105 ${todo.completed ? "opacity-50" : ""}`}>
            <div className="flex items-center">
                <input
                    type="checkbox"
                    checked={todo.completed}
                    onChange={(e) => onToggle(todo.id, e.target.checked)}
                    className="h-6 w-6 rounded-full border-gray-300 text-indigo-600 focus:ring-indigo-500"
                />
                <div className="ml-4">
                    <h3 className={`text-lg font-bold ${todo.completed ? "line-through" : ""}`}>
                        {todo.title}
                        {todo.recurring_interval && <span className="ml-2" title={`Recurs ${todo.recurring_interval}`}>&#x21bb;</span>}
                    </h3>
                    {todo.description && <p className="text-sm text-gray-600">{todo.description}</p>}
                    {todo.due_date && <p className="text-sm text-gray-500">Due: {new Date(todo.due_date).toLocaleDateString()}</p>}
                    <div className="flex flex-wrap mt-2">
                        {todo.tags?.map(tag => (
                            <span key={tag} className="text-xs bg-gray-200 text-gray-800 rounded-full px-3 py-1 mr-2 mt-1">{tag}</span>
                        ))}
                    </div>
                </div>
            </div>
            <div className="flex items-center">
                <button onClick={openModal} className="px-3 py-1 bg-blue-500 text-white rounded-lg shadow-sm hover:bg-blue-600 transition-colors mr-2">
                    Edit
                </button>
                <button onClick={() => onDelete(todo.id)} className="px-3 py-1 bg-red-500 text-white rounded-lg shadow-sm hover:bg-red-600 transition-colors">
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





