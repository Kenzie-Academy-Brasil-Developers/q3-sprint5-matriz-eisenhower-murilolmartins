from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy import Column, ForeignKey,Integer,String
from sqlalchemy.orm import relationship,backref, validates
from .task_categories_table import tasks_categories_table


@dataclass
class TaskModel(db.Model):

    id: int
    name: str
    description: str
    duration: int
    classification: str
    categories: list

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    name= Column(String(100), nullable=False, unique=True)
    description=Column(String)
    duration=Column(Integer)
    importance= Column(Integer)
    urgency= Column(Integer)

    eisenhower_id = Column(Integer, ForeignKey("eisenhowers.id"), nullable=False)

    categories = relationship("CategorieModel",secondary=tasks_categories_table ,backref="tasks")

    classification = relationship("EisenhowerModel", backref="tasks", uselist=False)


    @validates("name","importance","urgency") 
    def validate_fields(self, key, value: str):
        if key == "name":
            return value.lower()
        if key == "importance" or key == "urgency":
            if not type(value) == int:
                raise TypeError
            if value != 1 and value != 2:
                raise ValueError
            return value


