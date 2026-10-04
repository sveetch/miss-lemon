"""
TODO:

A script which allow to perform test renaming to increase or decrease their number
prefix.

Eg: ::

    010_foo
    020_bar

Could be turned to: ::

    00010_foo
    00020_bar

Would build data to generate a shell script to apply renaming, either with "mv" or
"git mv" command.
"""
import logging
import math
import re

from . import __pkgname__
from .models.resource import ResourceModel


class DirWalker:
    DEFAULT_FILE_PATTERN = re.compile(
        r"(?P<original_prefix>[0-9]+)_(?P<name>[\S]+)"
    )

    def __init__(self, basepath, file_pattern=None):
        self.logger = logging.getLogger(__pkgname__)
        self.basepath = basepath.resolve(strict=True)
        self.file_pattern = file_pattern or self.DEFAULT_FILE_PATTERN

    def is_ignored_file(self, path):
        """
        Check if resource is hidden or protected to ignore.

        * Hidden resource name starts with ``.``;
        * Protected resource name starts with ``_``;

        """
        return (
            path.name.startswith(".")
            or path.name.startswith("_")
        )

    def get_resource(self, path):
        """
        Parse resource with regex pattern to validate it then return a Resource object.
        """
        matched = self.file_pattern.match(path.name)

        if matched:
            return ResourceModel(
                path=path,
                original_prefix=matched.group("original_prefix"),
                name=matched.group("name"),
            )

        self.logger.warning("Invalid pattern for: {}".format(path.name))

        return False

    def recursive_path_walk(self, path):
        """
        Recursively collect all eligible resources from a path.

        Arguments:
            path (Path): Path object to scan for resources.

        Returns:
            list: List of ResourceModel objects.
        """
        resources = []

        for item in path.iterdir():
            if self.is_ignored_file(item):
                continue

            resource = self.get_resource(item)

            if not resource:
                continue

            resources.append(resource)

            if item.is_dir():
                resource.set_children(*self.recursive_path_walk(item))

        return resources

    def collect(self):
        """
        Collect all resources from given root base path.

        Returns:
            ResourceModel: The root resource.
        """
        root = ResourceModel(path=self.basepath)
        root.set_children(*self.recursive_path_walk(self.basepath))

        return root

    def get_increments(self, step, maxdeep):
        """
        Compute the range of prefix incrementation for all resources.

        Returns:
            list: A list of integer for all incrementation, return in the order from
            root to leaf.
        """
        increments = [(step * (10 ** v)) for v in list(range(0, maxdeep))]
        increments.reverse()
        return increments

    def get_prefix_matrix(self, step, maxdeep):
        """
        Calculate the length of the prefix matrix.
        """
        return int(maxdeep + math.log10(step) + 1)

    def compute_resource(self, resource):
        level = resource.get_level()
        # print(("  " * level) + "  ➖ computed:", resource.path.name)
        # print(("  " * level) + "  ➖ level:", level)

        files = sorted(
            [v for v in resource.children if v.path.is_file()],
            key=lambda x: x.path.name
        )
        dirs = sorted(
            [v for v in resource.children if v.path.is_dir()],
            key=lambda x: x.path.name
        )

        # Patch directories with their computed prefix
        for position, resource in enumerate(dirs, start=1):
            resource.number = resource.parent.number + (self.increments[level] * position)
            resource.prefix = str(resource.number).zfill(self.matrix_length)
            # print(("  " * level) + "  📌", resource.prefix, resource.name)
            self.compute_resource(resource)

        # Patch files with their computed prefix
        for position, resource in enumerate(files, start=1):
            resource.number = resource.parent.number + position
            resource.prefix = str(resource.number).zfill(self.matrix_length)
            # print(("  " * level) + "  🔖", resource.prefix, resource.name)

    def compute(self, step=100):
        """
        Compute prefix data for each collected resource.

        So we want something like this to be computed: ::

        structure/
        ├── 01000_core
        ├── 02000_models
        │   └── 02100_managers
        └── 03000_forms

        Keyword Arguments:
            step (integer): Define the lowest limit of prefix for the leaf items. Each
                parent will increase this value according to their level. Such as for
                a step of 10, the leaf prefixes would be like between '10' and '19',
                then direct parent would be between '100' and '190', etc..

        Returns:
            ResourceModel: The root resource.
        """
        root = self.collect()

        self.maxdeep = root.get_deep()
        self.matrix_length = self.get_prefix_matrix(step, self.maxdeep)
        self.increments = self.get_increments(step, self.maxdeep)

        self.compute_resource(root)

        return root