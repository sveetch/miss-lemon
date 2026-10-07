class Renamer:
    """
    TODO:
        The class that will output commands to apply resource renaming.

        At least with 'mv' or 'git mv' commands. To be moved safely we need:

        1. We always process distinctly the files first and then directories;
        2. Move leaf resources in first and go to the top;

        Resource model seems to need distinct methods to recursively get a flat list of
        directories and files, order on their path (from the leaf to the top).

        Possibly we would have another option to rename directly in Python without to
        perform commands.
    """
    def __init__(self, root):
        self.root = root

    def organize(self):
        """
        Gather all files and directories to rename.

        Returns:
            tuple: First item is for files and second one for the directories. Both
            items are a list of tuple, each tuple include the source and the
            destination (with new filename with prefix) of resource.
        """
        files = [
            (
                item.path.relative_to(self.root.path),
                item.path.relative_to(self.root.path).with_name(item.built_name),
            )
            for item in self.root.recursive_children_files()
        ]

        dirs = [
            (
                item.path.relative_to(self.root.path),
                item.path.relative_to(self.root.path).with_name(item.built_name),
            )
            for item in self.root.recursive_children_directories()
        ]

        return files, dirs

    def with_shell_mv(self, git=False):
        """
        Output shell commands to rename files and directories using either ``mv``
        command or ``git mv``command.

        Keyword Arguments:
            git (boolean): If enabled, the output command lines will be prefixed with
                ``git``.

        Returns:
            string: The command lines.
        """
        lines = [
            (
                "# This shell script will 'cd' into the source directory then apply "
                "renaming of resources."
            ),
            "cd '{}';".format(str(self.root.path).replace("'", "\'")),
        ]

        files, dirs = self.organize()

        command_name = "git mv" if git is True else "mv"

        for src, dst in (files + dirs):
            lines.append(
                "{cmd} '{src}' '{dst}';".format(
                    cmd=command_name,
                    src=str(src).replace("'", "\'"),
                    dst=str(dst).replace("'", "\'"),
                )
            )

        lines.append("echo \"Finished all tasks!\";")

        return "\n".join(lines) + "\n"

    def with_shell_gitmv(self):
        """
        Shortcut for ``with_shell_mv`` with Git prefix enabled.

        Returns:
            string: The command lines.
        """
        return self.with_shell_mv(git=True)
