from __future__ import annotations

from flask.views import MethodView
from flask_smorest import abort
from flask_smorest import Blueprint

from .controller import AuditCtrl
from .schema import LogHistory

bp = Blueprint(
    "history",
    __name__,
    url_prefix="/histories",
    description="Providing API usage history.",
)


@bp.route("/")
class HistoryAPI(MethodView):
    @bp.response(200, LogHistory(many=True))
    def get(self):
        """List the last 10 audit logs in history."""
        results = AuditCtrl.get_tail_logs(page_limit=10)
        return results[::-1]
