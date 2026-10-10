import operator
from pathlib import Path
from dataclasses import dataclass, field as dataclasses_field
from typing import Any, ClassVar, Union

from .lists import SerializableList
from .mixins.export import ExportMixin


@dataclass
class ResourceModel(ExportMixin):
    """
    Keyword Arguments:
        path (Path): The path of the Resource.
        number (integer): Number of resource used according to 'prefix', commonly empty
            at object initialization then computed further..
        prefix (integer): New filename prefix, commonly empty at object initialization
            then computed further.
        original_prefix (string): Filename prefix as parsed from original path. It is
            almost unused, its role is more for history.
        name (string): Filename content as parsed from original path.
        parent (ResourceModel): Possible parent resource, it should never be a file.
        children (list): List of possible children Resource.
    """
    EXPORT_PRIVATES: ClassVar[tuple[str]] = ("parent",)
    EXPORT_PROPERTIES: ClassVar[tuple[str]] = ("built_name",)
    path: Path
    number: int = 0
    prefix: str = ""
    original_prefix: str = ""
    name: str = ""
    parent: Any = dataclasses_field(repr=False, default=None)
    children: Union[SerializableList, list] = dataclasses_field(
        repr=False,
        default_factory=SerializableList,
    )

    def __post_init__(self):
        if self.children and isinstance(self.children, list):
            self.children = SerializableList(self.children)

        # Automatically link sub objects relations
        if self.children:
            self.set_children(*self.children, from_init=True)

    @property
    def built_name(self):
        """
        Build name with prefix if not empty, else just the resource name.
        """
        if not self.prefix and not self.name:
            return self.path.name

        if not self.prefix:
            return self.name

        return self.prefix + "_" + self.name

    def set_children(self, *args, from_init=False):
        """
        Append resources as children while linking them to their parent.

        This is the recommended method to add children else you will have to perform
        addition and linking yourself for parent and children.

        Arguments:
            *children (ResourceModel): ResourceModel objects to set as children.

        Keyword Arguments:
            from_init (bool): If true this will not append objects to
                ``children`` attribute. This is only useful when calling this
                method from class init and avoid recursion. Default value is false.
        """
        if args:
            for item in args:
                item.parent = self

            if not from_init:
                self.children.extend(args)

    def children_directories(self):
        """
        Return only direct children directories.

        Returns:
            list: List of children resources.
        """
        return [v for v in self.children if v.path.is_dir()]

    def children_files(self):
        """
        Return only direct children files.

        Returns:
            list: List of children resources.
        """
        return [v for v in self.children if v.path.is_file()]

    def ordered_children(self):
        """
        Return children resources properly ordered.

        * Directories comes first;
        * Then files;
        * Dir and files are in ascending order;
        * Ordering with respect of their original file with prefix OR on parsed filename
          content (ignoring the original_prefix);

        Returns:
            list: List of children resources.
        """
        return (
            sorted(self.children_directories(), key=lambda x: x.path.name)
            + sorted(self.children_files(), key=lambda x: x.path.name)
        )

    def recursive_directories(self, directories=None):
        """
        Return a flat list of all directories from resource, recursively.

        Returns:
            list: A flat list of all children directories ordered on their path from
            leaf to the top, then ascending on name.
        """
        directories = [] if directories is None else directories

        for v in self.children_directories():
            directories.append(v)

            v.recursive_directories(directories=directories)

        order_per_name = sorted(directories, key=operator.attrgetter("built_name"))
        return sorted(
            order_per_name,
            key=operator.methodcaller("get_level"),
            reverse=True
        )

    def recursive_files(self, files=None):
        """
        Return a flat list of all files from resource, recursively.

        Returns:
            list: A flat list of all children files ordered on their path from leaf to
            the top, then ascending on name.
        """
        files = [] if files is None else files

        for v in self.children_files():
            files.append(v)

        for v in self.children_directories():
            v.recursive_files(files=files)

        order_per_name = sorted(files, key=operator.attrgetter("built_name"))
        return sorted(
            order_per_name,
            key=operator.methodcaller("get_level"),
            reverse=True
        )

    def is_root(self):
        """
        Returns True if resource has no parent and therefore is the root resource.
        """
        return self.parent is None

    def get_deep(self):
        """
        Recursively dig into children to count the deep.

        Note than files does not count to increment the deep.

        Returns:
            integer: The deep if resource has directory children else 0.
        """
        deep = 0

        dirs = self.children_directories()

        if dirs:
            # For the resource itself
            deep += 1
            # Get the most high deep through all children
            deep += max([child.get_deep() for child in dirs])

        return deep

    def get_level(self):
        """
        Recursively dig up into parents to count the level from root.

        File level is always one more than their parent directory level. It is a
        mistake to set a file as child of another file.

        Returns:
            integer: The deep if resource has parent directory else 0.
        """
        level = 0

        if self.parent:
            # For the resource itself
            level += 1
            # Get parent sum
            level += self.parent.get_level()

        return level
