# my_todo_app/repository.py
from sqlalchemy.orm import Session
from .database import TodoDB
from .models import TodoCreate, TodoUpdate
from typing import List, Optional


def get_todo(db: Session, todo_id: int):
    return db.query(TodoDB).filter(TodoDB.id == todo_id).first()


def get_todos(db: Session, skip: int = 0, limit: int = 100) -> List[TodoDB]:
    return db.query(TodoDB).offset(skip).limit(limit).all()


def create_todo(db: Session, todo: TodoCreate):
    db_todo = TodoDB(description=todo.description, completed=todo.completed)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo(db: Session, todo_id: int, todo_update: TodoUpdate):
    db_todo = get_todo(db, todo_id)
    if not db_todo:
        return None
    
    if todo_update.description is not None:
        db_todo.description = todo_update.description
    if todo_update.completed is not None:
        db_todo.completed = todo_update.completed
    
    db_todo.updated_at = db.func.now()
    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int):
    db_todo = get_todo(db, todo_id)
    if not db_todo:
        return False
    
    db.delete(db_todo)
    db.commit()
    return True