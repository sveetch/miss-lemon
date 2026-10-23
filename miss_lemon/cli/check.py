from pathlib import Path

from ..diff import DiffTree
from ..exceptions import NoAvailableResource
from ..walker import DirWalker

# On default rich is not present in outputs and may become available further
AVAILABLE_OUTPUTS = ["json", "tree"]
# On default Big tree output is prefered
DEFAULT_OUTPUT = "tree"
# First try to get Rich stack, fallback to basic Click and BigTree
try:
    import rich_click as click
except ImportError:
    import click
else:
    from rich import print as RichPrint
    # Append Rich to output and make it the default one
    AVAILABLE_OUTPUTS.append("rich")
    DEFAULT_OUTPUT = "rich"


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
    "--output",
    metavar="NAME",
    show_default=True,
    type=click.Choice(AVAILABLE_OUTPUTS),
    help=(
        "Report output format name. 'json' will print a dictionnary of computed "
        "resources. 'tree' and 'rich' are similar but the latter one "
        "is only allowed if the rich stack has been installed, it will provide colored "
        "nodes (according to their status). Both will print a tree of differences "
        "between original and renamed tree"
    ),
    default=DEFAULT_OUTPUT,
)
@click.option(
    "--unprefixed",
    is_flag=True,
    help=(
        "Allows to collect all resource even if they don't match the regex for "
        "\"filename with prefix\" (eg: '0001_foo'). Default behavior when this option "
        "is not enabled, is to ignore those files without prefix, they won't be "
        "renamed. This is commonly used with '--excludes' to prevent some resources to "
        "be renamed."
    ),
)
@click.option(
    "--excludes",
    metavar="PATTERN",
    show_default=True,
    multiple=True,
    help=(
        "Define a 'Unix filename pattern'(compatible with Python module 'fnmatch') to "
        "exclude resources from collect. This can be defined multiple times."
    ),
)
@click.option(
    "--from-original",
    is_flag=True,
    help=(
        "If enabled, the tree will display the original name first then the renamed "
        "name. On default the renamed name is printed first."
    ),
)
@click.option(
    "--display-ignored",
    "display_ignored",
    is_flag=True,
    help="Enable display of collected 'ignored' resources in tree.",
)
@click.option(
    "--exit-1",
    "exit_signal",
    is_flag=True,
    help=(
        "Command will exist with signal code 1 if there is one or more resources to "
        "rename."
    ),
)
@click.pass_context
def check_command(context, source, step, output, unprefixed, excludes, from_original,
                  display_ignored, exit_signal):
    """
    Proceed to analyze and prefix computation on a path then output a report.

    This does not write or rename anything.

    The preview report can be either a JSON payload or a tree of the original structure
    including a preview of renaming that would occurs with the command 'rename'.
    """
    logger = context.obj["logger"]

    logger.debug("Working on: {}".format(source))
    logger.debug("Select output: {}".format(output))
    logger.debug("Collecting resource without prefix: {}".format(unprefixed))
    if excludes:
        logger.debug("Excludes: {}".format(", ".join(excludes)))

    hidden_status = []
    if not display_ignored:
        hidden_status.append("ignored")

    logger.debug("Hidden status: {}".format(hidden_status or None))

    # Collect and compute with user options
    new_walker = DirWalker(source, allow_unprefixed=unprefixed, excludes=excludes)
    new_root = new_walker.compute(step=step)

    # Just print output as simple JSON
    if output == "json":
        click.echo(new_root.as_json())
        return

    # Other output formats involve a diff between original and changes preview
    differ = DiffTree(source_first=from_original, hidden_status=hidden_status)

    # Collect the full structure without any exclusions (ignoring user options)
    original_walker = DirWalker(source, allow_unprefixed=True)
    original_root = original_walker.collect()

    # Print tree preview with differences report
    try:
        if output == "tree":
            built = differ.build_bigtree(original_root, new_root)
        elif output == "rich":
            built = differ.build_richtree(original_root, new_root)
    except NoAvailableResource:
        click.echo("Nothing to rename.")
    else:
        if output == "tree":
            click.echo("🎨 Big Tree preview")
            click.echo(built.show(alias="label"))
        elif output == "rich":
            click.echo("🎨 Rich tree preview")
            RichPrint(built)
        # Exit error signal if enabled from option
        if exit_signal:
            raise click.Abort
