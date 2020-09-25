from flask.cli import FlaskGroup

from project import app


cli = FlaskGroup(app)

# This registers a new command, recreate_db, to the CLI so that we can run it from the command line
@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

if __name__ == '__main__':
    cli()