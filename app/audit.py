from __future__ import annotations

from flask import Flask
from flask import request

from .api.v1.audit.controller import AuditCtrl
from .database import db


monitored_apis = "/api/randomizes"


def register_auditing(app: Flask):
    """Register an after request function to log request history to API endpoints in monitored_apis"""

    @app.after_request
    def log_request(response):
        if request.path.startswith(monitored_apis):
            AuditCtrl.create_new_log(request, response)

        return response
