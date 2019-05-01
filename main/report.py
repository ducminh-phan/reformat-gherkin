from pathlib import Path

import click
from attr import dataclass

from .utils import err, out


@dataclass
class Report:
    """Provides a reformatting counter. Can be rendered with `str(report)`."""

    check: bool
    change_count: int = 0
    same_count: int = 0
    failure_count: int = 0

    def done(self, path: Path, changed: bool) -> None:
        """Increment the counter for successful reformatting. Write out a message."""
        if changed:
            reformatted = "Would reformat" if self.check else "Reformatted"
            out(f"{reformatted} {path}")

            self.change_count += 1
        else:
            self.same_count += 1

    def failed(self, path: Path, message: str) -> None:
        """Increment the counter for failed reformatting. Write out a message."""
        err(f"Error: cannot format {path}: {message}")
        self.failure_count += 1

    @property
    def return_code(self) -> int:
        """Return the exit code that the app should use.

        This considers the current state of changed files and failures:
        - if there were any failures, return 123;
        - if any files were changed and --check is being used, return 1;
        - otherwise return 0.
        """
        # According to http://tldp.org/LDP/abs/html/exitcodes.html starting with
        # 126 we have special return codes reserved by the shell.
        if self.failure_count:
            return 123

        elif self.change_count and self.check:
            return 1

        return 0

    def __str__(self) -> str:
        """Render a color report of the current state.

        Use `click.unstyle` to remove colors.
        """
        if self.check:
            reformatted = "would be reformatted"
            unchanged = "would be left unchanged"
            failed = "would fail to reformat"
        else:
            reformatted = "reformatted"
            unchanged = "left unchanged"
            failed = "failed to reformat"

        report_lines = []
        if self.change_count:
            s = "s" if self.change_count > 1 else ""
            report_lines.append(
                click.style(f"{self.change_count} file{s} {reformatted}", bold=True)
            )
        if self.same_count:
            s = "s" if self.same_count > 1 else ""
            report_lines.append(f"{self.same_count} file{s} {unchanged}")
        if self.failure_count:
            s = "s" if self.failure_count > 1 else ""
            report_lines.append(
                click.style(f"{self.failure_count} file{s} {failed}", fg="red")
            )
        return ", ".join(report_lines) + "."
