from __future__ import annotations

from random import sample

from sqlalchemy.exc import SQLAlchemyError

from .model import Word
from app.database import db


class Randomize:
    @classmethod
    def _randomize(cls, word: str) -> str:
        """Use random.sample function from random package to randomize string provided.
        Return randomized string
        """
        return "".join(sample(word, len(word)))

    @classmethod
    def create_new_entry(cls, data: dict) -> Word:
        """Generate new randomized word based on JSON data provided.
        Assumption: Repeated strings will be randomized again rather than providing the same randomization it already has.
        Results in users getting different randomization's for the same input string
        """
        word = data.get("word", None)
        if not word:
            raise ValueError(
                f"Word provided in request body, cannot be an empty string. Given `{data}`"
            )
        jumbled_word = cls._randomize(word)

        new = Word(original=word, jumbled=jumbled_word)
        try:
            db.session.add(new)
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            raise err
        else:
            db.session.flush()
        return new

    @classmethod
    def get_by_id(cls, id: int) -> Word:
        """Retrieve randomization data based on ID."""
        result = Word.query.filter_by(id=id).first()
        return result
