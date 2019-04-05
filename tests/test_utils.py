from main import utils


def test_camel_to_snake_case():
    f = utils.camel_to_snake_case

    assert f("FirstName") == "first_name"
    assert f("firstName") == "first_name"
    assert f("AaBbCcDd") == "aa_bb_cc_dd"


def test_extract_beginning_spaces():
    f = utils.extract_beginning_spaces
    assert f("asd") == ""
    assert f("   asd") == "   "
    assert f(" asd  ") == " "
