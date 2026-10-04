import json
import logging

from miss_lemon import __pkgname__
from miss_lemon.walker import DirWalker
from miss_lemon.models.resource import ResourceModel


def test_structure(caplog, settings):
    """
    The full structure should be returned only with valid resources.
    """
    structure = settings.datas_path / "basic_structure"
    walker = DirWalker(structure)

    root = walker.collect()

    assert isinstance(root, ResourceModel)
    assert json.loads(root.as_json()) == {
        "path": "{}".format(structure),
        "number": 0,
        "prefix": "",
        "original_prefix": "",
        "name": "",
        "children": [
            {
                "path": "{}/1000_views".format(structure),
                "number": 0,
                "prefix": "",
                "original_prefix": "1000",
                "name": "views",
                "children": []
            },
            {
                "path": "{}/010_base".format(structure),
                "number": 0,
                "prefix": "",
                "original_prefix": "010",
                "name": "base",
                "children": [
                    {
                        "path": "{}/010_base/030_cool.bak.py".format(structure),
                        "number": 0,
                        "prefix": "",
                        "original_prefix": "030",
                        "name": "cool.bak.py",
                        "children": []
                    },
                    {
                        "path": "{}/010_base/010_ok.txt".format(structure),
                        "number": 0,
                        "prefix": "",
                        "original_prefix": "010",
                        "name": "ok.txt",
                        "children": []
                    }
                ]
            },
            {
                "path": "{}/0200_empty".format(structure),
                "number": 0,
                "prefix": "",
                "original_prefix": "0200",
                "name": "empty",
                "children": []
            },
            {
                "path": "{}/020_foo.py".format(structure),
                "number": 0,
                "prefix": "",
                "original_prefix": "020",
                "name": "foo.py",
                "children": []
            },
            {
                "path": "{}/0100_models".format(structure),
                "number": 0,
                "prefix": "",
                "original_prefix": "0100",
                "name": "models",
                "children": [
                    {
                        "path": "{}/0100_models/0101_blog.py".format(structure),
                        "number": 0,
                        "prefix": "",
                        "original_prefix": "0101",
                        "name": "blog.py",
                        "children": []
                    },
                    {
                        "path": "{}/0100_models/010_base.py".format(structure),
                        "number": 0,
                        "prefix": "",
                        "original_prefix": "010",
                        "name": "base.py",
                        "children": []
                    },
                    {
                        "path": "{}/0100_models/002_lookups".format(structure),
                        "number": 0,
                        "prefix": "",
                        "original_prefix": "002",
                        "name": "lookups",
                        "children": []
                    },
                    {
                        "path": "{}/0100_models/0103_category.py".format(structure),
                        "number": 0,
                        "prefix": "",
                        "original_prefix": "0103",
                        "name": "category.py",
                        "children": []
                    },
                    {
                        "path": "{}/0100_models/0102_article.py".format(structure),
                        "number": 0,
                        "prefix": "",
                        "original_prefix": "0102",
                        "name": "article.py",
                        "children": []
                    },
                    {
                        "path": "{}/0100_models/001_managers".format(structure),
                        "number": 0,
                        "prefix": "",
                        "original_prefix": "001",
                        "name": "managers",
                        "children": [
                            {
                                "path": (
                                    "{}/0100_models/001_managers/001_blog.py"
                                ).format(
                                    structure
                                ),
                                "number": 0,
                                "prefix": "",
                                "original_prefix": "001",
                                "name": "blog.py",
                                "children": []
                            },
                            {
                                "path": (
                                    "{}/0100_models/001_managers/002_article.py"
                                ).format(
                                    structure
                                ),
                                "number": 0,
                                "prefix": "",
                                "original_prefix": "002",
                                "name": "article.py",
                                "children": []
                            }
                        ]
                    }
                ]
            },
            {
                "path": "{}/1020_bar.py".format(structure),
                "number": 0,
                "prefix": "",
                "original_prefix": "1020",
                "name": "bar.py",
                "children": []
            },
            {
                "path": "{}/0500_forms".format(structure),
                "number": 0,
                "prefix": "",
                "original_prefix": "0500",
                "name": "forms",
                "children": [
                    {
                        "path": "{}/0500_forms/502_article.py".format(structure),
                        "number": 0,
                        "prefix": "",
                        "original_prefix": "502",
                        "name": "article.py",
                        "children": []
                    }
                ]
            },
        ]
    }

    assert caplog.record_tuples == [
        (__pkgname__, logging.WARNING, "Invalid pattern for: nib.py"),
        (__pkgname__, logging.WARNING, "Invalid pattern for: nope"),
        (__pkgname__, logging.WARNING, "Invalid pattern for: niet.py"),
        (__pkgname__, logging.WARNING, "Invalid pattern for: niet.txt"),
        (__pkgname__, logging.WARNING, "Invalid pattern for: no"),
        (__pkgname__, logging.WARNING, "Invalid pattern for: nada.py"),
    ]
