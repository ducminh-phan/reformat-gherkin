import click


@click.command()
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "-o",
    "--output",
    default="inplace",
    show_default=True,
    help=(
        "Specify the output path. Valid options: inplace, stdout, "
        "or a path to a folder, which should not be a sub-folder of the path provided."
    ),
)
@click.option(
    "-R",
    "--no-recursive",
    "recursive",
    flag_value=False,
    default=True,
    help=(
        "By default, the sub-folders are scanned recursively. Use this option to "
        "scan files without looking into sub-folders."
    ),
)
def main(path: str, output: str, recursive: bool):
    """
    Reformat a Gherkin file or all files in a directory. If a directory is provided,
    the tool will reformat all files in all sub-folders recursively.
    """
    print(path, output, recursive)
