from __future__ import annotations

from flask import Flask
from flask_cors import CORS


def init_middleware(app: Flask):
    # init configuration
    app.config.from_pyfile("config.py")

    # init db
    from .database import init_db

    init_db(app)

    from .api import register_api

    register_api(app)

    # implement CORS
    CORS(app, resources=r"/api/*")

    from .audit import register_auditing

    register_auditing(app)


def create_app():
    app = Flask(__name__)

    init_middleware(app)

    return app
