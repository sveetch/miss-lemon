import logging
from pathlib import Path

import click

from ..walker import DirWalker
from ..renamer import Renamer


@click.command()
@click.argument(
    "source",
    nargs=1,
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        path_type=Path,
        resolve_path=True,
    )
)
@click.option(
    "--step",
    type=click.INT,
    default=100,
    help=(
        "The lowest number slot step for the leaf resources."
    ),
)
@click.option(
    "--output",
    metavar="STRING",
    type=click.Choice(["mv", "git-mv"]),
    help="Command format name.",
    default="mv",
    show_default=True,
)
@click.pass_context
def rename_command(context, source, step, output):
    """
    Rename directories and files from a path with a computed number prefix.
    """
    logging.getLogger("miss-lemon")

    walker = DirWalker(source)

    root = walker.compute()

    renamer = Renamer(root)

    if output == "mv":
        output = renamer.with_shell_mv()
    elif output == "git-mv":
        output = renamer.with_shell_gitmv()

    click.echo(output)
