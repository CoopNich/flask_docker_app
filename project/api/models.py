import os

from flask_admin.contrib.sqla import ModelView 

from sqlalchemy.sql import func

from project import db


class BudgetItem(db.Model):

    __tablename__ = 'budget_items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    cost = db.Column(db.String(128), nullable=False)
    paid = db.Column(db.Boolean(), default=False, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, name, cost):
        self.name = name
        self.cost = cost

if os.getenv("FLASK_ENV") == "development":
    from project import admin
    admin.add_view(ModelView(BudgetItem, db.session))