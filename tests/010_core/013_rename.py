from pathlib import Path

from miss_lemon.walker import DirWalker
from miss_lemon.renamer import Renamer


def test_organize(caplog, settings):
    """
    Method should return a list of files and a list of directories where each resource
    is a tuple of source and destination paths, relatively to the root path.
    """
    structure = settings.datas_path / "basic_structure"
    walker = DirWalker(structure)

    root = walker.compute()

    renamer = Renamer(root)
    files, dirs = renamer.organize()

    assert files == [
        (
            Path("0100_models/001_managers/001_blog.py"),
            Path("0100_models/001_managers/01101_blog.py"),
        ),
        (
            Path("0100_models/001_managers/002_article.py"),
            Path("0100_models/001_managers/01102_article.py"),
        ),
        (
            Path("010_base/030_cool.bak.py"),
            Path("010_base/02002_cool.bak.py"),
        ),
        (
            Path("010_base/010_ok.txt"),
            Path("010_base/02001_ok.txt"),
        ),
        (
            Path("0100_models/0101_blog.py"),
            Path("0100_models/01001_blog.py"),
        ),
        (
            Path("0100_models/010_base.py"),
            Path("0100_models/01004_base.py"),
        ),
        (
            Path("0100_models/0103_category.py"),
            Path("0100_models/01003_category.py"),
        ),
        (
            Path("0100_models/0102_article.py"),
            Path("0100_models/01002_article.py"),
        ),
        (
            Path("0500_forms/502_article.py"),
            Path("0500_forms/04001_article.py"),
        ),
        (
            Path("020_foo.py"),
            Path("00001_foo.py"),
        ),
        (
            Path("1020_bar.py"),
            Path("00002_bar.py"),
        ),
    ]

    assert dirs == [
        (
            Path("0100_models/002_lookups"),
            Path("0100_models/01200_lookups"),
        ),
        (
            Path("0100_models/001_managers"),
            Path("0100_models/01100_managers"),
        ),
        (
            Path("1000_views"),
            Path("05000_views"),
        ),
        (
            Path("010_base"),
            Path("02000_base"),
        ),
        (
            Path("0200_empty"),
            Path("03000_empty"),
        ),
        (
            Path("0100_models"),
            Path("01000_models"),
        ),
        (
            Path("0500_forms"),
            Path("04000_forms"),
        ),
    ]


def test_with_shell_mv(caplog, settings):
    """
    Method should output all command lines to rename resources using command 'mv'.
    """
    structure = settings.datas_path / "basic_structure"
    walker = DirWalker(structure)

    root = walker.compute()

    renamer = Renamer(root)
    output = renamer.with_shell_mv()

    assert output == (
        "# This shell script will 'cd' into the source directory then apply renaming "
        "of resources.\n"
        "cd '{}';\n"
        "mv '0100_models/001_managers/001_blog.py' "
        "'0100_models/001_managers/01101_blog.py';\n"
        "mv '0100_models/001_managers/002_article.py' "
        "'0100_models/001_managers/01102_article.py';\n"
        "mv '010_base/030_cool.bak.py' '010_base/02002_cool.bak.py';\n"
        "mv '010_base/010_ok.txt' '010_base/02001_ok.txt';\n"
        "mv '0100_models/0101_blog.py' '0100_models/01001_blog.py';\n"
        "mv '0100_models/010_base.py' '0100_models/01004_base.py';\n"
        "mv '0100_models/0103_category.py' '0100_models/01003_category.py';\n"
        "mv '0100_models/0102_article.py' '0100_models/01002_article.py';\n"
        "mv '0500_forms/502_article.py' '0500_forms/04001_article.py';\n"
        "mv '020_foo.py' '00001_foo.py';\n"
        "mv '1020_bar.py' '00002_bar.py';\n"
        "mv '0100_models/002_lookups' '0100_models/01200_lookups';\n"
        "mv '0100_models/001_managers' '0100_models/01100_managers';\n"
        "mv '1000_views' '05000_views';\n"
        "mv '010_base' '02000_base';\n"
        "mv '0200_empty' '03000_empty';\n"
        "mv '0100_models' '01000_models';\n"
        "mv '0500_forms' '04000_forms';\n"
        "echo \"Finished all tasks!\";\n"
    ).format(structure)


def test_with_shell_gitmv(caplog, settings):
    """
    Method should output all command lines to rename resources using command 'git mv'.
    """
    structure = settings.datas_path / "basic_structure"
    walker = DirWalker(structure)

    root = walker.compute()

    renamer = Renamer(root)
    output = renamer.with_shell_gitmv()

    assert output == (
        "# This shell script will 'cd' into the source directory then apply renaming "
        "of resources.\n"
        "cd '{}';\n"
        "git mv '0100_models/001_managers/001_blog.py' "
        "'0100_models/001_managers/01101_blog.py';\n"
        "git mv '0100_models/001_managers/002_article.py' "
        "'0100_models/001_managers/01102_article.py';\n"
        "git mv '010_base/030_cool.bak.py' '010_base/02002_cool.bak.py';\n"
        "git mv '010_base/010_ok.txt' '010_base/02001_ok.txt';\n"
        "git mv '0100_models/0101_blog.py' '0100_models/01001_blog.py';\n"
        "git mv '0100_models/010_base.py' '0100_models/01004_base.py';\n"
        "git mv '0100_models/0103_category.py' '0100_models/01003_category.py';\n"
        "git mv '0100_models/0102_article.py' '0100_models/01002_article.py';\n"
        "git mv '0500_forms/502_article.py' '0500_forms/04001_article.py';\n"
        "git mv '020_foo.py' '00001_foo.py';\n"
        "git mv '1020_bar.py' '00002_bar.py';\n"
        "git mv '0100_models/002_lookups' '0100_models/01200_lookups';\n"
        "git mv '0100_models/001_managers' '0100_models/01100_managers';\n"
        "git mv '1000_views' '05000_views';\n"
        "git mv '010_base' '02000_base';\n"
        "git mv '0200_empty' '03000_empty';\n"
        "git mv '0100_models' '01000_models';\n"
        "git mv '0500_forms' '04000_forms';\n"
        "echo \"Finished all tasks!\";\n"
    ).format(structure)
