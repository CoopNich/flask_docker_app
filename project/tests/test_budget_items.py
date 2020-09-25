import json

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
