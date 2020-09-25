from flask import Blueprint, request
from flask_restx import Resource, Api

from project import db
from project.api.models import BudgetItem


budget_items_blueprint = Blueprint('budget_items', __name__)
api = Api(budget_items_blueprint)


class BudgetItemsList(Resource):
    def post(self):
        post_data = request.get_json()
        name = post_data.get('name')
        cost = post_data.get('cost')
        response_object = {}

        budget_item = BudgetItem.query.filter_by(name=name).first()
        if budget_item:
            response_object['message'] = 'Sorry. That item already exists.'
            return response_object, 400
        db.session.add(BudgetItem(name=name, cost=cost))
        db.session.commit()
        response_object = {
            'message': f'{name} was added!'
        }
        return response_object, 201


api.add_resource(BudgetItemsList, '/budget_items')