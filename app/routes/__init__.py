from flask import Flask,Blueprint
from .categories_route import bp as bp_categories
from .tasks_route import bp as bp_tasks 

bp_api = Blueprint("api",__name__)


def init_app(app: Flask):

    bp_api.register_blueprint(bp_categories)
    bp_api.register_blueprint(bp_tasks)

    app.register_blueprint(bp_api)

