from pathlib import Path
from typing import Iterable, Optional

import click
import yaml

CONFIG_FILE = ".reformat-gherkin.yaml"
SYSTEM_ROOT = Path("/").resolve()


def find_project_root(srcs: Iterable[str]) -> Path:
    """
    Return a directory containing .git, .hg, or .reformat-gherkin.yaml.

    That directory can be one of the directories passed in `srcs` or their
    common parent.

    If no directory in the tree contains a marker that would specify it's the
    project root, the root of the file system is returned.
    """
    if not srcs:
        return SYSTEM_ROOT

    common_base = min(Path(src).resolve() for src in srcs)
    if common_base.is_dir():
        # Append a dummy file so `parents` below returns `common_base_dir`, too.
        common_base /= "dummy-file"

    directory = SYSTEM_ROOT
    for directory in common_base.parents:
        if (directory / ".git").is_dir():
            return directory

        if (directory / ".hg").is_dir():
            return directory

        if (directory / CONFIG_FILE).is_file():
            return directory

    return directory  # pragma: no cover


def read_config_file(
    ctx: click.Context, _: click.Parameter, value: Optional[str]
) -> Optional[str]:
    """
    Inject the configuration from ".reformat-gherkin.yaml" into defaults in `ctx`.

    Returns the path to a successfully found and read configuration file, None
    otherwise.
    """
    if not value:
        root = find_project_root(ctx.params.get("src", ()))
        path = root / CONFIG_FILE
        if path.is_file():
            value = str(path.resolve())
        else:
            return None

    try:
        with open(value, "r") as f:
            config = yaml.safe_load(f)
    except (yaml.YAMLError, OSError) as e:
        raise click.FileError(
            filename=value, hint=f"Error reading configuration file: {e}"
        )

    if not config:
        return None

    if ctx.default_map is None:
        ctx.default_map = {}

    ctx.default_map.update(  # type: ignore  # bad types in .pyi
        {k.replace("--", "").replace("-", "_"): v for k, v in config.items()}
    )
    return value
