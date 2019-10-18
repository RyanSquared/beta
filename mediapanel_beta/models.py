import click
from flask.cli import with_appcontext

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError  # noqa: F401

from mediapanel.db import Base, User, Client  # noqa: F401

db = SQLAlchemy(model_class=Base)


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear and reset db"""
    db.create_all()
    click.echo("Initialized database")


def init_app(app):
    db.init_app(app)
    app.cli.add_command(init_db_command)
