from __future__ import annotations

from marshmallow import fields
from marshmallow import Schema


class JumbledWord(Schema):
    """Output Schema response users will expect to see."""

    class Meta:
        fields = ("id", "created", "updated", "original", "jumbled")

    id = fields.Int()
    created = fields.DateTime()
    updated = fields.DateTime()
    original = fields.Str()
    jumbled = fields.Str()


class JumbledInput(Schema):
    """Expected input JSON body Schema."""

    word = fields.Str()
