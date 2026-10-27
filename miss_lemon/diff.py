from pathlib import Path

try:
    from rich.tree import Tree as RichTree
except ImportError:
    RichTree = None

from bigtree import Node, Tree

from .exceptions import NoAvailableResource


class DiffTree:
    """
    Compute differences between original and renamed resource tree.

    Arguments:
        source_first (boolean): If enabled, the diff output will print the source first
            then the renamed name. If disabled (the default) the renamed name is
            printed first.
        hidden_status (list): List of resource diff status name to ignore from output.
            On default this is only ``ignored``.

    .. Note::
        Because the diff process lists the original source, the tree order will not be
        ordered like the changes preview.
    """
    def __init__(self, source_first=False, hidden_status=None):
        self.source_first = source_first
        self.hidden_status = [] if hidden_status is None else hidden_status

    def build_flat_tree(self, root):
        """
        Build a flat dict of all root resources.

        Arguments:
            root (ResourceModel): Resource object.

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
            dict: A dictionnary with diff data items 'status', 'from' (Path object) and
            'to' (Path name string). 'to' can be None if resource has been ignored from
            collection with user options.
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
            "from": resource.path,
            "to": to,
        }

    def get_ascii_label(self, diff):
        """
        Build a resource label in proper ASCII.

        Arguments:
            diff (dict): Computed difference infos as returned from
                ``DiffTree.diff_resource()``.

        Keyword Arguments:
            changes (dict): Flat dict of paths that have been collected (with user
                options) then computed.

        Returns:
            string: The built label.
        """
        source = diff["from"].name + "/" if diff["from"].is_dir() else diff["from"].name
        dest = diff["to"] or ""
        if diff["from"].is_dir():
            dest = dest + "/"

        if diff["status"] == "ignored":
            return "{} (IGNORED)".format(source)
        elif diff["status"] == "identical":
            return "{} (SAME)".format(source)

        if self.source_first:
            tpl = "{old} -> {new}"
        else:
            tpl = "{new} <- {old}"

        return tpl.format(old=source, new=dest)

    def get_rich_label(self, diff):
        """
        Build a resource label with Rich syntax.

        Arguments:
            diff (dict): Computed difference infos as returned from
                ``DiffTree.diff_resource()``.

        Returns:
            string: The built label.
        """
        source = diff["from"].name + "/" if diff["from"].is_dir() else diff["from"].name
        dest = diff["to"] or ""
        if diff["from"].is_dir():
            dest = dest + "/"

        if diff["status"] == "ignored":
            return "[yellow]{} (IGNORED)".format(source)
        elif diff["status"] == "identical":
            return "{} (SAME)".format(source)

        if self.source_first:
            tpl = "{old} -> [green]{new}[/green]"
        else:
            tpl = "[green]{new}[/green] <- {old}"

        return tpl.format(old=source, new=dest)

    def add_rich_children_node(self, parent, resource, changes, eligibles=None):
        """
        Recursively attach resource and its children to the parent node.

        Arguments:
            parent (rich.Tree): Parent tree object where to attach resource.
            resource (ResourceModel): Resource object to attach.
            changes (dict): Flat dict of paths that have been collected (with user
                options) then computed.
            eligibles (list): A list where to add eligible resources.
        """
        eligibles = [] if eligibles is None else eligibles

        diff = self.diff_resource(resource, changes.get(str(resource.path), None))

        # Ignore resource with a status to hide
        if diff["status"] in self.hidden_status:
            return

        # Add eligible resource node label as parent child
        node = parent.add(
            self.get_rich_label(diff)
        )

        if diff["status"] not in ("ignored", "identical"):
            eligibles.append(diff["from"])

        # Dig into the node children
        for child in resource.ordered_children():
            self.add_rich_children_node(node, child, changes, eligibles=eligibles)

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

        # Build a flat tree of computed resources
        changes = self.build_flat_tree(changes_root)

        # Start tree with root
        tree = RichTree(str(original_root.path))

        # Then recursively append children
        eligibles = []
        for child in original_root.ordered_children():
            self.add_rich_children_node(tree, child, changes, eligibles=eligibles)

        if not eligibles:
            raise NoAvailableResource("No available resource.")

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
        basenodepath = original_root.path.parent

        changes = self.build_flat_tree(changes_root)

        # Start tree with root
        tree = Tree(
            Node(
                str(original_root.path.name),
                label=str(original_root.path),
                diff={}
            )
        )

        # Then build a flat dict to digest by Big Tree, each item key must be a path
        # under the root path
        children_nodes = {}
        for k, v in self.build_flat_tree(original_root).items():
            node_key = str(Path(k).relative_to(basenodepath))
            diff = self.diff_resource(
                v["resource"],
                changes.get(str(v["resource"].path), None)
            )

            # Don't store resource or its children if resource is ignored
            if diff["status"] in self.hidden_status:
                continue

            children_nodes[node_key] = {
                "diff": diff,
                "label": self.get_ascii_label(diff)
            }

        # Check if there is at least one eligible resource else raise error
        valid = [
            k
            for k, v in children_nodes.items()
            if v["diff"]["status"] not in ("ignored", "identical")
        ]
        if not valid:
            raise NoAvailableResource("No available resource.")

        # If there is some children nodes to display
        if children_nodes:
            tree.add_dict_by_path(children_nodes)

        return tree
