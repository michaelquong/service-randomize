"""Standard minimum Flask configuration settings
"""
from __future__ import annotations

from os import environ
from os import path

from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


# Application description
API_TITLE = "Randomize String Service"
API_VERSION = "0.0.1"
API_SPEC_OPTIONS = {
    "security": [{"bearerAuth": []}],
    "components": {
        "securitySchemes": {
            "bearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
        }
    },
}


# OpenAPI documentation
OPENAPI_VERSION = "3.0.2"
OPENAPI_URL_PREFIX = "/"
OPENAPI_SWAGGER_UI_PATH = "/docs"
OPENAPI_SWAGGER_UI_URL = "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.18.3/"

# Database
SQLALCHEMY_DATABASE_URI = "sqlite:///project.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
