from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uvicorn
from fastapi.staticfiles import StaticFiles

# Local files imports
import database
import models
import crud

# Database tables create karna (Phase II)
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Todo App - Phase 1", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Dependency: Database session management
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
# Phase 1: CRUD Endpoints
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

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)