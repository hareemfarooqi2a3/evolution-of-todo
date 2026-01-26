# chatbot_backend/mcp_server.py

from chatbot_backend.tools.task_tools import add_task, list_tasks, complete_task, update_task, delete_task

def get_mcp_tools():
    """
    Returns a list of MCP tools for the agent.
    """
    return [add_task, list_tasks, complete_task, update_task, delete_task]
