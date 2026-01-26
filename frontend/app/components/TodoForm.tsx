"use client";

import { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { Todo } from "../services/todoAPI";

interface TodoFormProps {
    onAdd: (todo: Omit<Todo, 'id' | 'completed'>) => void;
}

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

    return (
        <form onSubmit={handleSubmit} className="mb-6 p-6 bg-gray-50 rounded-lg shadow-md">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <input
                    type="text"
                    placeholder="Title"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    className="w-full p-3 border rounded-lg shadow-sm"
                />
                <textarea
                    placeholder="Description"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    className="w-full p-3 border rounded-lg shadow-sm"
                ></textarea>
                <select value={priority} onChange={(e) => setPriority(e.target.value)} className="w-full p-3 border rounded-lg shadow-sm">
                    <option value="High">High</option>
                    <option value="Medium">Medium</option>
                    <option value="Low">Low</option>
                </select>
                <input
                    type="text"
                    placeholder="Tags (comma-separated)"
                    value={tags}
                    onChange={(e) => setTags(e.target.value)}
                    className="w-full p-3 border rounded-lg shadow-sm"
                />
                <DatePicker
                    selected={dueDate}
                    onChange={(date) => setDueDate(date)}
                    placeholderText="Due Date"
                    className="w-full p-3 border rounded-lg shadow-sm"
                />
                <select value={recurringInterval} onChange={(e) => setRecurringInterval(e.target.value)} className="w-full p-3 border rounded-lg shadow-sm">
                    <option value="">Not Recurring</option>
                    <option value="daily">Daily</option>
                    <option value="weekly">Weekly</option>
                    <option value="monthly">Monthly</option>
                </select>
            </div>
            <button type="submit" className="mt-4 w-full px-4 py-3 bg-indigo-600 text-white rounded-lg shadow-md hover:bg-indigo-700 transition-colors">
                Add Todo
            </button>
        </form>
    );
}


