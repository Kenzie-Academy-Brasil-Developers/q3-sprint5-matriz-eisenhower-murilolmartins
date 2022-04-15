from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy import Column, String, Integer


@dataclass
class EisenhowerModel(db.Model):

    id: int
    type: str

    __tablename__ = "eisenhowers"

    id = Column(Integer, primary_key=True)
    type = Column(String(100))
    

