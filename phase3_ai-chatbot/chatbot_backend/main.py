from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlmodel import Session, select
import datetime
import json
import time

# Handle imports for both running from within directory and as a package
try:
    from chatbot_backend.agent import get_agent, client
    from chatbot_backend.database import engine, init_db
    from chatbot_backend.models import Conversation, Message
    from chatbot_backend.tools.task_tools import add_task, list_tasks, complete_task, update_task, delete_task
except ImportError:
    from agent import get_agent, client
    from database import engine, init_db
    from models import Conversation, Message
    from tools.task_tools import add_task, list_tasks, complete_task, update_task, delete_task

app = FastAPI(title="AI Todo Chatbot API", description="OpenAI Assistants-powered Todo Chatbot")

@app.on_event("startup")
def on_startup():
    init_db()
    print("[INFO] Chatbot database initialized")

# CORS Middleware - Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    client_openai, assistant = agent_parts

    with Session(engine) as session:
        # Step 1: Find or create conversation and thread
        if request.conversation_id:
            conversation = session.get(Conversation, request.conversation_id)
            if not conversation or conversation.user_id != user_id:
                return {"error": "Conversation not found or access denied"}

            if not conversation.thread_id:
                thread = client_openai.beta.threads.create()
                conversation.thread_id = thread.id
                session.add(conversation)
                session.commit()
                session.refresh(conversation)
            else:
                thread = client_openai.beta.threads.retrieve(conversation.thread_id)
        else:
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
        max_polls = 120  # 60 seconds max wait
        poll_count = 0
        while run.status in ['queued', 'in_progress', 'cancelling', 'requires_action']:
            poll_count += 1
            if poll_count > max_polls:
                print(f"[ERROR] Run timed out after {max_polls * 0.5}s. Status: {run.status}")
                break
            time.sleep(0.5)
            run = client_openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            print(f"[DEBUG] Run status: {run.status}")

            if run.status == 'requires_action':
                for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    # Always add user_id to function args (all tools require it)
                    function_args['user_id'] = user_id

                    tool_response = ""
                    try:
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

                client_openai.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
                tool_outputs = []

        # Check if run failed
        if run.status == 'failed':
            error_msg = run.last_error.message if run.last_error else "Unknown error"
            error_code = run.last_error.code if run.last_error else "unknown"
            print(f"[ERROR] Run failed: {error_code} - {error_msg}")
            return {
                "conversation_id": conversation.id,
                "response": f"Assistant error: {error_msg}",
                "thread_id": thread.id
            }
        elif run.status == 'expired':
            print(f"[ERROR] Run expired")
            return {
                "conversation_id": conversation.id,
                "response": "The assistant took too long to respond. Please try again.",
                "thread_id": thread.id
            }

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
