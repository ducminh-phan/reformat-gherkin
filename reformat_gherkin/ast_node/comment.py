from typing import Annotated

from pydantic import AfterValidator

from ._base import GherkinString
from .location import LocationMixin


def normalize_comment_text(text: str) -> str:
    """
    Return a consistently formatted comment from the given Comment instance.
    All comments should have a single space between the hash sign and the content.
    """
    # A comment always start with a hash sign
    normalized_text = text[1:].strip()

    return ("# " + normalized_text).strip()


class Comment(LocationMixin):
    text: Annotated[GherkinString, AfterValidator(normalize_comment_text)]
