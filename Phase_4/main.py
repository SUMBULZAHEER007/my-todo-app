import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import uvicorn
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles

# Local files imports
import database
import models
import crud
from ai_interface import get_ai_model
from rag import RAGService

# Environment variables load karein (.env file se)
load_dotenv()

# Database tables create karna (Phase II)
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Todo AI Agent", version="1.0.0")

# Add CORS middleware to allow frontend-backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Dependency: Database session management
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pre-initialize services for better performance
rag_service = RAGService()

# -------------------------------
# Home Route
# -------------------------------
@app.get("/")
def read_root():
    from fastapi.responses import HTMLResponse
    with open("static/index.html") as f:
        content = f.read()
    return HTMLResponse(content=content)

# -------------------------------
# Phase II: CRUD Endpoints
# -------------------------------

@app.post("/todos", response_model=models.TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(todo: models.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db=db, todo=todo)

@app.get("/todos", response_model=List[models.TodoResponse])
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_todos(db, skip=skip, limit=limit)

@app.get("/todos/{todo_id}", response_model=models.TodoResponse)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.get_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@app.put("/todos/{todo_id}", response_model=models.TodoResponse)
def update_todo(todo_id: int, todo: models.TodoUpdate, db: Session = Depends(get_db)):
    db_todo = crud.update_todo(db, todo_id=todo_id, todo_update=todo)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    success = crud.delete_todo(db, todo_id=todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"detail": "Todo deleted successfully"}

# -------------------------------
# Phase III: AI & RAG Endpoints
# -------------------------------

@app.post("/api/chat")
def chat_with_ai(query: str, selected_text: str = "", db: Session = Depends(get_db)):
    try:
        ai_model = get_ai_model()

        # 1. Database se context build karein
        task_context = rag_service.create_context_from_todos(db)

        # 2. Similarity search agar user ne specific text select kiya ho
        similar_context = ""
        if selected_text.strip():
            rag_service.build_vector_store(db)
            similar_tasks = rag_service.search_similar_tasks(selected_text)
            if similar_tasks:
                similar_context = "\nSpecifically relevant to your selection:\n"
                for task in similar_tasks:
                    similar_context += f"- {task['content']}\n"

        # 3. Final Prompt for Hugging Face
        prompt = f"System: You are a helpful Todo Assistant. Use the context below to answer.\n\nContext:\n{task_context}\n{similar_context}\n\nUser Question: {query}\nAssistant:"

        response = ai_model.generate_response(prompt)
        return {"response": response}

    except Exception as e:
        print(f"Chat endpoint error: {str(e)}")  # Log the error for debugging
        return {"response": f"AI is thinking... please try again later."}

@app.post("/api/tasks/summary")
def get_task_summary(db: Session = Depends(get_db)):
    try:
        ai_model = get_ai_model()
        full_context = rag_service.create_context_from_todos(db)

        # Create a more specific prompt for a 2-sentence summary
        prompt = f"System: Write exactly 2 sentences summarizing the following tasks. Be concise and professional.\n\nTasks:\n{full_context}\n\nSummary:"
        response = ai_model.generate_response(prompt)

        # Ensure the response contains exactly 2 sentences as per specification
        sentences = response.split('.')
        if len(sentences) >= 2:
            # Take the first two sentences and join them back
            response = '.'.join(sentences[:2]) + '.'
        else:
            # If there's only one sentence, keep it as is
            response = sentences[0] + '.' if sentences[0] else "Your task list is up to date."

        return {"summary": response}
    except Exception as e:
        print(f"Task summary endpoint error: {str(e)}")  # Log the error for debugging
        return {"summary": "AI is thinking... Please try again later."}

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)