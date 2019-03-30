from main import utils


def test_camel_to_snake_case():
    assert utils.camel_to_snake_case("FirstName") == "first_name"
    assert utils.camel_to_snake_case("firstName") == "first_name"
    assert utils.camel_to_snake_case("AaBbCcDd") == "aa_bb_cc_dd"
