from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import models
import crud
from database import engine, get_db
from schemas import TaskCreate, TaskUpdate, TaskResponse

# Create database tables if they do not exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API")

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def home():
    return {"message": "Task Manager API is running"}


# Add task
@app.post("/tasks", response_model=TaskResponse)
def add_task(task: TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, task)


# Get all tasks
@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return crud.get_all_tasks(db)


# Get task by ID
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


# Update task
@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db)
):
    updated_task = crud.update_task(db, task_id, task)

    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return updated_task


# Delete task
@app.delete("/tasks/{task_id}")
def remove_task(task_id: int, db: Session = Depends(get_db)):
    deleted_task = crud.delete_task(db, task_id)

    if deleted_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted successfully"}


# Complete task
@app.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
def mark_completed(task_id: int, db: Session = Depends(get_db)):
    task = crud.complete_task(db, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task