"use client";

import { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { Todo } from "../services/todoAPI";

interface TodoFormProps {
    onAdd: (todo: Omit<Todo, 'id' | 'completed'>) => void;
}

// Priority option styles for visual indication
const priorityStyles: Record<string, string> = {
    High: "text-red-600",
    Medium: "text-yellow-600",
    Low: "text-green-600",
};

export default function TodoForm({ onAdd }: TodoFormProps) {
    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [priority, setPriority] = useState("Medium");
    const [tags, setTags] = useState("");
    const [dueDate, setDueDate] = useState<Date | null>(null);
    const [recurringInterval, setRecurringInterval] = useState("");

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!title.trim()) return;
        const tagsArray = tags.split(",").map(tag => tag.trim()).filter(tag => tag);
        onAdd({ title, description, priority, tags: tagsArray, due_date: dueDate?.toISOString(), recurring_interval: recurringInterval });
        setTitle("");
        setDescription("");
        setPriority("Medium");
        setTags("");
        setDueDate(null);
        setRecurringInterval("");
    };

    // Get color indicator for priority
    const getPriorityIndicator = (p: string) => {
        const colors: Record<string, string> = {
            High: "bg-red-500",
            Medium: "bg-yellow-500",
            Low: "bg-green-500",
        };
        return colors[p] || colors.Medium;
    };

    return (
        <form onSubmit={handleSubmit} className="mb-6 p-6 bg-gray-50 rounded-lg shadow-md">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Title */}
                <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-1">Title *</label>
                    <input
                        type="text"
                        placeholder="What needs to be done?"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        className="w-full p-3 border rounded-lg shadow-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                        required
                    />
                </div>

                {/* Description */}
                <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                    <textarea
                        placeholder="Add more details..."
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        className="w-full p-3 border rounded-lg shadow-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                        rows={2}
                    ></textarea>
                </div>

                {/* Priority */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Priority</label>
                    <div className="relative">
                        <span className={`absolute left-3 top-1/2 transform -translate-y-1/2 w-3 h-3 rounded-full ${getPriorityIndicator(priority)}`}></span>
                        <select
                            value={priority}
                            onChange={(e) => setPriority(e.target.value)}
                            className="w-full p-3 pl-8 border rounded-lg shadow-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 appearance-none bg-white"
                        >
                            <option value="High">High Priority</option>
                            <option value="Medium">Medium Priority</option>
                            <option value="Low">Low Priority</option>
                        </select>
                    </div>
                </div>

                {/* Tags */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Tags</label>
                    <input
                        type="text"
                        placeholder="work, personal, urgent (comma-separated)"
                        value={tags}
                        onChange={(e) => setTags(e.target.value)}
                        className="w-full p-3 border rounded-lg shadow-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
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
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Due Date</label>
                    <DatePicker
                        selected={dueDate}
                        onChange={(date) => setDueDate(date)}
                        placeholderText="Select due date"
                        className="w-full p-3 border rounded-lg shadow-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                        dateFormat="MMMM d, yyyy"
                        minDate={new Date()}
                        isClearable
                    />
                </div>

                {/* Recurring Interval */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Repeat</label>
                    <select
                        value={recurringInterval}
                        onChange={(e) => setRecurringInterval(e.target.value)}
                        className="w-full p-3 border rounded-lg shadow-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                    >
                        <option value="">Does not repeat</option>
                        <option value="daily">Daily</option>
                        <option value="weekly">Weekly</option>
                        <option value="monthly">Monthly</option>
                    </select>
                </div>
            </div>
            <button
                type="submit"
                className="mt-4 w-full px-4 py-3 bg-indigo-600 text-white rounded-lg shadow-md hover:bg-indigo-700 transition-colors font-medium"
            >
                Add Todo
            </button>
        </form>
    );
}


