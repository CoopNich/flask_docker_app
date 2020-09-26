
import sys

from flask.cli import FlaskGroup

from project import create_app, db   # new
from project.api.models import BudgetItem  # new


app = create_app()  # new
cli = FlaskGroup(create_app=create_app)  # new


@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command('seed_db')
def seed_db():
    db.session.add(BudgetItem(name='rent', cost="1200.00"))
    db.session.add(BudgetItem(name='car payment', cost='250.00'))
    db.session.commit()


if __name__ == '__main__':
    cli()