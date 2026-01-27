from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from chatbot_backend.agent import get_agent, client
from chatbot_backend.database import engine
from chatbot_backend.models import Conversation, Message
from sqlmodel import Session, select
import datetime
import json
import time
from openai.types.beta.threads.runs import ToolCall
from chatbot_backend.tools.task_tools import add_task, list_tasks, complete_task, update_task, delete_task

app = FastAPI()

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": f"An unexpected error occurred: {exc}"},
    )

class ChatRequest(BaseModel):
    message: str
    conversation_id: int | None = None

@app.post("/api/{user_id}/chat")
async def chat(user_id: str, request: ChatRequest, agent_parts = Depends(get_agent)):
    client_openai, assistant = agent_parts # Renamed client to client_openai to avoid conflict with local 'client' variable
    
    with Session(engine) as session:
        # Step 1: Find or create conversation and thread
        if request.conversation_id:
            conversation = session.get(Conversation, request.conversation_id)
            if not conversation or conversation.user_id != user_id:
                return {"error": "Conversation not found or access denied"}
            
            if not conversation.thread_id:
                # If conversation exists but no thread_id, create one
                thread = client_openai.beta.threads.create()
                conversation.thread_id = thread.id
                session.add(conversation)
                session.commit()
                session.refresh(conversation)
            else:
                thread = client_openai.beta.threads.retrieve(conversation.thread_id)
        else:
            # New conversation, create new thread
            thread = client_openai.beta.threads.create()
            conversation = Conversation(
                user_id=user_id,
                thread_id=thread.id,
                created_at=str(datetime.datetime.utcnow()),
                updated_at=str(datetime.datetime.utcnow())
            )
            session.add(conversation)
            session.commit()
            session.refresh(conversation)

        # Step 2: Add user message to the thread
        client_openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=request.message,
        )
        
        # Store user message in DB
        user_message_db = Message(
            conversation_id=conversation.id,
            user_id=user_id,
            role="user",
            content=request.message,
            created_at=str(datetime.datetime.utcnow())
        )
        session.add(user_message_db)
        session.commit()

        # Step 3: Run the assistant
        run = client_openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )

        # Step 4: Poll for run status and handle tool calls
        tool_outputs = []
        while run.status in ['queued', 'in_progress', 'cancelling', 'requires_action']:
            time.sleep(0.5)
            run = client_openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            
            if run.status == 'requires_action':
                for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    # Dynamically call the tool function
                    # Ensure user_id is passed if tool expects it
                    if 'user_id' in function_args:
                        function_args['user_id'] = user_id

                    tool_response = ""
                    try:
                        # Map tool names to actual functions
                        if function_name == "add_task":
                            tool_response = add_task(**function_args)
                        elif function_name == "list_tasks":
                            tool_response = list_tasks(**function_args)
                        elif function_name == "complete_task":
                            tool_response = complete_task(**function_args)
                        elif function_name == "update_task":
                            tool_response = update_task(**function_args)
                        elif function_name == "delete_task":
                            tool_response = delete_task(**function_args)
                        else:
                            tool_response = {"error": f"Unknown tool: {function_name}"}
                            
                        tool_outputs.append({
                            "tool_call_id": tool_call.id,
                            "output": json.dumps(tool_response)
                        })
                    except Exception as e:
                        tool_outputs.append({
                            "tool_call_id": tool_call.id,
                            "output": json.dumps({"error": str(e)})
                        })
                
                # Submit tool outputs
                client_openai.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
                tool_outputs = [] # Clear outputs after submission

        # Step 5: Retrieve the assistant's response
        messages = client_openai.beta.threads.messages.list(thread_id=thread.id, order="desc", limit=1)
        assistant_response_content = "No response from assistant."
        for message in messages.data:
            if message.role == "assistant":
                for content_block in message.content:
                    if content_block.type == "text":
                        assistant_response_content = content_block.text.value
                        break
                if assistant_response_content != "No response from assistant.":
                    break
        
        # Store assistant message in DB
        assistant_message_db = Message(
            conversation_id=conversation.id,
            user_id="assistant",
            role="assistant",
            content=assistant_response_content,
            created_at=str(datetime.datetime.utcnow())
        )
        session.add(assistant_message_db)
        
        conversation.updated_at = str(datetime.datetime.utcnow())
        session.add(conversation)
        
        session.commit()

        return {
            "conversation_id": conversation.id,
            "response": assistant_response_content,
            "thread_id": thread.id
        }

@app.get("/")
def read_root():
    return {"Hello": "World"}
