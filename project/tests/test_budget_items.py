import json

from project import db
from project.api.models import BudgetItem

# test for succesful post


def test_add_budget_item(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/budget_items',
        data=json.dumps({
            'name': 'rent',
            'cost': '1200.00'
        }),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert 'rent was added!' in data['message']

# test for empty json object


def test_add_budget_item_invalid_json(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/budget_items',
        data=json.dumps({}),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Input payload validation failed' in data['message']

# test for invalid json keys


def test_add_budget_item_invalid_json_keys(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/budget_items',
        data=json.dumps({"cost": "1000"}),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Input payload validation failed' in data['message']

# test for duplicate items


def test_add_budget_item_duplicate(test_app, test_database):
    client = test_app.test_client()
    client.post(
        '/budget_items',
        data=json.dumps({
            'name': 'rent',
            'cost': '1200.00'
        }),
        content_type='application/json',
    )
    resp = client.post(
        '/budget_items',
        data=json.dumps({
            'name': 'rent',
            'cost': '1200.00'
        }),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Sorry. That item already exists.' in data['message']

# test to GET single budget item

def test_single_budget_item(test_app, test_database):
    budget_item = BudgetItem(name='car', cost="250.00")
    db.session.add(budget_item)
    db.session.commit()
    client = test_app.test_client()
    resp = client.get(f'/budget_items/{budget_item.id}')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert 'car' in data['name']
    assert '250.00' in data['cost']


