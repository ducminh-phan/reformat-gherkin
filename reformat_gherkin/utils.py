import difflib
import re
import tempfile
from functools import lru_cache, partial
from typing import List

import click
from gherkin.dialect import Dialect

out = partial(click.secho, bold=True, err=True)
err = partial(click.secho, fg="red", err=True)

_first_cap_re = re.compile(r"(.)([A-Z][a-z]+)")
_all_cap_re = re.compile(r"([a-z0-9])([A-Z])")


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
        mode="w", prefix="rfmt-ghk_", suffix=".log", delete=False, encoding="utf-8"
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
        difflib.unified_diff(a_lines, b_lines, fromfile=a_name, tofile=b_name, n=5)
    )


@lru_cache()
def get_step_keywords(dialect_name="en") -> List[str]:
    dialect = Dialect.for_name(dialect_name)

    keywords = (
        dialect.given_keywords
        + dialect.when_keywords
        + dialect.then_keywords
        + dialect.and_keywords
        + dialect.but_keywords
    )

    return [kw.strip() for kw in keywords]


_beginning_spaces_re = re.compile(r"^(\s*).*")


def extract_beginning_spaces(string: str) -> str:
    return _beginning_spaces_re.findall(string)[0]


def strip_spaces(string: str) -> str:
    lines = string.splitlines()
    return "\n".join(line.strip() for line in lines)
