from typing import Optional, Tuple

import click

from .config import read_config_file
from .core import reformat
from .errors import EmptySources
from .options import AlignmentMode, Options, WriteBackMode
from .report import Report
from .utils import out
from .version import __version__


@click.command()
@click.argument(
    "src",
    nargs=-1,
    type=click.Path(
        exists=True, file_okay=True, dir_okay=True, readable=True, resolve_path=True
    ),
    is_eager=True,
)
@click.option(
    "--check",
    is_flag=True,
    help=(
        "Don't write the files back, just return the status. Return code 0 "
        "means nothing would change. Return code 1 means some files would be "
        "reformatted. Return code 123 means there was an internal error."
    ),
)
@click.option(
    "-a",
    "--alignment",
    type=click.Choice([AlignmentMode.LEFT.value, AlignmentMode.RIGHT.value]),
    help=(
        "Specify the alignment of step keywords (Given, When, Then,...). "
        "If specified, all statements after step keywords are left-aligned, "
        "spaces are inserted before/after the keywords to right/left align them. "
        "By default, step keywords are left-aligned, and there is a single "
        "space between the step keyword and the statement."
    ),
)
@click.option(
    "--fast/--safe",
    is_flag=True,
    help="If --fast given, skip the sanity checks of file contents. [default: --safe]",
)
@click.option(
    "--config",
    type=click.Path(
        exists=True, file_okay=True, dir_okay=False, readable=True, allow_dash=False
    ),
    is_eager=True,
    callback=read_config_file,
    help="Read configuration from FILE.",
)
@click.version_option(version=__version__)
@click.pass_context
def main(
    ctx: click.Context,
    src: Tuple[str],
    check: bool,
    alignment: Optional[str],
    fast: bool,
    config: Optional[str],
) -> None:
    """
    Reformat the given Gherkin files and all files in the given directories recursively.
    """
    if config:
        out(f"Using configuration from {config}.", bold=False, fg="blue")

    write_back_mode = WriteBackMode.from_configuration(check)
    alignment_mode = AlignmentMode.from_configuration(alignment)

    options = Options(
        write_back=write_back_mode, step_keyword_alignment=alignment_mode, fast=fast
    )

    report = Report(check=check)
    try:
        reformat(src, report, options=options)
    except EmptySources:
        out("No paths given. Nothing to do 😴")
        ctx.exit(0)

    bang = "💥 💔 💥" if report.return_code else "✨ 🍰 ✨"
    out(f"All done! {bang}")
    click.secho(str(report), err=True)
    ctx.exit(report.return_code)
