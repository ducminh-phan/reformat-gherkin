import os
from io import BytesIO, StringIO

import pytest

from reformat_gherkin import utils


def test_camel_to_snake_case():
    f = utils.camel_to_snake_case

    assert f("FirstName") == "first_name"
    assert f("firstName") == "first_name"
    assert f("AaBbCcDd") == "aa_bb_cc_dd"


@pytest.mark.parametrize(
    "output, content",
    [
        (("a", "bb"), "a\nbb\n"),
        (("a\n", "bb"), "a\nbb\n"),
        (("a\n", "bb\n"), "a\nbb\n"),
    ],
)
def test_dump_to_file(output, content):
    f = utils.dump_to_file

    name = f(*output)

    with open(name, "r") as f:
        assert f.read() == content

    os.remove(name)


def test_remove_trailing_spaces():
    f = utils.remove_trailing_spaces

    assert f("asd") == "asd"
    assert f("  asd  ") == "  asd"
    assert f(" a s d \n  def  ") == " a s d\n  def"


def test_decode_bytes():
    f = utils.decode_bytes
    lines = "Lorem ipsum dolor sit amet".replace(" ", "\n")

    for newline in ("\n", "\r\n"):
        tmp_file = StringIO(lines, newline=newline)

        tmp_buf = BytesIO(tmp_file.read().encode())

        contents, _, _newline = f(tmp_buf.read())

        assert contents == lines
        assert _newline == newline


@pytest.mark.parametrize(
    ["text", "width"],
    [
        ("abc", 3),
        ("あああ", 6),
        ("1.5倍", 5),
        ("😍", 2),
        ("１２３", 6),
        ("ááá", 3),  # Combining diacritics
        ("ááá", 3),  # Single-character diacritics
        ("aaa\b", 4),
        ("\t", 1),
        ("", 0),
        ("\\|", 2),  # Gherkin pipe escape sequence
        ("\u202f", 1),  # Narrow no-break space
        ("\u200d", 0),  # Zero width joiner
    ],
)
def test_get_display_width(text, width):
    assert utils.get_display_width(text) == width
