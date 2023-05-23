from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from app.database import db


@dataclass
class AuditLog(db.Model):
    """Database table model. The format of data storage and expected column types.
    If not provided, created values will be automatically generated based on UTCNow.
    id Key is automatically generated per insert.
    data format is also expected to sanitized as a string.
    """

    id: Optional[int] = None
    created: Optional[datetime] = None
    method: str
    route: str
    data: str
    status: str

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, nullable=False, default=datetime.utcnow)
    method = Column(String)
    route = Column(String)
    data = Column(Text)
    status = Column(String)
