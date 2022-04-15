from flask import Blueprint
from app.controllers import tasks_cotroller

bp = Blueprint("tasks",__name__,url_prefix= "/tasks")

bp.post("")(tasks_cotroller.create_task)
bp.patch("<int:id>")(tasks_cotroller.update_task)
bp.delete("<int:id>")(tasks_cotroller.delete_task)