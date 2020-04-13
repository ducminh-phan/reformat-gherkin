from typing import Optional, Tuple

import click

from .config import read_config_file
from .core import reformat
from .errors import EmptySources
from .options import AlignmentMode, NewlineMode, Options, TagLineMode, WriteBackMode
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
    default=AlignmentMode.RIGHT.value,
    help=(
        "Specify the alignment of step keywords (Given, When, Then,...). "
        "If specified, all statements after step keywords are left-aligned, "
        "spaces are inserted before/after the keywords to right/left align them. "
        "By default, step keywords are left-aligned, and there is a single "
        "space between the step keyword and the statement."
    ),
)
@click.option(
    "-n",
    "--newline",
    type=click.Choice([NewlineMode.LF.value, NewlineMode.CRLF.value]),
    help=(
        "Specify the line separators when formatting files inplace. "
        "If not specified, line separators are preserved."
    ),
)
@click.option(
    "--fast/--safe",
    is_flag=True,
    help="If --fast given, skip the sanity checks of file contents. [default: --safe]"
         "Note: if you use custom --line-tags fast value is True",
)
@click.option(
    "--line-tags",
    type=click.Choice([TagLineMode.SINGLELINE.value, TagLineMode.MULTILINE.value, TagLineMode.CUSTOM.value]),
    default= TagLineMode.CUSTOM.value,
    help=(
        "If 'singleline', output consecutive tags on one line. "
        "If 'multiline', output one tag per line. "
        "If 'custom', output custom tag per line. "
        "[default:CUSTOM"
    ),
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
    newline: Optional[str],
    fast: bool,
    line_tags: Optional[str],
    config: Optional[str],
) -> None:
    """
    Reformat the given Gherkin files and all files in the given directories recursively.
    """
    if config:
        out(f"Using configuration from {config}.", bold=False, fg="blue")

    write_back_mode = WriteBackMode.from_configuration(check)
    alignment_mode = AlignmentMode.from_configuration(alignment)
    newline_mode = NewlineMode.from_configuration(newline)
    tag_line_mode = TagLineMode.from_configuration(line_tags)

    options = Options(
        write_back=write_back_mode,
        step_keyword_alignment=alignment_mode,
        newline=newline_mode,
        fast=True if tag_line_mode == TagLineMode.CUSTOM.value else fast,
        tag_line_mode=tag_line_mode,
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
