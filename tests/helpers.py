from reformat_gherkin.options import AlignmentMode, Options, WriteBackMode

OPTIONS = [
    Options(
        write_back=WriteBackMode.CHECK,
        step_keyword_alignment=alignment_mode,
        fast=False,
    )
    for alignment_mode in AlignmentMode
]


def get_content(file_name):
    with open(f"tests/data/valid/{file_name}.feature") as f:
        return f.read()


def dump_to_stderr(*output: str) -> str:
    return "\n" + "\n".join(output) + "\n"
