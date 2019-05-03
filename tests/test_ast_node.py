from reformat_gherkin.parser import parse


def test_iterate(valid_contents):
    for content in valid_contents:
        ast = parse(content)

        for node in ast:
            assert hasattr(node, "location")
