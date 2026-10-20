import fnmatch
import logging
import math
import operator
import re

from . import __pkgname__
from .models.resource import ResourceModel


class DirWalker:
    """
    Recursively walk into a path to find its resources.

    Arguments:
        basepath (Path): The path where to collect resources.

    Keyword Arguments:
        file_pattern (re.Pattern): Compiled regex to match filename prefix and name.
            The regex pattern must include groups ``original_prefix`` and ``name``.
        allow_unprefixed (boolean): If enabled, resource that don't match are collected
            also but they won't never have a "original_prefix" (which won't avoid them
            to have a proper built prefix).
        excludes (list): A list of "Unix filename patterns" (with fnmatch) to exclude
            resources that match any of them.
    """
    DEFAULT_FILE_PATTERN = re.compile(
        r"(?P<original_prefix>[0-9]+)_(?P<name>[\S]+)"
    )

    def __init__(self, basepath, file_pattern=None, allow_unprefixed=False,
                 excludes=None):
        self.logger = logging.getLogger(__pkgname__)
        self.basepath = basepath.resolve(strict=True)
        self.file_pattern = file_pattern or self.DEFAULT_FILE_PATTERN
        self.allow_unprefixed = allow_unprefixed
        self.excludes = excludes or []

    def is_ignored(self, path):
        """
        Check if resource is hidden or protected to ignore.

        * Hidden resource name starts with ``.``;
        * Protected resource name starts with ``_``;

        Results:
            boolean: False if the path is not to ignore, else True.
        """
        return (
            path.name.startswith(".")
            or path.name.startswith("_")
        )

    def is_excluded(self, path):
        """
        Exclude path if its path (relative to 'basepath') match one of exclusion
        patterns.

        Results:
            boolean: False if the path is not excluded, else True.
        """
        relative = path.relative_to(self.basepath)

        for item in self.excludes:
            if fnmatch.fnmatch(relative, item):
                return True

        return False

    def get_resource(self, path):
        """
        Get Resource object for path if it is eligible to collect.

        Results:
            ResourceModel: The resource object if path was eligible else returns False.
        """
        if self.is_ignored(path):
            return False

        if self.is_excluded(path):
            return False

        matched = self.file_pattern.match(path.name)

        if matched:
            return ResourceModel(
                path=path,
                original_prefix=matched.group("original_prefix"),
                name=matched.group("name"),
            )
        elif self.allow_unprefixed:
            return ResourceModel(
                path=path,
                name=path.name,
            )

        self.logger.debug("Ignored resource (from pattern): {}".format(path.name))

        return False

    def recursive_path_walk(self, path):
        """
        Recursively collect all eligible resources from a path.

        Arguments:
            path (Path): Path object to scan for resources.

        Returns:
            list: List of ResourceModel objects. This is sorted on the original path
            name, meaning it will respect the original order.
        """
        resources = []

        files = sorted(
            [v for v in path.iterdir() if v.is_file()],
            key=operator.attrgetter("name")
        )
        dirs = sorted(
            [v for v in path.iterdir() if v.is_dir()],
            key=operator.attrgetter("name")
        )

        for item in dirs + files:
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
        root = ResourceModel(path=self.basepath, name=self.basepath.name)
        root.set_children(*self.recursive_path_walk(self.basepath))

        return root

    def get_increments(self, step, maxdeep):
        """
        Compute the range of prefix incrementation for all resources.

        Arguments:
            step (integer): Step is the minimum value of a prefix for the leaf nodes in
                the resource tree. Such as step value 100, allow leafs from 101 to 199.
                Step value 10 allows leafs from 11 to 19. Etc..
            maxdeep (integer): Maximum deep level in ressource tree.

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

        Arguments:
            step (integer): Step is the minimum value of a prefix for the leaf nodes in
                the resource tree. Such as step value 100, allow leafs from 101 to 199.
                Step value 10 allows leafs from 11 to 19. Etc..
            maxdeep (integer): Maximum deep level in ressource tree.

        Returns:
            integer: Length calculated on basis of step (as a decimal number) which is
            incremented with maxdeep value.
        """
        return int(maxdeep + math.log10(step) + 1)

    def compute_resource(self, resource):
        """
        Compute the prefix data for a resource object.

        Arguments:
            resource (ResourceModel): The resource object to patch.

        Returns:
            ResourceModel: The patched resource object. However it is almost useless
            because the object is mutated in place.
        """
        level = resource.get_level()

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
            resource.number = resource.parent.number + (
                self.increments[level] * position
            )
            resource.prefix = str(resource.number).zfill(self.matrix_length)
            self.compute_resource(resource)

        # Patch files with their computed prefix
        for position, resource in enumerate(files, start=1):
            resource.number = resource.parent.number + position
            resource.prefix = str(resource.number).zfill(self.matrix_length)

        return resource

    def compute(self, step=100):
        """
        Compute prefix data for collected resources.

        Keyword Arguments:
            step (integer): Step is the minimum value of a prefix for the leaf nodes in
                the resource tree. Such as step value 100, allow leafs from 101 to 199.
                Step value 10 allows leafs from 11 to 19. Etc..

        Returns:
            ResourceModel: The root resource.
        """
        root = self.collect()

        self.maxdeep = root.get_deep()
        self.matrix_length = self.get_prefix_matrix(step, self.maxdeep)
        self.increments = self.get_increments(step, self.maxdeep)

        self.compute_resource(root)

        return root
