from __future__ import annotations

from flask.views import MethodView
from flask_smorest import abort
from flask_smorest import Blueprint

from .controller import Randomize
from .schema import JumbledInput
from .schema import JumbledWord


bp = Blueprint(
    "randomizes",
    __name__,
    url_prefix="/randomizes",
    description="Operations related to randomizing strings provided.",
)


@bp.route("/")
class RandomizeAPI(MethodView):
    @bp.arguments(JumbledInput)
    @bp.response(201, JumbledWord)
    def post(self, data):
        """Randomize word provided in json body."""
        try:
            return Randomize.create_new_entry(data=data)
        except ValueError as err:
            abort(400, err)


@bp.route("/<id>")
class RandomizedIdAPI(MethodView):
    @bp.response(200, JumbledWord)
    def get(self, id: int):
        """Retrieve the word and jumbled word by the assigned ID."""
        return Randomize.get_by_id(id=id)
