from enum import Enum, unique
from typing import Optional

from attr import dataclass


@unique
class WriteBackMode(Enum):
    INPLACE = "inplace"
    CHECK = "check"

    @classmethod
    def from_configuration(cls, check: bool) -> "WriteBackMode":
        return WriteBackMode.CHECK if check else WriteBackMode.INPLACE


@unique
class AlignmentMode(Enum):
    NONE = None
    LEFT = "left"
    RIGHT = "right"

    @classmethod
    def from_configuration(cls, alignment: Optional[str]) -> "AlignmentMode":
        return AlignmentMode(alignment)


@unique
class NewlineMode(Enum):
    KEEP = None
    LF = "LF"
    CRLF = "CRLF"

    @classmethod
    def from_configuration(cls, newline: Optional[str]) -> "NewlineMode":
        return NewlineMode(newline)


@unique
class TagLineMode(Enum):
    SINGLELINE = "singleline"
    MULTILINE = "multiline"

    @classmethod
    def from_configuration(cls, single_line_tags: bool) -> "TagLineMode":
        return TagLineMode.SINGLELINE if single_line_tags else TagLineMode.MULTILINE


def get_indent_from_configuration(tab_width: int, use_tabs: bool):
    return "\t" if use_tabs else " " * tab_width


@dataclass(frozen=True)
class Options:
    write_back: WriteBackMode
    step_keyword_alignment: AlignmentMode
    newline: NewlineMode
    tag_line_mode: TagLineMode
    fast: bool
    indent: str
