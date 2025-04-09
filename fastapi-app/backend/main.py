from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Enable CORS for all domains (only for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory DB simulation
tasks = []
current_id = 1

class Task(BaseModel):
    id: int
    title: str
    completed: bool = False

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    global current_id
    task.id = current_id
    current_id += 1
    tasks.append(task)
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    for i, task in enumerate(tasks):
        if task.id == task_id:
            tasks[i] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks
    tasks = [task for task in tasks if task.id != task_id]
    return {"message": "Task deleted"}
