from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Relative dots (.) hata diye hain taake direct run ho sake
import database
import models
import crud
from ai_interface import get_ai_model
from rag import RAGService

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Todo API with AI", version="1.0.0")

# Dependency to get database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------
# Phase II endpoints
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

@app.patch("/todos/{todo_id}", response_model=models.TodoResponse)
def patch_todo(todo_id: int, todo: models.TodoUpdate, db: Session = Depends(get_db)):
    db_todo = crud.update_todo(db, todo_id=todo_id, todo_update=todo)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    success = crud.delete_todo(db, todo_id=todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"detail": "Todo deleted successfully"}


# -------------------------------
# Phase III AI / RAG endpoints
# -------------------------------

@app.post("/api/chat")
def chat_with_ai(query: str, selected_text: str = "", db: Session = Depends(get_db)):
    try:
        ai_model = get_ai_model()
        rag_service = RAGService()
        task_context = rag_service.create_context_from_todos(db)

        similar_context = ""
        if selected_text.strip():
            rag_service.build_vector_store(db)
            similar_tasks = rag_service.search_similar_tasks(selected_text)
            if similar_tasks:
                similar_context = "Relevant tasks based on your selected text:\n"
                for task in similar_tasks:
                    similar_context += f"- {task['content']}\n"

        prompt = f"""
        Context from tasks:
        {task_context}

        {similar_context}

        User query: {query}

        Please provide a helpful response based on the context and query.
        """

        response = ai_model.generate_response(prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")


@app.post("/api/tasks/summary")
def get_task_summary(db: Session = Depends(get_db)):
    try:
        ai_model = get_ai_model()
        rag_service = RAGService()
        full_context = rag_service.create_context_from_todos(db)

        prompt = f"""
        Please provide a concise summary of the following tasks:

        {full_context}

        Focus on the main themes, progress, and any recommendations.
        """

        response = ai_model.generate_response(prompt)
        return {"summary": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")


# Main execution
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)