import difflib
import io
import re
import tempfile
import tokenize
from contextlib import nullcontext
from functools import lru_cache, partial
from pathlib import Path
from typing import IO, AnyStr, BinaryIO, Tuple, Union

import click
from wcwidth import wcswidth

out = partial(click.secho, bold=True, err=True)
err = partial(click.secho, fg="red", err=True)

_first_cap_re = re.compile(r"(.)([A-Z][a-z]+)")
_all_cap_re = re.compile(r"([a-z\d])([A-Z])")


@lru_cache()
def camel_to_snake_case(name: str) -> str:
    """
    Convert camelCase to snake_case.
    Taken from https://stackoverflow.com/a/1176023/2585762.
    """
    s1 = _first_cap_re.sub(r"\1_\2", name)
    return _all_cap_re.sub(r"\1_\2", s1).lower()


def dump_to_file(*output: str) -> str:
    """
    Dump `output` to a temporary file. Return path to the file.
    """
    with tempfile.NamedTemporaryFile(
        mode="w",
        prefix="rfmt-ghk_",
        suffix=".log",
        delete=False,
        encoding="utf-8",
    ) as f:
        for lines in output:
            f.write(lines)
            if lines and lines[-1] != "\n":
                f.write("\n")
    return f.name


def diff(a: str, b: str, a_name: str, b_name: str) -> str:
    """Return a unified diff string between strings `a` and `b`."""
    a_lines = [line + "\n" for line in a.split("\n")]
    b_lines = [line + "\n" for line in b.split("\n")]
    return "".join(
        difflib.unified_diff(
            a_lines,
            b_lines,
            fromfile=a_name,
            tofile=b_name,
            n=5,
        )
    )


_beginning_spaces_re = re.compile(r"^(\s*).*")


def extract_beginning_spaces(string: str) -> str:
    return _beginning_spaces_re.findall(string)[0]


def remove_trailing_spaces(string: str) -> str:
    ends_with_newline = string.endswith("\n")

    lines = string.splitlines()
    if ends_with_newline:
        lines.append("")

    return "\n".join(line.rstrip() for line in lines)


def decode_stream(src: BinaryIO) -> Tuple[str, str, str]:
    """
    Return a tuple of (decoded_contents, encoding, newline).

    `newline` is either CRLF or LF but `decoded_contents` is decoded with
    universal newlines (i.e. only contains LF).
    """
    # in case the source is not seekable, read into memory now
    src = io.BytesIO(src.read())
    encoding, lines = tokenize.detect_encoding(src.readline)
    if not lines:
        return "", encoding, "\n"

    newline = "\r\n" if b"\r\n" == lines[0][-2:] else "\n"
    src.seek(0)
    with io.TextIOWrapper(src, encoding) as tiow:
        return tiow.read(), encoding, newline


@lru_cache()
def get_display_width(text: str) -> int:
    """
    Get the display width of a string.

    When displayed in a console, some characters can have a width of 2 (for
    example, East Asian characters) or a width of 0 (for example, combining
    diacritic characters). Use the wcwidth package to find the correct display
    width for strings including these characters.

    Some characters do not have a width (for example, control characters like
    the bell character). If a string contains any such characters, then
    wcwidth.wcswidth returns -1. In this case, use the number of code points as
    a fallback.
    """
    width = wcswidth(text)
    if width < 0:
        width = len(text)
    return width


def open_stream_or_path(stream_or_path: Union[IO[AnyStr], Path], mode: str):
    if isinstance(stream_or_path, Path):
        return open(stream_or_path, mode)
    else:
        return nullcontext(stream_or_path)
