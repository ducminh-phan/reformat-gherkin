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


@dataclass(frozen=True, kw_only=True)
class Options:
    write_back: WriteBackMode
    step_keyword_alignment: AlignmentMode
    fast: bool
