import os

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


def test_extract_beginning_spaces():
    f = utils.extract_beginning_spaces

    assert f("asd") == ""
    assert f("   asd") == "   "
    assert f(" asd  ") == " "


def test_remove_trailing_spaces():
    f = utils.remove_trailing_spaces

    assert f("asd") == "asd"
    assert f("  asd  ") == "  asd"
    assert f(" a s d \n  def  ") == " a s d\n  def"
