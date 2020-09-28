import json

from project.api.models import BudgetItem

# test POST for succesful post


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

# test POST for empty json object


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

# test POST for invalid json keys


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

# test POST for duplicate items


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

# test GET single budget item

def test_single_budget_item(test_app, test_database, add_budget_item):
    budget_item = add_budget_item(name='car', cost="250.00")
    client = test_app.test_client()
    resp = client.get(f'/budget_items/{budget_item.id}')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert 'car' in data['name']
    assert '250.00' in data['cost']

# test GET all budget items

def test_all_items(test_app, test_database, add_budget_item):
    test_database.session.query(BudgetItem).delete()
    add_budget_item('insurance', '200.00')
    add_budget_item('electric', '100.00')
    client = test_app.test_client()
    resp = client.get('/budget_items')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data) == 2
    assert 'insurance' in data[0]['name']
    assert '200.00' in data[0]['cost']
    assert 'electric' in data[1]['name']
    assert '100.00' in data[1]['cost']

# test GET if id does not exist 

def test_single_budget_item_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.get('/budget_items/999')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert 'Item 999 does not exist' in data['message']

# test DELETE single item

def test_remove_budget_item(test_app, test_database, add_budget_item):
    test_database.session.query(BudgetItem).delete()
    budget_item = add_budget_item("rent", "1200")
    client = test_app.test_client()
    resp_one = client.get("/budget_items")
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    assert len(data) == 1
    resp_two = client.delete(f"/budget_items/{budget_item.id}")
    data = json.loads(resp_two.data.decode())
    assert resp_two.status_code == 200
    assert 'rent was removed!' in data['message']
    resp_three = client.get("/budget_items")
    data = json.loads(resp_three.data.decode())
    assert resp_three.status_code == 200
    assert len(data) == 0

# test DELETE if id does not exist

def test_remove_budget_item_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.delete("/budget_items/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "Item 999 does not exist" in data["message"]

def test_update_budget_item(test_app, test_database, add_budget_item):
    budget_item = add_budget_item("example", "9000",)
    client = test_app.test_client()
    resp_one = client.put(
        f"/budget_items/{budget_item.id}",
        data=json.dumps({"name": "new_example", "cost": "8000", "paid": True}),
        content_type="application/json",
    )
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    assert f"{budget_item.id} was updated!" in data["message"]
    resp_two = client.get(f"/budget_items/{budget_item.id}")
    data = json.loads(resp_two.data.decode())
    assert resp_two.status_code == 200
    assert "new_example" in data["name"]
    assert "8000" in data["cost"]
    assert True == data["paid"]


def test_update_budget_item_invalid_json(test_app, test_database):
    client = test_app.test_client()
    resp = client.put(
        "/budget_items/1",
        data=json.dumps({}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_update_budget_item_invalid_json_keys(test_app, test_database):
    client = test_app.test_client()
    resp = client.put(
        "/budget_items/1",
        data=json.dumps({"cost": "900.00"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_update_budget_item_does_not_exist(test_app, test_database):
    client = test_app.test_client()
    resp = client.put(
        "/budget_items/999",
        data=json.dumps({"name": "loan", "cost": "600.00", "paid": True}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "Item 999 does not exist" in data["message"]




