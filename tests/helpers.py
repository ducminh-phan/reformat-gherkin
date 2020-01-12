from reformat_gherkin.options import (
    AlignmentMode,
    NewlineMode,
    Options,
    TagLineMode,
    WriteBackMode,
)


def make_options(
    alignment_mode=AlignmentMode.NONE, tag_line_mode=TagLineMode.MULTILINE
):
    return Options(
        write_back=WriteBackMode.CHECK,
        step_keyword_alignment=alignment_mode,
        newline=NewlineMode.KEEP,
        tag_line_mode=tag_line_mode,
        fast=False,
    )


OPTIONS = [make_options(alignment_mode) for alignment_mode in AlignmentMode]


filename_option_map = {
    "expected_default": make_options(),
    "expected_left_aligned": make_options(alignment_mode=AlignmentMode.LEFT),
    "expected_right_aligned": make_options(alignment_mode=AlignmentMode.RIGHT),
    "expected_single_line_tags": make_options(tag_line_mode=TagLineMode.SINGLELINE),
}


def get_content(dir_name):
    with open(f"tests/data/valid/{dir_name}/input.feature") as f:
        return f.read()


def dump_to_stderr(*output: str) -> str:
    return "\n" + "\n".join(output) + "\n"
