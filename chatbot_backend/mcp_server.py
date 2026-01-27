# chatbot_backend/mcp_server.py

from chatbot_backend.tools.task_tools import add_task, list_tasks, complete_task, update_task, delete_task

def get_mcp_tools():
    """
    Returns a list of MCP tools for the agent in OpenAI Assistants API format.
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "add_task",
                "description": "Create a new task for a user.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The ID of the user."},
                        "title": {"type": "string", "description": "The title of the task."},
                        "description": {"type": "string", "description": "The description of the task."}
                    },
                    "required": ["user_id", "title"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_tasks",
                "description": "Retrieve tasks for a user, optionally filtering by status.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The ID of the user."},
                        "status": {"type": "string", "enum": ["all", "pending", "completed"], "description": "Filter tasks by status ('all', 'pending', 'completed'). Default is 'all'."}
                    },
                    "required": ["user_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "complete_task",
                "description": "Mark a task as complete.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The ID of the user."},
                        "task_id": {"type": "integer", "description": "The ID of the task to complete."}
                    },
                    "required": ["user_id", "task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "update_task",
                "description": "Update a task's title or description.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The ID of the user."},
                        "task_id": {"type": "integer", "description": "The ID of the task to update."},
                        "title": {"type": "string", "description": "The new title of the task."},
                        "description": {"type": "string", "description": "The new description of the task."}
                    },
                    "required": ["user_id", "task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "delete_task",
                "description": "Delete a task.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The ID of the user."},
                        "task_id": {"type": "integer", "description": "The ID of the task to delete."}
                    },
                    "required": ["user_id", "task_id"]
                }
            }
        }
    ]
