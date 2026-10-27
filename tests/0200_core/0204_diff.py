from pathlib import Path

from miss_lemon.walker import DirWalker
from miss_lemon.diff import DiffTree
from miss_lemon.models.resource import ResourceModel


def test_build_flat_tree(settings):
    """
    Method should return a flat tree (in a dict) of all resources from given parent
    resource.
    """
    structure = settings.datas_path / "basic_structure"
    walker = DirWalker(structure)
    root = walker.compute()

    differ = DiffTree()
    result = differ.build_flat_tree(root)

    expected = [
        "{}/0100_models/001_managers",
        "{}/0100_models/002_lookups",
        "{}/0100_models",
        "{}/010_base",
        "{}/0200_empty",
        "{}/0500_forms",
        "{}/1000_views",
        "{}/0100_models/001_managers/001_blog.py",
        "{}/0100_models/001_managers/002_article.py",
        "{}/0100_models/0101_blog.py",
        "{}/0100_models/0102_article.py",
        "{}/0100_models/0103_category.py",
        "{}/0100_models/010_base.py",
        "{}/010_base/010_ok.txt",
        "{}/010_base/030_cool.bak.py",
        "{}/0500_forms/502_article.py",
        "{}/020_foo.py",
        "{}/1020_bar.py",
    ]

    assert [k for k, v in result.items()] == [v.format(structure) for v in expected]
    assert isinstance(
        result["{}/0100_models".format(structure)]["resource"],
        ResourceModel
    ) is True


def test_diff_resource():
    """
    Method should correctly compute the resource status with original and possible
    changes.
    """
    differ = DiffTree()

    leaf = Path("root/middle/leaf")
    original = ResourceModel(path=leaf)
    different = ResourceModel(path=Path("root/middle/new_leaf"))

    # No changes given, assume this is a resource to ignore
    result = differ.diff_resource(original, changes=None)
    assert result == {"status": "ignored", "from": leaf, "to": None}

    # Changes lead to the same name, state it as "identical"
    result = differ.diff_resource(original, changes={"resource": original})
    assert result == {"status": "identical", "from": leaf, "to": "leaf"}

    # Changes lead to the same name, state it as "identical"
    result = differ.diff_resource(original, changes={"resource": different})
    assert result == {"status": "changed", "from": leaf, "to": "new_leaf"}


def test_get_ascii_label(settings):
    """
    Label should be correct proper ascii with ending slash for directory
    """
    structure = settings.datas_path / "basic_structure"

    differ = DiffTree()

    original = ResourceModel(path=(structure / "0100_models/001_managers"))
    different = ResourceModel(path=(structure / "0100_models/010_managers"))

    # No changes given, assume this is a resource to ignore
    result = differ.diff_resource(original, changes=None)
    assert differ.get_ascii_label(result) == "001_managers/ (IGNORED)"

    # Changes lead to the same name, state it as "identical"
    result = differ.diff_resource(original, changes={"resource": original})
    assert differ.get_ascii_label(result) == "001_managers/ (SAME)"

    # Changes lead to the same name, state it as "identical"
    result = differ.diff_resource(original, changes={"resource": different})
    assert differ.get_ascii_label(result) == "010_managers/ <- 001_managers/"


def test_get_rich_label(settings):
    """
    Label should be correct Rich syntax with ending slash for directory
    """
    structure = settings.datas_path / "basic_structure"

    differ = DiffTree()

    original = ResourceModel(path=(structure / "0100_models/001_managers"))
    different = ResourceModel(path=(structure / "0100_models/010_managers"))

    # No changes given, assume this is a resource to ignore
    result = differ.diff_resource(original, changes=None)
    assert differ.get_rich_label(result) == "[yellow]001_managers/ (IGNORED)"

    # Changes lead to the same name, state it as "identical"
    result = differ.diff_resource(original, changes={"resource": original})
    assert differ.get_rich_label(result) == "001_managers/ (SAME)"

    # Changes lead to the same name, state it as "identical"
    result = differ.diff_resource(original, changes={"resource": different})
    assert differ.get_rich_label(result) == (
        "[green]010_managers/[/green] <- 001_managers/"
    )
