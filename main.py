from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uuid
import requests
import json


app = FastAPI()

#model_path = r"C:\Users\Kyle\AppData\Local\nomic.ai\GPT4All\Meta-Llama-3-8B-Instruct.Q4_0.gguf"

OLLAMA_API_URL = "http://localhost:11434/api/generate"

# Task model
class Task(BaseModel):
    id: str
    title: str
    priority: str  # "high", "medium", "low"
    deadline: str  # Fix typo from 'dealine'
    duration: int  # Estimated time in hours
    completed: bool = False  # Default to False

# In-memory database
tasks_db = []

# Create a new task
@app.post("/add_task")
async def add_task(task: Task):
    tasks_db.append(task)
    return {"message": "Task added successfully", "task": task}

# Get all tasks
@app.get("/get_tasks", response_model=List[Task])
async def get_tasks():
    return tasks_db

# Delete a task
@app.delete("/delete_task/{task_id}")
async def delete_task(task_id: str):
    for task in tasks_db:
        if task.id == task_id:
            tasks_db.remove(task)
            return {"message": "Task deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Task not found")

# AI schedule recommendation
@app.post("/get_schedule")  # FIXED: Added missing "/"
async def get_schedule():
    prompt = """I have the following tasks to complete today:\n"""

    for task in tasks_db:
        prompt += f"Id is {task.id}, Title is {task.title}, Priority is {task.priority}, Deadline is {task.deadline}, Duration is {task.duration} hours, Completed is {task.completed}\n"

    prompt += """
        Based on efficiency, dependencies, and time of day, recommend the best order to complete these tasks. 
        Respond **only** in valid JSON format with an ordered list of tasks and a brief reason for each order.
        Example format:
        {{
            "recommended_order": [
                {{"task": "Task Name", "reason": "Reason for choosing this order"}},
                {{"task": "Task Name", "reason": "Reason for choosing this order"}}
            ]
        }}
        """
    
    payload = {
        "model": "llama3.2",
        "prompt": prompt,
        "format": "json",
        "stream": False
    }

    

    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error contacting Ollama API: {str(e)}")
    
    return response.json()
    

    
    
    
    
    
    
    
    

    

