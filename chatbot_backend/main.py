from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from chatbot_backend.agent import get_agent
from chatbot_backend.database import engine
from chatbot_backend.models import Conversation, Message
from sqlmodel import Session, select
import datetime
import json

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
    client, tools = agent_parts
    
    with Session(engine) as session:
        # Step 1: Find or create conversation
        if request.conversation_id:
            conversation = session.get(Conversation, request.conversation_id)
            if not conversation or conversation.user_id != user_id:
                return {"error": "Conversation not found or access denied"}
            # Retrieve history
            history_statement = select(Message).where(Message.conversation_id == conversation.id).order_by(Message.created_at)
            history = session.exec(history_statement).all()
        else:
            conversation = Conversation(
                user_id=user_id,
                created_at=str(datetime.datetime.utcnow()),
                updated_at=str(datetime.datetime.utcnow())
            )
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
            history = []

        # Step 2: Store user message
        user_message = Message(
            conversation_id=conversation.id,
            user_id=user_id,
            role="user",
            content=request.message,
            created_at=str(datetime.datetime.utcnow())
        )
        session.add(user_message)
        session.commit()
        
        # Add current message to history for context
        history.append(user_message)
        
        # This is where you would format the history for the agent
        agent_context = ([{"role": msg.role, "content": msg.content} for msg in history])

        # Mocked agent logic starts here
        response_data = None

        # This logic should be replaced by a real agent call that uses agent_context
        if "add task" in request.message.lower():
            title_from_message = request.message.lower().replace("add task", "").strip()
            add_task_tool = next((tool for tool in tools if tool.__name__ == 'add_task'), None)
            if add_task_tool:
                tool_result = add_task_tool(user_id=user_id, title=title_from_message)
                response_data = {
                    "response": f"I've added the task '{title_from_message}'. The ID is {tool_result['task_id']}",
                    "tool_calls": [{"name": "add_task", "result": tool_result}]
                }
        
        if not response_data:
             response_data = {
                "response": "I can do many things! Try asking me to 'add a task'.",
                "tool_calls": []
            }

        # Step 3: Store assistant message
        assistant_message = Message(
            conversation_id=conversation.id,
            user_id="assistant",
            role="assistant",
            content=response_data["response"],
            created_at=str(datetime.datetime.utcnow())
        )
        session.add(assistant_message)
        
        conversation.updated_at = str(datetime.datetime.utcnow())
        session.add(conversation)
        
        session.commit()

        return {
            "conversation_id": conversation.id,
            "response": response_data["response"],
            "tool_calls": response_data["tool_calls"]
        }

@app.get("/")
def read_root():
    return {"Hello": "World"}
