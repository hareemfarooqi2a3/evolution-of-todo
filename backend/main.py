from typing import List, Optional
from datetime import timedelta # Added for token expiration
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from .models import Todo, TodoCreate, TodoUpdate, User, UserCreate, Token
from .services.todo_service import TodoService
from .db import get_db_session
from .security import create_access_token, get_password_hash, verify_password, oauth2_scheme

# Dapr Imports
from dapr.clients import DaprClient
import os
import json

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Dapr Client Initialization
dapr_client = DaprClient()
PUBSUB_NAME = os.getenv("DAPR_PUBSUB_NAME", "pubsub") # Default pubsub component name
TODO_EVENTS_TOPIC = os.getenv("DAPR_TODO_EVENTS_TOPIC", "todo-events")


# --- Authentication Endpoints ---
@app.post("/register", response_model=User)
def register_user(user_create: UserCreate, session: Session = Depends(get_db_session)):
    user_exists = session.exec(select(User).where(User.username == user_create.username)).first()
    if user_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    
    hashed_password = get_password_hash(user_create.password)
    user = User(username=user_create.username, hashed_password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db_session)):
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/todos", response_model=List[Todo])
def get_todos(
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_db_session),
    search: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    sort: Optional[str] = None
):
    todo_service = TodoService(session, dapr_client, PUBSUB_NAME, TODO_EVENTS_TOPIC)
    return todo_service.get_all(
        user_id=current_user.id,
        search=search,
        filter_by_status=status,
        filter_by_priority=priority,
        sort_by=sort
    )

@app.post("/todos", response_model=Todo)
def create_todo(
    todo_create: TodoCreate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_db_session)
):
    todo_service = TodoService(session, dapr_client, PUBSUB_NAME, TODO_EVENTS_TOPIC)
    return todo_service.create(todo_create, user_id=current_user.id)

@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(
    todo_id: int,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_db_session)
):
    todo_service = TodoService(session, dapr_client, PUBSUB_NAME, TODO_EVENTS_TOPIC)
    todo = todo_service.get_by_id(todo_id, user_id=current_user.id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_db_session)
):
    todo_service = TodoService(session, dapr_client, PUBSUB_NAME, TODO_EVENTS_TOPIC)
    todo = todo_service.update(todo_id, todo_update, user_id=current_user.id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo

@app.delete("/todos/{todo_id}")
def delete_todo(
    todo_id: int,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_db_session)
):
    todo_service = TodoService(session, dapr_client, PUBSUB_NAME, TODO_EVENTS_TOPIC)
    if not todo_service.delete(todo_id, user_id=current_user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return {"message": "Todo deleted successfully"}

