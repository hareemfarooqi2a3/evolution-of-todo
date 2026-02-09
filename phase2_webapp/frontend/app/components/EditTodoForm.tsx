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

// Priority color indicator
const getPriorityIndicator = (p: string) => {
    const colors: Record<string, string> = {
        High: "bg-red-500",
        Medium: "bg-yellow-500",
        Low: "bg-green-500",
    };
    return colors[p] || colors.Medium;
};

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
            <h2 className="text-xl font-bold text-gray-800 mb-4">Edit Todo</h2>

            {/* Title */}
            <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">Title *</label>
                <input
                    type="text"
                    placeholder="What needs to be done?"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                    required
                />
            </div>

            {/* Description */}
            <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                <textarea
                    placeholder="Add more details..."
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                    rows={3}
                ></textarea>
            </div>

            {/* Priority */}
            <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">Priority</label>
                <div className="relative">
                    <span className={`absolute left-3 top-1/2 transform -translate-y-1/2 w-3 h-3 rounded-full ${getPriorityIndicator(priority)}`}></span>
                    <select
                        value={priority}
                        onChange={(e) => setPriority(e.target.value)}
                        className="w-full p-3 pl-8 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 appearance-none bg-white"
                    >
                        <option value="High">High Priority</option>
                        <option value="Medium">Medium Priority</option>
                        <option value="Low">Low Priority</option>
                    </select>
                </div>
            </div>

            {/* Tags */}
            <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">Tags</label>
                <input
                    type="text"
                    placeholder="work, personal, urgent (comma-separated)"
                    value={tags}
                    onChange={(e) => setTags(e.target.value)}
                    className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                />
                {tags && (
                    <div className="flex flex-wrap gap-1 mt-2">
                        {tags.split(",").map(tag => tag.trim()).filter(tag => tag).map((tag, index) => (
                            <span key={index} className="text-xs bg-indigo-100 text-indigo-700 rounded-full px-2 py-0.5">
                                #{tag}
                            </span>
                        ))}
                    </div>
                )}
            </div>

            {/* Due Date */}
            <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">Due Date</label>
                <DatePicker
                    selected={dueDate}
                    onChange={(date) => setDueDate(date)}
                    placeholderText="Select due date"
                    className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                    dateFormat="MMMM d, yyyy"
                    isClearable
                />
            </div>

            {/* Recurring Interval */}
            <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">Repeat</label>
                <select
                    value={recurringInterval}
                    onChange={(e) => setRecurringInterval(e.target.value)}
                    className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                >
                    <option value="">Does not repeat</option>
                    <option value="daily">Daily</option>
                    <option value="weekly">Weekly</option>
                    <option value="monthly">Monthly</option>
                </select>
            </div>

            {/* Action Buttons */}
            <div className="flex justify-end gap-2 mt-6">
                <button
                    type="button"
                    onClick={onClose}
                    className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors font-medium"
                >
                    Cancel
                </button>
                <button
                    type="submit"
                    className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-medium"
                >
                    Update Todo
                </button>
            </div>
        </form>
    );
}
