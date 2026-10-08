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
            Path("0100_models/0101_blog.py"), Path("0100_models/01001_blog.py"),
        ),
        (
            Path("0100_models/0102_article.py"), Path("0100_models/01002_article.py"),
        ),
        (
            Path("0100_models/0103_category.py"), Path("0100_models/01003_category.py"),
        ),
        (
            Path("0100_models/010_base.py"), Path("0100_models/01004_base.py"),
        ),
        (
            Path("010_base/010_ok.txt"), Path("010_base/02001_ok.txt"),
        ),
        (
            Path("010_base/030_cool.bak.py"), Path("010_base/02002_cool.bak.py"),
        ),
        (
            Path("0500_forms/502_article.py"), Path("0500_forms/04001_article.py"),
        ),
        (
            Path("020_foo.py"), Path("00001_foo.py"),
        ),
        (
            Path("1020_bar.py"), Path("00002_bar.py"),
        ),
    ]

    assert dirs == [
        (
            Path("0100_models/001_managers"), Path("0100_models/01100_managers"),
        ),
        (
            Path("0100_models/002_lookups"), Path("0100_models/01200_lookups"),
        ),
        (
            Path("0100_models"), Path("01000_models"),
        ),
        (
            Path("010_base"), Path("02000_base"),
        ),
        (
            Path("0200_empty"), Path("03000_empty"),
        ),
        (
            Path("0500_forms"), Path("04000_forms"),
        ),
        (
            Path("1000_views"), Path("05000_views"),
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

    assert output == "\n".join([
        "# This shell script will 'cd' into the source directory then apply renaming "
        "of resources.",
        "cd '{}';".format(structure),
        (
            "mv '0100_models/001_managers/001_blog.py' "
            "'0100_models/001_managers/01101_blog.py';"
        ),
        (
            "mv '0100_models/001_managers/002_article.py' "
            "'0100_models/001_managers/01102_article.py';"
        ),
        "mv '0100_models/0101_blog.py' '0100_models/01001_blog.py';",
        "mv '0100_models/0102_article.py' '0100_models/01002_article.py';",
        "mv '0100_models/0103_category.py' '0100_models/01003_category.py';",
        "mv '0100_models/010_base.py' '0100_models/01004_base.py';",
        "mv '010_base/010_ok.txt' '010_base/02001_ok.txt';",
        "mv '010_base/030_cool.bak.py' '010_base/02002_cool.bak.py';",
        "mv '0500_forms/502_article.py' '0500_forms/04001_article.py';",
        "mv '020_foo.py' '00001_foo.py';",
        "mv '1020_bar.py' '00002_bar.py';",
        "mv '0100_models/001_managers' '0100_models/01100_managers';",
        "mv '0100_models/002_lookups' '0100_models/01200_lookups';",
        "mv '0100_models' '01000_models';",
        "mv '010_base' '02000_base';",
        "mv '0200_empty' '03000_empty';",
        "mv '0500_forms' '04000_forms';",
        "mv '1000_views' '05000_views';",
        "echo \"Finished all tasks!\";",
        "",
    ])


def test_with_shell_gitmv(caplog, settings):
    """
    Method should output all command lines to rename resources using command 'git mv'.
    """
    structure = settings.datas_path / "basic_structure"
    walker = DirWalker(structure)

    root = walker.compute()

    renamer = Renamer(root)
    output = renamer.with_shell_gitmv()

    assert output == "\n".join([
        "# This shell script will 'cd' into the source directory then apply renaming "
        "of resources.",
        "cd '{}';".format(structure),
        (
            "git mv '0100_models/001_managers/001_blog.py' "
            "'0100_models/001_managers/01101_blog.py';"
        ),
        (
            "git mv '0100_models/001_managers/002_article.py' "
            "'0100_models/001_managers/01102_article.py';"
        ),
        "git mv '0100_models/0101_blog.py' '0100_models/01001_blog.py';",
        "git mv '0100_models/0102_article.py' '0100_models/01002_article.py';",
        "git mv '0100_models/0103_category.py' '0100_models/01003_category.py';",
        "git mv '0100_models/010_base.py' '0100_models/01004_base.py';",
        "git mv '010_base/010_ok.txt' '010_base/02001_ok.txt';",
        "git mv '010_base/030_cool.bak.py' '010_base/02002_cool.bak.py';",
        "git mv '0500_forms/502_article.py' '0500_forms/04001_article.py';",
        "git mv '020_foo.py' '00001_foo.py';",
        "git mv '1020_bar.py' '00002_bar.py';",
        "git mv '0100_models/001_managers' '0100_models/01100_managers';",
        "git mv '0100_models/002_lookups' '0100_models/01200_lookups';",
        "git mv '0100_models' '01000_models';",
        "git mv '010_base' '02000_base';",
        "git mv '0200_empty' '03000_empty';",
        "git mv '0500_forms' '04000_forms';",
        "git mv '1000_views' '05000_views';",
        "echo \"Finished all tasks!\";",
        "",
    ])
