from __future__ import annotations

from flask import Flask
from flask_smorest import Api
from flask_smorest import Blueprint


api_bp = Blueprint("api", __name__, url_prefix="/api", description="Global API")


def register_api(app: Flask) -> None:
    """Initialize Api instance with Flask App instance and register all blueprints."""
    api = Api(app)

    # register child blueprints
    from .v1.randomize import bp as randomize_bp
    from .v1.audit import bp as audit_bp

    api_bp.register_blueprint(randomize_bp)
    api_bp.register_blueprint(audit_bp)

    # register api blueprint to app
    api.register_blueprint(api_bp)
