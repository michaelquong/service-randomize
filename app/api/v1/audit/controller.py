from __future__ import annotations

from sqlalchemy.exc import SQLAlchemyError

from .model import AuditLog
from app.database import db


class AuditCtrl:
    @classmethod
    def create_new_log(cls, request, response) -> None:
        """Create a new audit log entry when every a request is made.
        Errors are logged to console.
        """
        new = AuditLog(
            method=request.method,
            route=request.path,
            data=str(request.get_data()),
            status=response.status,
        )
        try:
            db.session.add(new)
            db.session.commit()
        except SQLAlchemyError as err:
            print(err)
            db.session.rollback()
        else:
            db.session.flush()

    @classmethod
    def get_tail_logs(cls, page_limit: int = 10):
        """Return the last `page_limit` of entries from the audit_log table."""
        query = AuditLog.query.order_by(AuditLog.id.desc()).limit(page_limit)
        results = query.all()
        return results
