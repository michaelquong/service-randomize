from __future__ import annotations

from marshmallow import fields
from marshmallow import Schema


class LogHistory(Schema):
    """Output Schema response expected to see."""

    class Meta:
        fields = ("id", "created", "method", "route", "data", "status")

    id = fields.Int()
    created = fields.DateTime()
    method = fields.Str()
    route = fields.Str()
    data = fields.Str()
    status = fields.Str()
