from sqlalchemy import Column, Integer, String, Boolean
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# -------------------------------
# 1. SQLAlchemy Model (Database Table)
# -------------------------------
class TodoDB(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    completed = Column(Boolean, default=False)
    category = Column(String, default="Uncategorized")  # For AI auto-categorization

# -------------------------------
# 2. Pydantic Models (FastAPI Validation)
# -------------------------------
class TodoBase(BaseModel):
    description: str
    completed: bool = False
    category: str = "Uncategorized"

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    description: str | None = None
    completed: bool | None = None
    category: str | None = None

class TodoResponse(TodoBase):
    id: int

    class Config:
        from_attributes = True # Purane Pydantic versions mein ye 'orm_mode = True' tha