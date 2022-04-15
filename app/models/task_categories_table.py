from app.configs.database import db


tasks_categories_table = db.Table("tasks_categories",
        db.Column("id", db.Integer, primary_key=True),
        db.Column("task_id", db.Integer, db.ForeignKey("tasks.id"),nullable=False),
        db.Column("categories_id", db.Integer, db.ForeignKey("categories.id"),nullable=False)
)