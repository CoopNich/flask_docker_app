import os
from flask import Flask, jsonify
from flask_restx import Resource, Api
from flask_sqlalchemy import SQLAlchemy


# instantiate the app
app = Flask(__name__)

api = Api(app)

# set config
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings) 

# instantiate the db
db = SQLAlchemy(app)

# model
class BudgetItem(db.Model):
    __tablename__ = 'budget_items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    cost = db.Column(db.String(128), nullable=False)
    paid = db.Column(db.Boolean(), default=False, nullable=False)

    def __init__(self, name, cost):
        self.name = name
        self.cost = cost


class Ping(Resource):
    def get(self):
        return {
            'status': 'success',
            'message': 'pong!'
        }


api.add_resource(Ping, '/ping')