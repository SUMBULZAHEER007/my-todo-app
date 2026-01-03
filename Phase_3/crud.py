from sqlalchemy.orm import Session
import models

def get_todo(db: Session, todo_id: int):
    return db.query(models.TodoDB).filter(models.TodoDB.id == todo_id).first()

def get_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TodoDB).offset(skip).limit(limit).all()

def create_todo(db: Session, todo: models.TodoCreate):
    # Auto-categorize the task based on keywords in the description
    category = categorize_task(todo.description)
    db_todo = models.TodoDB(
        description=todo.description,
        completed=todo.completed,
        category=category
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def categorize_task(description: str) -> str:
    """
    Auto-categorize a task based on keywords in the description.
    """
    desc_lower = description.lower()

    # Define keywords for each category
    work_keywords = ['meeting', 'work', 'project', 'report', 'email', 'presentation', 'client', 'boss', 'deadline', 'task']
    personal_keywords = ['personal', 'family', 'friend', 'shopping', 'grocery', 'dinner', 'lunch', 'appointment', 'doctor']
    urgent_keywords = ['urgent', 'asap', 'immediately', 'today', 'now', 'critical', 'important', 'deadline', 'crucial']

    # Check for urgent first
    for keyword in urgent_keywords:
        if keyword in desc_lower:
            return 'Urgent'

    # Then check for work
    for keyword in work_keywords:
        if keyword in desc_lower:
            return 'Work'

    # Then check for personal
    for keyword in personal_keywords:
        if keyword in desc_lower:
            return 'Personal'

    # Default to Uncategorized if no keywords match
    return 'Uncategorized'

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