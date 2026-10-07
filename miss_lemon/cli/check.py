import json
import logging
from pathlib import Path

import click
from bigtree import Tree

from ..walker import DirWalker


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
    "--format",
    metavar="STRING",
    type=click.Choice(["json", "tree"]),
    help="Report output format name.",
    default="tree",
    show_default=True,
)
@click.pass_context
def check_command(context, source, format):
    """
    Proceed to analyze and prefix computation on a path and output a basic report.
    """
    logging.getLogger("miss-lemon")

    walker = DirWalker(source)

    root = walker.compute()

    if format == "json":
        print(root.as_json())

    if format == "tree":
        tree = Tree.from_nested_dict(
            json.loads(root.as_json()),
        )
        tree.show(alias="built_name")
