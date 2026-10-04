import json
from pathlib import Path
from dataclasses import (
    dataclass,
    field as dataclasses_field,
    fields as dataclasses_fields,
)
from typing import Any, ClassVar

from ..utils.jsons import ExtendedJsonEncoder


@dataclass
class ResourceModel:
    """
    Keyword Arguments:
        path (Path): The path of the Resource.
        number (integer): Number of resource used according to 'prefix'.
        prefix (integer): New filename prefix.
        original_prefix (string): Filename prefix as parsed from original path. It is
            almost unused.
        name (string): Filename content as parsed from original path.
        parent (ResourceModel): Possible parent resource, it should never be a file.
        children (list): List of possible children Resource.
    """
    EXPORT_PRIVATES: ClassVar[list[str]] = ["parent"]
    path: Path
    number: int = 0
    prefix: str = ""
    original_prefix: str = ""
    name: str = ""
    parent: Any = dataclasses_field(repr=False, default=None)
    children: list[Any] = dataclasses_field(repr=False, default_factory=list)

    def __post_init__(self):
        # Automatically link sub objects relations
        if self.children:
            self.set_children(*self.children, from_init=True)

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

    def serialize(self, coerced=False):
        """
        A safe way to convert to a dict without recursion issues.

        Keyword Arguments:
            coerced (bool): If enabled all values with a method ``serialize()``
                will use it instead of returning model object. This is almost only
                implemented internally in Deovi models so you can get an output of
                ``serialize()`` only with Python builtin types.

        Returns:
            dict: This model object attribute serialized in a dictionnary, items named
                after one of names from EXPORT_PRIVATES won't be in the output.
        """
        return {
            f.name: (
                getattr(self, f.name).serialize(coerced=coerced)
                if coerced is True and hasattr(getattr(self, f.name), "serialize")
                else getattr(self, f.name)
            )
            for f in dataclasses_fields(self)
            if f.name not in self.EXPORT_PRIVATES
        }

    def children_directories(self):
        """
        Return only children directories.

        Returns:
            list: List of children resources.
        """
        return [v for v in self.children if v.path.is_dir()]

    def children_files(self):
        """
        Return only children files.

        Returns:
            list: List of children resources.
        """
        return [v for v in self.children if v.path.is_file()]

    def ordered_children(self):
        """
        Return children properly ordered.

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

    def as_coerced(self):
        """
        A shortcut to returns the output of ``serialize()`` with ``coerced`` option
        enabled.
        """
        return self.serialize(coerced=True)

    def as_json(self):
        """
        Returns the output of ``serialize()`` in a JSON string.
        """
        return json.dumps(self.serialize(), indent=4, cls=ExtendedJsonEncoder)
