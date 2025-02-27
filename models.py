from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    priority = Column(String(255), nullable=False)
    deadline = Column(String(255), nullable=False)
    duration = Column(Integer, nullable=False)
    completed = Column(Boolean, nullable=False, default=False)
    
