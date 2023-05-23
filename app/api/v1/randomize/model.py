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
class Word(db.Model):
    """Database table model. The format of data storage and expected column types.
    If not provided, created and updated datetime values will be automatically generated based on UTCNow.
    id Key is automatically generated per insert.
    """

    id: Optional[int] = None
    created: Optional[datetime] = None
    updated: Optional[datetime] = None
    original: str
    jumbled: str

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated = Column(DateTime, onupdate=datetime.utcnow)
    original = Column(String(255))
    jumbled = Column(String(255))
