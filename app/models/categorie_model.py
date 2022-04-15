from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import validates


@dataclass
class CategorieModel(db.Model):

    id: int
    name: str
    description: str

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable= False , unique=True)
    description= Column(String)

    @validates("name")
    def validate_name(self,key,name: str):
        return name.lower()