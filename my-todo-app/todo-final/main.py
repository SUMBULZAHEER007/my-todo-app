from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .database import SessionLocal, engine
from . import models, crud
from .ai_interface import get_ai_model
from .rag import RAGService

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo API with AI", version="1.0.0")

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/todos", response_model=models.TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(todo: models.TodoCreate, db: Session = Depends(get_db)):
    """
    Create a new todo
    """
    return crud.create_todo(db=db, todo=todo)


@app.get("/todos", response_model=List[models.TodoResponse])
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve todos
    """
    todos = crud.get_todos(db, skip=skip, limit=limit)
    return todos


@app.get("/todos/{todo_id}", response_model=models.TodoResponse)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    """
    Get a specific todo by ID
    """
    db_todo = crud.get_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@app.put("/todos/{todo_id}", response_model=models.TodoResponse)
def update_todo(todo_id: int, todo: models.TodoUpdate, db: Session = Depends(get_db)):
    """
    Update a specific todo
    """
    db_todo = crud.update_todo(db, todo_id=todo_id, todo_update=todo)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@app.patch("/todos/{todo_id}", response_model=models.TodoResponse)
def patch_todo(todo_id: int, todo: models.TodoUpdate, db: Session = Depends(get_db)):
    """
    Update todo completion status
    """
    db_todo = crud.update_todo(db, todo_id=todo_id, todo_update=todo)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """
    Delete a specific todo
    """
    success = crud.delete_todo(db, todo_id=todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"detail": "Todo deleted successfully"}


# AI-based endpoints
@app.post("/api/chat")
def chat_with_ai(query: str, selected_text: str = "", db: Session = Depends(get_db)):
    """
    Chat endpoint for AI queries with optional selected text
    """
    try:
        # Get the AI model
        ai_model = get_ai_model()

        # Create context from existing todos
        rag_service = RAGService()
        task_context = rag_service.create_context_from_todos(db)

        # If selected text is provided, search for similar tasks
        similar_context = ""
        if selected_text.strip():
            rag_service.build_vector_store(db)  # Build vector store for similarity search
            similar_tasks = rag_service.search_similar_tasks(selected_text)
            if similar_tasks:
                similar_context = "Relevant tasks based on your selected text:\n"
                for task in similar_tasks:
                    similar_context += f"- {task['content']}\n"

        # Create prompt for chat
        prompt = f"""
        Context from tasks:
        {task_context}

        {similar_context}

        User query: {query}

        Please provide a helpful response based on the context and query.
        """

        # Generate response using AI
        response = ai_model.generate_response(prompt)

        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")


@app.post("/api/tasks/summary")
def get_task_summary(db: Session = Depends(get_db)):
    """
    Generate AI summary of tasks
    """
    try:
        # Get the AI model
        ai_model = get_ai_model()

        # Create context from existing todos
        rag_service = RAGService()
        full_context = rag_service.create_context_from_todos(db)

        # Create prompt for summarization
        prompt = f"""
        Please provide a concise summary of the following tasks:

        {full_context}

        Focus on the main themes, progress, and any recommendations.
        """

        # Generate response using AI
        response = ai_model.generate_response(prompt)

        return {"summary": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")


# For running the application directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)