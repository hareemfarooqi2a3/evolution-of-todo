# chatbot_backend/agent.py

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Handle imports for both running from within directory and as a package
try:
    from chatbot_backend.mcp_server import get_mcp_tools
except ImportError:
    from mcp_server import get_mcp_tools

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Store assistant_id globally to avoid recreating it
assistant_id = None 

def create_or_retrieve_assistant():
    global assistant_id
    if assistant_id:
        print(f"Using existing assistant with ID: {assistant_id}")
        return client.beta.assistants.retrieve(assistant_id)
    
    # Define the capabilities and instructions for the assistant
    assistant_instructions = """
    You are an AI-powered Todo List assistant. Your primary goal is to help users manage their tasks.
    You can:
    - Add new tasks (add_task)
    - List existing tasks (list_tasks)
    - Complete tasks (complete_task)
    - Update tasks (update_task)
    - Delete tasks (delete_task)

    Always respond concisely and directly to the user's request.
    When creating or updating a task, confirm the action taken.
    When listing tasks, present them clearly.
    If a task ID is needed and not provided, ask for it.
    Always prioritize using the available tools to fulfill the user's request.
    If a task involves a date or time, try to extract it from the user's request.
    """
    
    # Get the tools in the format expected by the Assistants API
    tools = get_mcp_tools()
    
    # Check if an assistant with the desired name already exists
    # This avoids creating multiple assistants during development
    existing_assistants = client.beta.assistants.list(limit=100)
    for existing_assistant in existing_assistants.data:
        if existing_assistant.name == "Todo List Assistant":
            print(f"Found existing assistant: {existing_assistant.id}")
            assistant_id = existing_assistant.id
            return existing_assistant
            
    # Create the assistant if it doesn't exist
    assistant = client.beta.assistants.create(
        name="Todo List Assistant",
        instructions=assistant_instructions,
        model="gpt-4o", # Using a capable model
        tools=tools,
    )
    assistant_id = assistant.id
    print(f"Created new assistant with ID: {assistant.id}")
    return assistant

def get_agent():
    # This function now acts as a dependency that provides the client and the configured assistant
    assistant = create_or_retrieve_assistant()
    return client, assistant

print("OpenAI Agent setup initialized.")
