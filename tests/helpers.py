from reformat_gherkin.options import AlignmentMode, NewlineMode, Options, WriteBackMode

OPTIONS = [
    Options(
        write_back=WriteBackMode.CHECK,
        step_keyword_alignment=alignment_mode,
        newline=NewlineMode.KEEP,
        fast=False,
    )
    for alignment_mode in AlignmentMode
]


def get_content(dir_name):
    with open(f"tests/data/valid/{dir_name}/input.feature") as f:
        return f.read()


def dump_to_stderr(*output: str) -> str:
    return "\n" + "\n".join(output) + "\n"
