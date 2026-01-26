# chatbot_backend/agent.py

import os
from openai import OpenAI
from chatbot_backend.mcp_server import get_mcp_tools
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_agent():
    # This is a simplified representation.
    # In a real scenario, you might have a more complex agent setup.
    # The "tools" would be formatted in the way the OpenAI Assistants API expects.
    tools = get_mcp_tools()
    # For now, we are just returning the client and the tools
    # The actual agent execution will be in the main.py
    return client, tools

print("OpenAI Agent setup initialized.")
