# chatbot_backend/mcp_server.py

# Handle imports for both running from within directory and as a package
try:
    from chatbot_backend.tools.task_tools import add_task, list_tasks, complete_task, update_task, delete_task
except ImportError:
    from tools.task_tools import add_task, list_tasks, complete_task, update_task, delete_task

def get_mcp_tools():
    """
    Returns a list of MCP tools for the agent in OpenAI Assistants API format.
    Note: user_id is automatically injected from the API path, not from tool parameters.
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "add_task",
                "description": "Create a new task for the current user.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "The title of the task."},
                        "description": {"type": "string", "description": "The description of the task (optional)."}
                    },
                    "required": ["title"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_tasks",
                "description": "Retrieve all tasks for the current user, optionally filtering by status.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "enum": ["all", "pending", "completed"], "description": "Filter tasks by status ('all', 'pending', 'completed'). Default is 'all'."}
                    },
                    "required": []
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
                        "task_id": {"type": "integer", "description": "The ID of the task to complete."}
                    },
                    "required": ["task_id"]
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
                        "task_id": {"type": "integer", "description": "The ID of the task to update."},
                        "title": {"type": "string", "description": "The new title of the task (optional)."},
                        "description": {"type": "string", "description": "The new description of the task (optional)."}
                    },
                    "required": ["task_id"]
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
                        "task_id": {"type": "integer", "description": "The ID of the task to delete."}
                    },
                    "required": ["task_id"]
                }
            }
        }
    ]
