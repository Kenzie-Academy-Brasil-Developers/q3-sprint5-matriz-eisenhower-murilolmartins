from http import HTTPStatus
from flask import jsonify, request, session
from sqlalchemy.orm.session import Session
from app.configs.database import db
from app.models.categorie_model import CategorieModel
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation


def create_category():

    session: Session = db.session

    data = request.get_json()

    try:
        category = CategorieModel(**data)

        session.add(category)
        session.commit()

        return jsonify(category), HTTPStatus.CREATED

    except IntegrityError as err:
        
        if type(err.orig) == UniqueViolation :
            return {"msg": "category already exists!"}, HTTPStatus.CONFLICT

def update_categorie(id: int):

    session: Session = db.session

    data = request.get_json()

    category = session.query(CategorieModel).get(id)

    if not category:

        return {"msg": "category not found!"}, HTTPStatus.NOT_FOUND
    
    for key,value in data.items():

        setattr(category,key,value)
    
    session.commit()

    return jsonify(category), HTTPStatus.OK


def delete_categorie(id: int):

    session: Session = db.session

    data = request.get_json()

    category = session.query(CategorieModel).get(id)

    if not category:

        return {"msg": "category not found!"}, HTTPStatus.NOT_FOUND
    
    session.delete(category)
    session.commit()

    return "", HTTPStatus.NO_CONTENT




def get_all():

    session : Session = db.session

    categories = session.query(CategorieModel).all()

    serialize = [
        {
            "id": category.id,
            "name": category.name,
            "description": category.description,
            "tasks": [
                {
                    "id": task.id,
                    "name": task.name,
                    "description": task.description,
                    "duration": task.duration,
                    "cassification": task.classification.type

                } for task in category.tasks
            ]

        }
       for category in categories
    ]

    return jsonify(serialize), HTTPStatus.OK
