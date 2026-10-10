from pathlib import Path

try:
    from rich.tree import Tree as RichTree
except ImportError:
    RichTree = None

from bigtree import Node, Tree


class DiffTree:
    """
    Compute differences between original and renamed resource tree.

    Arguments:
        source_first (boolean): If enabled, the diff output will print the source first
            then the renamed name. If disabled (the default) the renamed name is
            printed first.

    .. Note::
        Because the diff process list the original source, the tree order will not be
        ordered like the changes preview.
    """
    def __init__(self, source_first=False):
        self.source_first = source_first

    def build_flat_tree(self, root):
        """
        Build a flat dict of all root resources.

        Arguments:
            resource (ResourceModel): Resource object.

        Returns:
            dict: Dict of resources, item key is indexed the resource relative (to the
            root) path and item value is the resource object.
        """
        return {
            str(item.path): {"resource": item}
            for item in root.recursive_directories() + root.recursive_files()
        }

    def diff_resource(self, resource, changes=None):
        """
        Get difference from original resources name to computed resource.

        Arguments:
            resource (ResourceModel): Resource object before computation.

        Keyword Arguments:
            changes (dict): Flat dict of paths that have been collected (with user
                options) then computed.

        Returns:
            dict: A dictionnary with diff data items 'status', 'from' and 'to'. 'to'
            can be None if resource has been ignored from collection with user options.
        """
        status = "ignored"
        to = None

        # No preview, the resource has not be computed because of exclusion/ignore
        if changes:
            to = changes["resource"].built_name

            # Resource has been computed but lead to the same resource name
            if resource.path.name == to:
                status = "identical"
            # Resource has been computed and lead to a new name
            else:
                status = "changed"

        return {
            "status": status,
            "from": resource.path.name,
            "to": to,
        }

    def get_ascii_label(self, resource, changes=None):
        """
        Build a resource label in proper ASCII.

        Arguments:
            resource (ResourceModel): Resource object before computation.

        Keyword Arguments:
            changes (dict): Flat dict of paths that have been collected (with user
                options) then computed.

        Returns:
            string: The built label.
        """
        diff = self.diff_resource(resource, changes)

        if diff["status"] == "ignored":
            return "{} (IGNORED)".format(diff["from"])
        elif diff["status"] == "identical":
            return "{} (SAME)".format(diff["from"])

        if self.source_first:
            tpl = "{old} -> {new}"
        else:
            tpl = "{new} <- {old}"

        return tpl.format(old=diff["from"], new=diff["to"])

    def get_rich_label(self, resource, changes=None):
        """
        Build a resource label with Rich syntax.

        Arguments:
            resource (ResourceModel): Resource object before computation.

        Keyword Arguments:
            changes (dict): Flat dict of paths that have been collected (with user
                options) then computed.

        Returns:
            string: The built label.
        """
        diff = self.diff_resource(resource, changes)

        if diff["status"] == "ignored":
            return "[yellow]{} (IGNORED)".format(diff["from"])
        elif diff["status"] == "identical":
            return "{} (SAME)".format(diff["from"])

        if self.source_first:
            tpl = "{old} -> [green]{new}[/green]"
        else:
            tpl = "[green]{new}[/green] <- {old}"

        return tpl.format(old=diff["from"], new=diff["to"])

    def add_rich_children_node(self, parent, resource, changes):
        """
        Recursively attach resource and its children to the parent node.

        Arguments:
            parent (rich.Tree): Parent tree object where to attach resource.
            resource (ResourceModel): Resource object to attach.
            changes (dict): Flat dict of paths that have been collected (with user
                options) then computed.
        """
        node = parent.add(
            self.get_rich_label(
                resource,
                changes.get(str(resource.path), None)
            )
        )

        for child in resource.ordered_children():
            self.add_rich_children_node(node, child, changes)

    def build_richtree(self, original_root, changes_root):
        """
        Build a Rich Tree ready to display.

        Arguments:
            original_root (ResourceModel): The resource object of the original
                collected root (before computation).
            changes_root (ResourceModel): The resource object of the computed root.

        Returns:
            rich.Tree: The Rich tree object of root resource.
        """
        if RichTree is None:
            raise ValueError("The 'Rich' stack is not installed.")

        # originals = self.build_flat_tree(original_root)
        changes = self.build_flat_tree(changes_root)

        tree = RichTree(str(original_root.path))

        for child in original_root.ordered_children():
            self.add_rich_children_node(tree, child, changes)

        return tree

    def build_bigtree(self, original_root, changes_root):
        """
        Build a Big Tree ready to display.

        Arguments:
            original_root (ResourceModel): The resource object of the original
                collected root (before computation).
            changes_root (ResourceModel): The resource object of the computed root.

        Returns:
            bigtree.Tree: The Bigtree object of root resource.
        """
        tree = Tree(
            Node(str(original_root.path.name))
        )
        basenodepath = original_root.path.parent

        originals = self.build_flat_tree(original_root)
        changes = self.build_flat_tree(changes_root)

        tree.add_dict_by_path({
            str(Path(k).relative_to(basenodepath)): {
                "label": self.get_ascii_label(
                    v["resource"],
                    changes.get(str(v["resource"].path), None)
                )
            }
            for k, v in originals.items()
        })

        return tree
