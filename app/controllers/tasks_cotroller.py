from http import HTTPStatus
from flask import jsonify, request
from app.models.task_model import TaskModel
from app.models.categorie_model import CategorieModel
from app.configs.database import db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation


def create_task():

    session: Session = db.session
    
    data = request.get_json()

    categories = data.pop("categories")

    if data["importance"] == 1 and data["urgency"] == 1:
        data["eisenhower_id"] = 1
    if data["importance"] == 2 and data["urgency"] == 1:
        data["eisenhower_id"] = 2
    if data["importance"] == 1 and data["urgency"] == 2:
        data["eisenhower_id"] = 3
    if data["importance"] == 2 and data["urgency"] == 2:
        data["eisenhower_id"] = 4
    try:
        task = TaskModel(**data)
    except TypeError as err:
        return {"error": str(err)}, HTTPStatus.BAD_REQUEST
    # except ValueError as err:
    #     return {"msg": {"valid_options": {"importance": [1, 2],"urgency": [1, 2]},"recieved_options": {"importance": data["importance"],"urgency": data["urgency"]}}}, HTTPStatus.BAD_REQUEST
    except IntegrityError as err:
        if type(err.orig) == UniqueViolation :
            return {"msg": "task already exists!"}, HTTPStatus.CONFLICT

    for category in categories:

        c = session.query(CategorieModel).filter_by(name=category.lower()).first()

        if not c:
            new_category = CategorieModel(name=category)

            session.add(new_category)
            task.categories.append(new_category)
        
        task.categories.append(c)
    
    session.add(task)
    session.commit()

    return jsonify({"name": task.name,"id": task.id, "description": task.description,"duration": task.duration,"categories":[category.name for category in task.categories],"classification": task.classification.type }), HTTPStatus.CREATED


def update_task(id):

    session: Session = db.session

    data = request.get_json()

    task = session.query(TaskModel).get(id)

    if not task:

        return {"msg": "task not found!"}, HTTPStatus.NOT_FOUND
    
    for key,value in data.items() :

        setattr(task, key, value)


    if data["urgency"] or data["importance"]:
        if task.importance == 1 and task.urgency == 1:
            setattr(task, "eisenhower_id" , 1)
        if task.importance == 2 and task.urgency == 1:
            setattr(task, "eisenhower_id" , 2)
        if task.importance == 1 and task.urgency == 2:
            setattr(task, "eisenhower_id" , 3)
        if task.importance == 2 and task.urgency == 2:
            setattr(task, "eisenhower_id" , 4)


    
    session.commit()

    return jsonify({"name": task.name,"id": task.id, "description": task.description,"duration": task.duration,"categories":[category.name for category in task.categories],"classification": task.classification.type }), HTTPStatus.OK


def delete_task(id):

    session: Session = db.session

    task = session.query(TaskModel).get(id)

    if not task:

        return {"msg": "task not found!"}, HTTPStatus.NOT_FOUND
    
    session.delete(task)
    session.commit()

    return "", HTTPStatus.NO_CONTENT






