import pytest

from project import create_app, db
from project.api.models import BudgetItem

# test_app and test_database (for initializing a test database)
@pytest.fixture(scope='module')
def test_app():
    app = create_app()
    app.config.from_object('project.config.TestingConfig')
    with app.app_context():
        yield app  # testing happens here


@pytest.fixture(scope='module')
def test_database():
    db.create_all()
    yield db  # testing happens here
    db.session.remove()
    db.drop_all()

@pytest.fixture(scope='function')
def add_budget_item():
    def _add_budget_item(name, cost):
        budget_item = BudgetItem(name=name, cost=cost)
        db.session.add(budget_item)
        db.session.commit()
        return budget_item
    return _add_budget_item