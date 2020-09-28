from sqlalchemy import exc
from flask import Blueprint, request
from flask_restx import Resource, Api, fields

from project import db
from project.api.models import BudgetItem


budget_items_blueprint = Blueprint('budget_items', __name__)
api = Api(budget_items_blueprint)

budget_item = api.model('BudgetItem', {
    'id': fields.Integer(readOnly=True),
    'name': fields.String(required=True),
    'cost': fields.String(required=True),
    'paid': fields.Boolean,
    'created_date': fields.DateTime,
})


class BudgetItems(Resource):
    @api.marshal_with(budget_item)
    def get(self, budget_item_id):
        budget_item = BudgetItem.query.filter_by(id=budget_item_id).first()
        if not budget_item:
            api.abort(404, f"Item {budget_item_id} does not exist")
        return budget_item, 200

    @api.expect(budget_item, validate=True)
    def put(self, budget_item_id):
        post_data = request.get_json()
        name = post_data.get("name")
        cost = post_data.get("cost")
        paid = post_data.get("paid")
        response_object = {}

        budget_item = BudgetItem.query.filter_by(id=budget_item_id).first()
        if not budget_item:
            api.abort(404, f"Item {budget_item_id} does not exist")
        budget_item.name = name
        budget_item.cost = cost
        budget_item.paid = paid
        db.session.commit()
        response_object["message"] = f"{budget_item.id} was updated!"
        return response_object, 200
        
    def delete(self, budget_item_id):
        response_object = {}
        budget_item = BudgetItem.query.filter_by(id=budget_item_id).first()
        if not budget_item:
            api.abort(404, f"Item {budget_item_id} does not exist")
        db.session.delete(budget_item)
        db.session.commit()
        response_object["message"] = f"{budget_item.name} was removed!"
        return response_object, 200  


class BudgetItemsList(Resource):
    @api.marshal_with(budget_item)
    def get(self, budget_item_id):
        return BudgetItem.query.filter_by(id=budget_item_id).first(), 200

    @api.marshal_with(budget_item, as_list=True)
    def get(self):
        return BudgetItem.query.all(), 200

    @api.expect(budget_item, validate=True)
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
api.add_resource(BudgetItems, '/budget_items/<int:budget_item_id>')
