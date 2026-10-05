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
    type=click.Path(exists=True, path_type=Path)
)
@click.pass_context
def order_command(context, source):
    """
    Order directories and files with a prefix number.

    TODO

    * Need option to exclude dir/file patterns

    """
    # logger =
    logging.getLogger("miss-lemon")

    click.echo("Hello")
    walker = DirWalker(source)

    root = walker.compute()

    print("AS JSON:")
    print(root.as_json())
    print()

    print("AS TREE:")
    tree = Tree.from_nested_dict(
        json.loads(root.as_json()),
        # name_key="built_name",
    )
    tree.show(alias="built_name")
    print()
