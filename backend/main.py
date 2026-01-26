from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import Todo, TodoCreate, TodoUpdate
from .services.todo_service import TodoService

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

todo_service = TodoService()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/todos", response_model=List[Todo])
def get_todos(search: Optional[str] = None, status: Optional[str] = None, priority: Optional[str] = None, sort: Optional[str] = None):
    return todo_service.get_all(search=search, filter_by_status=status, filter_by_priority=priority, sort_by=sort)

@app.post("/todos", response_model=Todo)
def create_todo(todo: TodoCreate):
    return todo_service.create(todo)

@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    todo = todo_service.get_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo_update: TodoUpdate):
    todo = todo_service.get_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo_service.update(todo_id, todo_update)

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    todo = todo_service.get_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_service.delete(todo_id)
    return {"message": "Todo deleted successfully"}
