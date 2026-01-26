"use client";

import { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { Todo } from "../services/todoAPI";

interface EditTodoFormProps {
    todo: Todo;
    onUpdate: (id: number, todo: Partial<Omit<Todo, 'id'>>) => void;
    onClose: () => void;
}

export default function EditTodoForm({ todo, onUpdate, onClose }: EditTodoFormProps) {
    const [title, setTitle] = useState(todo.title);
    const [description, setDescription] = useState(todo.description || "");
    const [priority, setPriority] = useState(todo.priority || "Medium");
    const [tags, setTags] = useState(todo.tags?.join(", ") || "");
    const [dueDate, setDueDate] = useState<Date | null>(todo.due_date ? new Date(todo.due_date) : null);
    const [recurringInterval, setRecurringInterval] = useState(todo.recurring_interval || "");

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!title.trim()) return;
        const tagsArray = tags.split(",").map(tag => tag.trim()).filter(tag => tag);
        onUpdate(todo.id, { title, description, priority, tags: tagsArray, due_date: dueDate?.toISOString(), recurring_interval: recurringInterval });
        onClose();
    };

    return (
        <form onSubmit={handleSubmit}>
            <div className="mb-2">
                <input
                    type="text"
                    placeholder="Title"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    className="w-full p-2 border rounded"
                />
            </div>
            <div className="mb-2">
                <textarea
                    placeholder="Description"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    className="w-full p-2 border rounded"
                ></textarea>
            </div>
            <div className="mb-2">
                <select value={priority} onChange={(e) => setPriority(e.target.value)} className="w-full p-2 border rounded">
                    <option value="High">High</option>
                    <option value="Medium">Medium</option>
                    <option value="Low">Low</option>
                </select>
            </div>
            <div className="mb-2">
                <input
                    type="text"
                    placeholder="Tags (comma-separated)"
                    value={tags}
                    onChange={(e) => setTags(e.target.value)}
                    className="w-full p-2 border rounded"
                />
            </div>
            <div className="mb-2">
                <DatePicker
                    selected={dueDate}
                    onChange={(date) => setDueDate(date)}
                    placeholderText="Due Date"
                    className="w-full p-2 border rounded"
                />
            </div>
            <div className="mb-2">
                <select value={recurringInterval} onChange={(e) => setRecurringInterval(e.target.value)} className="w-full p-2 border rounded">
                    <option value="">Not Recurring</option>
                    <option value="daily">Daily</option>
                    <option value="weekly">Weekly</option>
                    <option value="monthly">Monthly</option>
                </select>
            </div>
            <div className="flex justify-end">
                <button type="button" onClick={onClose} className="px-4 py-2 mr-2 bg-gray-300 text-black rounded">
                    Cancel
                </button>
                <button type="submit" className="px-4 py-2 bg-blue-500 text-white rounded">
                    Update
                </button>
            </div>
        </form>
    );
}
