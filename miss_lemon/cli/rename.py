from pathlib import Path

from ..walker import DirWalker
from ..renamer import Renamer

try:
    import rich_click as click
except ImportError:
    import click


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
    metavar="INTEGER",
    show_default=True,
    type=click.INT,
    default=100,
    help=(
        "The lowest number slot step for the leaf resources."
    ),
)
@click.option(
    "--command",
    metavar="NAME",
    show_default=True,
    type=click.Choice(["mv", "git-mv"]),
    help="Command name. All resource renaming lines will use this command.",
    default="mv",
)
@click.option(
    "--unprefixed",
    is_flag=True,
    help=(
        "Allows to collect all resource even if they don't match the regex for "
        "\"filename with prefix\" (eg: '0001_foo'). Default behavior when this option "
        "is not enabled, is to ignore those files without prefix, they won't be "
        "renamed. This is commonly used with '--exclude' to prevent some resources to "
        "be renamed."
    ),
)
@click.option(
    "--excludes",
    metavar="PATTERN",
    multiple=True,
    help=(
        "Define a 'Unix filename pattern'(compatible with Python module 'fnmatch') to "
        "exclude resources from collect. This can be defined multiple times."
    ),
)
@click.pass_context
def rename_command(context, source, step, command, unprefixed, excludes):
    """
    Rename resources (directories and files) from a path with a computed number prefix.
    """
    logger = context.obj["logger"]

    logger.debug("Working on: {}".format(source))
    logger.debug("Selected command: {}".format(command))
    logger.debug("Collecting resource without prefix: {}".format(unprefixed))
    if excludes:
        logger.debug("Excludes: {}".format(", ".join(excludes)))

    walker = DirWalker(source, allow_unprefixed=unprefixed, excludes=excludes)

    root = walker.compute(step=step)

    renamer = Renamer(root)

    if command == "mv":
        cmd_output = renamer.with_shell_mv()
    elif command == "git-mv":
        cmd_output = renamer.with_shell_gitmv()

    click.echo(cmd_output)
