from reformat_gherkin.ast_node import GherkinDocument
from reformat_gherkin.formatter import INDENT_LEVEL_MAP, LineGenerator
from reformat_gherkin.options import AlignmentMode, TagLineMode


def verify_indent_level_map():
    """
    Make sure that all node types with tags are included in the indent map.
    """
    import reformat_gherkin.ast_node as ast_node

    node_types = [
        attr
        for attr in (getattr(ast_node, name) for name in dir(ast_node))
        if isinstance(attr, type)
    ]

    for node_type in node_types:
        if hasattr(node_type, "tags"):
            assert node_type in INDENT_LEVEL_MAP


def format_ast(
    ast, alignment_mode=AlignmentMode.LEFT, tag_line_mode=TagLineMode.MULTILINE
):
    line_generator = LineGenerator(ast, alignment_mode, tag_line_mode)
    lines = line_generator.generate()
    return "\n".join(lines)


def test_format_empty_ast():
    assert format_ast(GherkinDocument(())) == ""
