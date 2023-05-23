from __future__ import annotations

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def init_db(app: Flask) -> None:
    """Initiate db instance with configuration from Flask app.
    Also initiate Flask migrate scripts to reflect model changes.
    """
    db.init_app(app)

    migrate.init_app(app, db)
