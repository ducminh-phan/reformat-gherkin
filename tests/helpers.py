from reformat_gherkin.options import AlignmentMode, NewlineMode, Options, WriteBackMode


def make_options(alignment_mode):
    return Options(
        write_back=WriteBackMode.CHECK,
        step_keyword_alignment=alignment_mode,
        newline=NewlineMode.KEEP,
        fast=False,
    )


OPTIONS = [make_options(alignment_mode) for alignment_mode in AlignmentMode]


FILENAME_OPTION_MAP = {
    "expected_default": make_options(AlignmentMode.NONE),
    "expected_left_aligned": make_options(AlignmentMode.LEFT),
    "expected_right_aligned": make_options(AlignmentMode.RIGHT),
}


def get_content(dir_name):
    with open(f"tests/data/valid/{dir_name}/input.feature") as f:
        return f.read()


def dump_to_stderr(*output: str) -> str:
    return "\n" + "\n".join(output) + "\n"
