import json
import logging

from miss_lemon import __pkgname__
from miss_lemon.walker import DirWalker
from miss_lemon.models.resource import ResourceModel


def test_collect_basic(caplog, settings):
    """
    The full basic structure should be returned only with valid resources.
    """
    caplog.set_level(logging.DEBUG)

    structure = settings.datas_path / "minimal_structure"
    walker = DirWalker(structure)

    root = walker.collect()

    assert isinstance(root, ResourceModel)

    assert json.loads(root.as_json()) == {
        "path": "{}".format(structure),
        "number": 0,
        "prefix": "",
        "original_prefix": "",
        "name": "minimal_structure",
        "children": [
            {
                "path": "{}/0100_models".format(structure),
                "number": 0,
                "prefix": "",
                "original_prefix": "0100",
                "name": "models",
                "children": [
                    {
                        "path": "{}/0100_models/001_managers".format(structure),
                        "number": 0,
                        "prefix": "",
                        "original_prefix": "001",
                        "name": "managers",
                        "children": [
                            {
                                "path": (
                                    "{}/0100_models/001_managers/001_blog.py".format(
                                        structure
                                    )
                                ),
                                "number": 0,
                                "prefix": "",
                                "original_prefix": "001",
                                "name": "blog.py",
                                "children": [],
                                "built_name": "blog.py"
                            }
                        ],
                        "built_name": "managers"
                    },
                    {
                        "path": "{}/0100_models/002_lookups".format(structure),
                        "number": 0,
                        "prefix": "",
                        "original_prefix": "002",
                        "name": "lookups",
                        "children": [],
                        "built_name": "lookups"
                    },
                    {
                        "path": "{}/0100_models/0103_category.py".format(structure),
                        "number": 0,
                        "prefix": "",
                        "original_prefix": "0103",
                        "name": "category.py",
                        "children": [],
                        "built_name": "category.py"
                    }
                ],
                "built_name": "models"
            },
            {
                "path": "{}/1000_views".format(structure),
                "number": 0,
                "prefix": "",
                "original_prefix": "1000",
                "name": "views",
                "children": [],
                "built_name": "views"
            },
            {
                "path": "{}/020_foo.py".format(structure),
                "number": 0,
                "prefix": "",
                "original_prefix": "020",
                "name": "foo.py",
                "children": [],
                "built_name": "foo.py"
            }
        ],
        "built_name": "minimal_structure"
    }

    assert caplog.record_tuples == [
        (__pkgname__, logging.DEBUG, "Ignored resource (from pattern): nada.py"),
        (__pkgname__, logging.DEBUG, "Ignored resource (from pattern): nib.py"),
        (__pkgname__, logging.DEBUG, "Ignored resource (from pattern): nope"),
        (__pkgname__, logging.DEBUG, "Ignored resource (from pattern): niet.py"),
    ]


def test_collect_all(caplog, settings):
    """
    Option 'allow_unprefixed' allows to collect all resources, even if they not match
    the regex pattern with prefix.
    """
    caplog.set_level(logging.DEBUG)

    structure = settings.datas_path / "minimal_structure"
    walker = DirWalker(structure, allow_unprefixed=True)

    root = walker.collect()

    assert json.loads(root.as_json(allows_only=("path", "children"))) == {
        "path": "{}".format(structure),
        "children": [
            {
                "path": "{}/0100_models".format(structure),
                "children": [
                    {
                        "path": "{}/0100_models/001_managers".format(structure),
                        "children": [
                            {
                                "path": (
                                    "{}/0100_models/001_managers/001_blog.py".format(
                                        structure
                                    )
                                ),
                                "children": []
                            }
                        ]
                    },
                    {
                        "path": "{}/0100_models/002_lookups".format(structure),
                        "children": []
                    },
                    {
                        "path": "{}/0100_models/0103_category.py".format(structure),
                        "children": []
                    },
                    {
                        "path": "{}/0100_models/nada.py".format(structure),
                        "children": []
                    }
                ]
            },
            {
                "path": "{}/1000_views".format(structure),
                "children": [
                    {
                        "path": "{}/1000_views/nib.py".format(structure), "children": []
                    }
                ]
            },
            {"path": "{}/nope".format(structure), "children": []},
            {"path": "{}/020_foo.py".format(structure), "children": []},
            {"path": "{}/niet.py".format(structure), "children": []}
        ]
    }

    assert caplog.record_tuples == []


def test_collect_exclude(caplog, settings):
    """
    Option 'excludes' allows to exclude resource with "Unix filename pattern" (fnmatch).
    """
    caplog.set_level(logging.DEBUG)

    structure = settings.datas_path / "minimal_structure"
    walker = DirWalker(
        structure,
        allow_unprefixed=True,
        excludes=["niet.py", "**/nib.py", "0100_models"],
    )

    root = walker.collect()

    assert json.loads(root.as_json(allows_only=("path", "children"))) == {
        "path": "{}".format(structure),
        "children": [
            {
                "path": "{}/1000_views".format(structure),
                "children": []
            },
            {"path": "{}/nope".format(structure), "children": []},
            {"path": "{}/020_foo.py".format(structure), "children": []},
        ]
    }
