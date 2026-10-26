.. _overview_intro:

========
Overview
========

Miss lemon provides a commandline to preview a path for possible resource renaming and
another one to build a renaming strategy to apply.

The renaming operation is only to add a numeric prefix to the resource name such like
resource ``hello`` would become ``001_hello``.

.. _usage_overview_prefix:

Prefix
******

The prefix is computed automatically so it is incremented in order of the resource list
order, no duplicate prefix is possible.

When discovered, a resource is parsed to find a possible existing prefix using the
**prefix pattern**, to resume:

* The resource ``001_hello`` is found to have the prefix ``001``;
* The resource ``hello`` is found to not have any prefix;
* The resource ``0bip_hello`` is found to not have any prefix because its prefix is
  not numeric;

Existing prefix is not used when the new resource name is computed.

.. _usage_overview_status:

Status
******

Miss lemon rename all resources (files and directories) from a path that are eligibles
for renaming. When processing resources it will compute their status:

ignored
    When the resource name is either a protected resource (name starting with
    character ``.`` or ``_``) or excluded from **prefix pattern** (this can be
    disabled from options).
identical
    When the resource renaming will lead to the same filename, commonly if the resource
    name was already prefixed correctly.
changed
    When the resource is eligible and computed new name lead to a different filename.


.. _usage_overview_sample:

Sample structure
****************

The usage documentation will use this sample structure for all command examples: ::

    sample_structure/
    ├── 0100_models
    │   ├── 001_managers
    │   │   └── 001_blog.py
    │   ├── 002_lookups
    │   ├── 0103_category.py
    │   └── nada.py
    ├── 020_foo.py
    ├── 1000_views
    │   └── no.py
    ├── nein.py
    ├── non
    │   └── 0300_bar.py
    └── nope

This structure contains various resources with or without a prefix.
