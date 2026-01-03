import os
import sys
from pathlib import Path

# Add the current directory to the Python path to handle imports when running from root
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import uvicorn
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

# Local files imports
from . import database
from . import models
from . import crud
from .ai_interface import get_ai_model
from . import rag_service

load_dotenv()

# Database tables create karna
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Sumbul Zaheer - Phase 2 AI Todo", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Render ke liye path fix (Phase_2 folder ko handle karne ke liye)
static_dir = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(static_dir, "static")

if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/", response_class=HTMLResponse)
def read_root():
    index_file = os.path.join(static_path, "index.html")
    if os.path.exists(index_file):
        with open(index_file) as f:
            return f.read()
    return "<h1>Phase 2 API is running. index.html not found in static folder.</h1>"

# --- Phase I: CRUD Endpoints ---

@app.post("/todos", response_model=models.TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(todo: models.TodoCreate, db: Session = Depends(database.get_db if hasattr(database, 'get_db') else lambda: database.SessionLocal())):
    db_session = database.SessionLocal()
    try:
        return crud.create_todo(db=db_session, todo=todo)
    finally:
        db_session.close()

@app.get("/todos", response_model=List[models.TodoResponse])
def read_todos(skip: int = 0, limit: int = 100):
    db = database.SessionLocal()
    try:
        return crud.get_todos(db, skip=skip, limit=limit)
    finally:
        db.close()

# --- Phase II: AI Summary Endpoint ---

@app.post("/api/tasks/summary")
def get_task_summary():
    db = database.SessionLocal()
    try:
        ai_model = get_ai_model()
        # rag_service ab sahi kaam karega kyunke import upar add kar diya hai
        full_context = rag_service.create_context_from_todos(db)

        prompt = f"System: Provide a clear, 2-sentence overview of the following todo list and suggest the next best action.\n\nTasks:\n{full_context}\n\nSummary:"
        response = ai_model.generate_response(prompt)
        return {"summary": response}
    except Exception as e:
        print(f"Task summary error: {str(e)}")
        return {"summary": "AI is setting up... Please add a task and try again."}
    finally:
        db.close()

if __name__ == "__main__":
    import os
    # Railway ya Render se port uthayen, warna default 8000
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("Phase_2.main:app", host="0.0.0.0", port=port)