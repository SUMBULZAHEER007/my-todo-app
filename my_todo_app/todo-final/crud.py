from sqlalchemy.orm import Session
import models
from ai_interface import get_ai_model

def get_todo(db: Session, todo_id: int):
    return db.query(models.TodoDB).filter(models.TodoDB.id == todo_id).first()

def get_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TodoDB).offset(skip).limit(limit).all()

def create_todo(db: Session, todo: models.TodoCreate):
    # Auto-categorize the task using AI
    ai_model = get_ai_model()
    category = ai_model.categorize_task(todo.description)
    db_todo = models.TodoDB(
        description=todo.description,
        completed=todo.completed,
        category=category
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo(db: Session, todo_id: int, todo_update: models.TodoUpdate):
    db_todo = get_todo(db, todo_id)
    if not db_todo:
        return None

    # .dict() ki jagah .model_dump() use karein (Pydantic V2)
    update_data = todo_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_todo, key, value)

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