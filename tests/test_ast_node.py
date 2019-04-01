from main.ast_node.gherkin_document import GherkinDocument
from main.parser import parse


def test_iterate(valid_contents):
    for content in valid_contents:
        ast = parse(content)

        for node in ast:
            if not isinstance(node, GherkinDocument):
                assert hasattr(node, "location")
