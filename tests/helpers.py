def get_content(file_name):
    with open(f"tests/data/valid/{file_name}.feature") as f:
        return f.read()


def dump_to_stderr(*output: str) -> str:
    return "\n" + "\n".join(output) + "\n"
