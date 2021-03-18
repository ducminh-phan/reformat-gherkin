import sys
import traceback
from contextlib import nullcontext
from io import BytesIO, TextIOWrapper
from pathlib import Path
from typing import BinaryIO, ContextManager, Iterable, Iterator, Optional, Set, Tuple

from .ast_node import GherkinDocument
from .errors import (
    BaseError,
    EmptySources,
    EquivalentError,
    InternalError,
    NothingChanged,
    StableError,
)
from .formatter import LineGenerator
from .options import NewlineMode, Options, WriteBackMode
from .parser import parse
from .report import Report
from .utils import decode_stream, diff, dump_to_file, err

REPORT_URL = "https://github.com/ducminh-phan/reformat-gherkin/issues"

NEWLINE_FROM_OPTION = {NewlineMode.CRLF: "\r\n", NewlineMode.LF: "\n"}


def find_sources(src: Iterable[str]) -> Set[Path]:
    sources: Set[Path] = set()

    for s in src:
        path = Path(s).resolve()
        if path.is_dir():
            sources.update(path.rglob("*.feature"))
        elif path.is_file():
            # If a file was explicitly given, we don't care about its extension
            sources.add(path)
        else:  # pragma: no cover
            err(f"Invalid path: {s}")

    return sources


def reformat(src: Tuple[str], report: Report, *, options: Options):
    use_stdin = "-" in src
    sources = find_sources(filter((lambda it: it != "-"), src))

    if not sources and not use_stdin:
        raise EmptySources

    if use_stdin:
        changed = reformat_stdin(options=options)
        report.done("stdin", changed)

    for path in sources:
        try:
            changed = reformat_single_file(path, options=options)
            report.done(str(path), changed)
        except Exception as e:
            report.failed(path, str(e))


def reformat_stdin(*, options: Options) -> bool:
    output = sys.stdout.buffer if options.write_back == WriteBackMode.INPLACE else None
    return reformat_streams(sys.stdin.buffer, output, options=options)


def reformat_single_file(path: Path, *, options: Options) -> bool:
    with open(path, "rb") as f:
        in_stream = BytesIO(f.read())

    out_stream_cm: ContextManager[Optional[BinaryIO]]
    if options.write_back == WriteBackMode.INPLACE:
        out_stream_cm = open(path, "wb")
    else:
        out_stream_cm = nullcontext(None)

    with out_stream_cm as out_stream:
        return reformat_streams(in_stream, out_stream, options=options)


def reformat_streams(
    input: BinaryIO, output: Optional[BinaryIO], *, options: Options
) -> bool:
    src_contents, encoding, existing_newline = decode_stream(input)

    newline = NEWLINE_FROM_OPTION.get(options.newline, existing_newline)

    content_changed = True
    try:
        dst_contents = format_file_contents(src_contents, options=options)
    except NothingChanged:
        content_changed = False
        dst_contents = src_contents

    # We reformat the file if either the content is changed, or the line separators
    # need to be changed.
    if not content_changed and newline == existing_newline:
        return False

    if output is not None:
        tiow = TextIOWrapper(output, encoding=encoding, newline=newline)
        tiow.write(dst_contents)
        # Ensures that the underlying stream is not closed when the
        # TextIOWrapper is garbage collected, which wouldn't be good for stdout
        tiow.detach()

    return True


def format_file_contents(src_contents: str, *, options: Options) -> str:
    """
    Reformat the contents of a file and return new contents. Raise NothingChanged
    if the contents were not changed after reformatting.

    If `options.fast` is False, additionally confirm that the reformatted file is
    valid by calling :func:`assert_equivalent` and :func:`assert_stable` on it.
    """
    if src_contents.strip() == "":
        raise NothingChanged

    dst_contents = format_str(src_contents, options=options)
    if src_contents == dst_contents:
        raise NothingChanged

    if not options.fast:
        assert_equivalent(src_contents, dst_contents)
        assert_stable(src_contents, dst_contents, options=options)

    return dst_contents


def format_str(src_contents: str, *, options: Options) -> str:
    """
    Reformat a string and return new contents.
    """
    ast = parse(src_contents)

    line_generator = LineGenerator(
        ast, options.step_keyword_alignment, options.tag_line_mode, options.indent
    )
    lines = line_generator.generate()

    return "\n".join(lines)


def assert_equivalent(src: str, dst: str) -> None:
    """
    Raise EquivalentError if `src` and `dst` aren't equivalent.
    """

    def _v(ast: GherkinDocument) -> Iterator[str]:
        """
        Simple visitor generating strings to compare ASTs by content
        """
        for node in ast:
            yield repr(node)

    src_ast = parse(src)

    try:
        dst_ast = parse(dst)
    except BaseError as exc:
        log = dump_to_file("".join(traceback.format_tb(exc.__traceback__)), dst)
        raise InternalError(
            f"INTERNAL ERROR: Invalid file contents are produced:\n"
            f"{exc}\n"
            f"Please report a bug on {REPORT_URL}.\n"
            f"This invalid output might be helpful:\n"
            f"{log}\n"
        ) from exc

    src_ast_str = "\n".join(_v(src_ast))
    dst_ast_str = "\n".join(_v(dst_ast))

    if src_ast_str != dst_ast_str:
        log = dump_to_file(diff(src_ast_str, dst_ast_str, "src", "dst"))
        raise EquivalentError(
            f"INTERNAL ERROR: The new content produced is not equivalent to "
            f"the source.\n"
            f"Please report a bug on {REPORT_URL}.\n"
            f"This diff might be helpful: {log}\n"
        )


def assert_stable(src: str, dst: str, *, options: Options) -> None:
    """
    Raise StableError if `dst` reformats differently the second time.
    """
    new_dst = format_str(dst, options=options)
    if dst != new_dst:
        log = dump_to_file(
            diff(src, dst, "source", "first pass"),
            diff(dst, new_dst, "first pass", "second pass"),
        )
        raise StableError(
            f"INTERNAL ERROR: Different contents are produced on the second pass "
            f"of the formatter.\n"
            f"Please report a bug on {REPORT_URL}.\n"
            f"This diff might be helpful: {log}\n"
        ) from None
