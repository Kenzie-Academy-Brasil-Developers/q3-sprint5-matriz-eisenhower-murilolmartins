from flask import Blueprint
from app.controllers import categories_controler

bp = Blueprint("categories",__name__,url_prefix= "/categories")

bp.get("")(categories_controler.get_all)
bp.post("")(categories_controler.create_category)
bp.patch("<int:id>")(categories_controler.update_categorie)
bp.delete("<int:id>")(categories_controler.delete_categorie)