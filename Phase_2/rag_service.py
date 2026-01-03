from typing import List
from sqlalchemy.orm import Session
from . import models


def create_context_from_todos(db_session: Session) -> str:
    """
    Create a context string from all todos in the database.
    
    Args:
        db_session: SQLAlchemy database session
        
    Returns:
        str: Context string containing all todos
    """
    try:
        todos = db_session.query(models.TodoDB).all()
        if not todos:
            return "The todo list is currently empty."
        
        context_parts = ["Current tasks in database:"]
        for todo in todos:
            status = "completed" if todo.completed else "pending"
            context_parts.append(f"- ID {todo.id}: {todo.description} [{status}]")
        
        return "\n".join(context_parts)
    except Exception as e:
        print(f"Error creating context from todos: {str(e)}")
        return "Error retrieving tasks from database."