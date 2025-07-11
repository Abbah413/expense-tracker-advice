import sqlite3
import click
from flask import current_app, g
import os

import os

def get_db():
    if 'db' not in g:
        db_path = os.path.abspath(current_app.config['DATABASE'])
        print(f"✅ Connecting to database at: {db_path}")
        print(f"📌 Using database: {current_app.config['DATABASE']}")

        g.db = sqlite3.connect(
            db_path,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
