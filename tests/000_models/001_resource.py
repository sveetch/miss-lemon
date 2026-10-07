import json
from pathlib import Path

from miss_lemon.models.lists import SerializableList
from miss_lemon.models.resource import ResourceModel


def test_creation(settings):
    """
    Model should create a new object and parent/children should be correctly set.
    """
    middle = ResourceModel(path=Path("root/middle"))

    root = ResourceModel(
        path=Path("root"),
        children=[middle],
    )

    leaf = ResourceModel(path=Path("root/middle/leaf"))

    middle.set_children(leaf)

    assert root.parent is None
    assert root.children == [middle]
    assert isinstance(root.children, SerializableList) is True
    assert middle.parent == root
    assert middle.children == [leaf]
    assert isinstance(middle.children, SerializableList) is True
    assert leaf.parent == middle
    assert leaf.children == []
    assert isinstance(leaf.children, SerializableList) is True


def test_one_level(settings, tmp_path):
    """
    Deep and level on one dir level should be correct.
    """
    # Add ping branch
    ping = ResourceModel(path=tmp_path / "ping")
    ping.path.mkdir()
    assert ping.get_deep() == 0
    assert ping.get_level() == 0

    # Add file to 'ping'
    pew = ResourceModel(path=ping.path / "pew.txt")
    pew.path.write_text("pew pew")
    ping.set_children(pew)
    assert ping.get_deep() == 0
    assert pew.get_level() == 1


def test_two_levels(settings, tmp_path):
    """
    Deep and level on two dir level should be correct.
    """
    # Add ping branch
    ping = ResourceModel(path=tmp_path / "ping")
    ping.path.mkdir()
    pong = ResourceModel(path=ping.path / "pong")
    pong.path.mkdir()
    ping.set_children(pong)
    assert ping.get_deep() == 1
    assert ping.get_level() == 0
    assert pong.get_level() == 1

    # Add file to 'pong'
    pew = ResourceModel(path=pong.path / "pew.txt")
    pew.path.write_text("pew pew")
    pong.set_children(pew)
    assert ping.get_deep() == 1
    assert ping.get_level() == 0
    assert pong.get_level() == 1
    assert pew.get_level() == 2


def test_two_branches(settings, tmp_path):
    """
    With two branches under a root resource.
    """
    # Add 'root' branch
    root = ResourceModel(path=tmp_path / "root")
    root.path.mkdir()
    assert root.get_level() == 0

    # Add 'foo' branch
    foo = ResourceModel(path=root.path / "foo")
    foo.path.mkdir()
    bar = ResourceModel(path=foo.path / "bar")
    bar.path.mkdir()
    foo.set_children(bar)
    hello = ResourceModel(path=bar.path / "hello.txt")
    hello.path.write_text("hello world")
    bar.set_children(hello)
    assert foo.get_deep() == 1
    assert foo.get_level() == 0
    assert bar.get_level() == 1

    # Add 'ping' branch
    ping = ResourceModel(path=root.path / "ping")
    ping.path.mkdir()
    pong = ResourceModel(path=ping.path / "pong")
    pong.path.mkdir()
    pang = ResourceModel(path=pong.path / "pang")
    pang.path.mkdir()
    ping.set_children(pong)
    pong.set_children(pang)
    assert ping.get_deep() == 2
    assert ping.get_level() == 0
    assert pong.get_level() == 1
    assert pang.get_level() == 2

    # Add file to 'pang'
    pew = ResourceModel(path=pang.path / "pew.txt")
    pew.path.write_text("pew pew")
    pang.set_children(pew)
    assert ping.get_deep() == 2
    assert ping.get_level() == 0
    assert pong.get_level() == 1
    assert pang.get_level() == 2
    assert pew.get_level() == 3

    # Push 'foo' and 'ping' branches into 'root'
    root.set_children(foo, ping)
    assert root.get_deep() == 3
    assert ping.get_level() == 1
    assert pong.get_level() == 2
    assert pang.get_level() == 3
    assert pew.get_level() == 4

    # import subprocess
    # tree = subprocess.check_output(["tree", tmp_path], stderr=subprocess.STDOUT)
    # print()
    # print(tree.decode("utf-8"))

    assert [v.path.name for v in root.children] == ["foo", "ping"]
    assert [v.path.name for v in root.children_directories()] == ["foo", "ping"]
    assert [v.path.name for v in root.children_files()] == []
    assert [v.path.name for v in pang.children_files()] == ["pew.txt"]


def test_ordered_children(tmp_path):
    """
    Method should correctly distincts directories and files, and their order should be
    correct ascending order.
    """
    # Add 'root' branch
    root = ResourceModel(path=tmp_path / "root")
    root.path.mkdir()
    assert root.get_level() == 0

    # Add 'foo' branch
    foo = ResourceModel(path=root.path / "foo")
    foo.path.mkdir()

    beer = ResourceModel(path=root.path / "beer")
    beer.path.mkdir()

    bar = ResourceModel(path=root.path / "001_bar")
    bar.path.mkdir()

    hello = ResourceModel(path=root.path / "hello.txt")
    hello.path.write_text("hello world")
    root.set_children(hello)

    bye = ResourceModel(path=root.path / "bye.txt")
    bye.path.write_text("bye bye")
    root.set_children(bye)

    root.set_children(foo, bar, beer)

    assert [child.path.name for child in root.ordered_children()] == [
        "001_bar",
        "beer",
        "foo",
        "bye.txt",
        "hello.txt",
    ]


def test_serialize(settings):
    """
    Method should correctly serialize object and respect options.
    """
    middle = ResourceModel(path=Path("root/middle"))
    root = ResourceModel(
        path=Path("root"),
        children=[middle],
    )
    leaf = ResourceModel(path=Path("root/middle/leaf"))
    middle.set_children(leaf)

    assert json.loads(root.as_json()) == {
        "path": "root",
        "number": 0,
        "prefix": "",
        "original_prefix": "",
        "name": "",
        "children": [
            {
                "path": "root/middle",
                "number": 0,
                "prefix": "",
                "original_prefix": "",
                "name": "",
                "children": [
                    {
                        "path": "root/middle/leaf",
                        "number": 0,
                        "prefix": "",
                        "original_prefix": "",
                        "name": "",
                        "children": [],
                        "built_name": "leaf"
                    }
                ],
                "built_name": "middle"
            }
        ],
        "built_name": "root"
    }

    assert json.loads(root.as_json(allows_only=("built_name", "children"))) == {
        "children": [
            {
                "children": [
                    {
                        "children": [],
                        "built_name": "leaf"
                    }
                ],
                "built_name": "middle"
            }
        ],
        "built_name": "root"
    }


def test_recursive_children_resources(settings, tmp_path):
    """
    Resource has methods to get a distinct flat list of recursive children either for
    directories or files. Resources are ordered from their relative path from leaft to
    top.
    """
    # Add 'root' branch
    root = ResourceModel(path=tmp_path / "root")
    root.path.mkdir()

    # Add 'foo' branch
    foo = ResourceModel(path=root.path / "foo")
    foo.path.mkdir()
    bar = ResourceModel(path=foo.path / "bar")
    bar.path.mkdir()
    foo.set_children(bar)
    hello = ResourceModel(path=bar.path / "hello.txt")
    hello.path.write_text("hello world")
    bar.set_children(hello)

    # Add 'ping' branch
    ping = ResourceModel(path=root.path / "ping")
    ping.path.mkdir()
    pong = ResourceModel(path=ping.path / "pong")
    pong.path.mkdir()
    pang = ResourceModel(path=pong.path / "pang")
    pang.path.mkdir()
    ping.set_children(pong)
    pong.set_children(pang)

    # Add file to 'pang'
    pew = ResourceModel(path=pang.path / "pew.txt")
    pew.path.write_text("pew pew")
    pang.set_children(pew)

    # Push 'foo' and 'ping' branches into 'root'
    root.set_children(foo, ping)

    # import subprocess
    # tree = subprocess.check_output(["tree", tmp_path], stderr=subprocess.STDOUT)
    # print()
    # print(tree.decode("utf-8"))
    # print()

    dirs = root.recursive_children_directories()
    assert [str(v.path.relative_to(root.path)) for v in dirs] == [
        "ping/pong/pang",
        "foo/bar",
        "ping/pong",
        "foo",
        "ping",
    ]

    files = root.recursive_children_files()
    assert [str(v.path.relative_to(root.path)) for v in files] == [
        "ping/pong/pang/pew.txt",
        "foo/bar/hello.txt",
    ]
