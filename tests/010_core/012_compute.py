"""
(step=10, maxdeep=1) = 3
(step=10, maxdeep=2) = 4
(step=10, maxdeep=3) = 5
(step=100, maxdeep=1) = 4
(step=100, maxdeep=2) = 5
(step=100, maxdeep=3) = 6
(step=1000, maxdeep=1) = 5


    step=10 / maxdeep=1 / digit=000 (3)
        010 managers/
            011 blog.py
            ...
            019 article.py
        090 lookups/
        001 blog.py
        ...
        009 article.py

    step=100 / maxdeep=1 / digit=0000 (4)
        0100 managers/
            0101 blog.py
            ...
            0199 article.py
        0900 lookups/
        0001 blog.py
        ...
        0099 article.py

    step=10 / maxdeep=2 / digit=0000 (4)
        0100 models/
            0110 managers/
                0111 blog.py
                ...
                0119 article.py
            0190 lookups/
            0101 blog.py
            ...
            0109 article.py
        0900 forms/
        ...
        0009 leap.py

    step=100 / maxdeep=2 / digit=00000 (5)
        01000 models/
            01100 managers/
                01101 blog.py
                ...
                01199 article.py
            01900 lookups/
            01001 blog.py
            ...
            01099 article.py
        09000 forms/
        ...
        00099 leap.py

    step=10 / maxdeep=3 / digit=00000 (5)
        01000 app_1/
            01100 models/
                01110 managers/
                    01111 blog.py
                    ...
                    01119 article.py
                01190 lookups/
                01101 blog.py
                ...
                01109 article.py
            01900 forms/
            ...
            01009 leap.py

    step=100 / maxdeep=3 / digit=000000 (6)
        010000 app_1/
            011000 models/
                011100 managers/
                    011101 blog.py
                    ...
                    011199 article.py
                011900 lookups/
                011001 blog.py
                ...
                011099 article.py
            019000 forms/
        090000 app_9/
        ...
        000099 leap.py

    step=1000 / maxdeep=1 / digit=00000(5)
        01000 managers/
            01001 blog.py
            ...
            01999 article.py
        09000 lookups/
        00001 blog.py
        ...
        00009 article.py
"""
import pytest

from miss_lemon.walker import DirWalker


def display_resource(resource, maxdeep=0, position=0, output=None):
    """
    Function helper to build a flat list of resources with indent.

    Returns:
        list: List of string, each item is a resource showing the resource prefix
        joined to its name, the resource level and some leading indent base on level.
    """
    output = [] if output is None else output

    # We only append non root element
    if not resource.is_root():
        level = resource.get_level()
        output.append("{indent}{prefix}_{name} [{level}]".format(**{
            "indent": "  " * level,
            "level": level,
            "prefix": resource.prefix,
            "name": resource.name,
        }))

    # Follow resource children
    for i, item in enumerate(resource.ordered_children(), start=1):
        display_resource(item, maxdeep=maxdeep, position=1, output=output)

    return output


@pytest.mark.parametrize("step, maxdeep, expected", [
    (10, 1, [10]),
    (10, 2, [100, 10]),
    (10, 3, [1000, 100, 10]),
    (100, 1, [100]),
    (100, 2, [1000, 100]),
    (100, 3, [10000, 1000, 100]),
    (1000, 1, [1000]),
])
def test_get_increments(settings, step, maxdeep, expected):
    """
    Method should return a list of increment base on step and maxdeep.
    """
    walker = DirWalker(settings.datas_path / "minimal_structure")
    result = walker.get_increments(step, maxdeep)

    assert result == expected


@pytest.mark.parametrize("step, maxdeep, matrix, digits", [
    (10, 1, 3, "000"),
    (10, 2, 4, "0000"),
    (10, 3, 5, "00000"),
    (100, 1, 4, "0000"),
    (100, 2, 5, "00000"),
    (100, 3, 6, "000000"),
    (1000, 1, 5, "00000"),
])
def test_get_prefix_matrix(settings, step, maxdeep, matrix, digits):
    """
    The prefix matrix length should always fit the maximum prefix value.
    """
    walker = DirWalker(settings.datas_path / "minimal_structure")
    result = walker.get_prefix_matrix(step, maxdeep)

    assert result == matrix
    assert digits == "0".zfill(matrix)


def test_compute_minimal(caplog, settings):
    """
    Computation of resource prefixes from minimal structure.
    """
    structure = settings.datas_path / "minimal_structure"
    walker = DirWalker(structure)

    root = walker.compute()

    output = display_resource(root, maxdeep=root.get_deep())
    assert output == [
        "  01000_models [1]",
        "    01100_managers [2]",
        "      01101_blog.py [3]",
        "    01200_lookups [2]",
        "    01001_category.py [2]",
        "  02000_views [1]",
        "  00001_foo.py [1]",
    ]


def test_compute_basic(caplog, settings):
    """
    Computation of resource prefixes from basic structure.
    """
    structure = settings.datas_path / "basic_structure"
    walker = DirWalker(structure)

    root = walker.compute()

    output = display_resource(root, maxdeep=root.get_deep())
    assert output == [
        "  01000_models [1]",
        "    01100_managers [2]",
        "      01101_blog.py [3]",
        "      01102_article.py [3]",
        "    01200_lookups [2]",
        "    01001_blog.py [2]",
        "    01002_article.py [2]",
        "    01003_category.py [2]",
        "    01004_base.py [2]",
        "  02000_base [1]",
        "    02001_ok.txt [2]",
        "    02002_cool.bak.py [2]",
        "  03000_empty [1]",
        "  04000_forms [1]",
        "    04001_article.py [2]",
        "  05000_views [1]",
        "  00001_foo.py [1]",
        "  00002_bar.py [1]",
    ]
