.. _usage_intro:

=====
Usage
=====

Miss lemon provides a commandline to preview a path for possible resource renaming and
another one to build a renaming strategy to apply.

The renaming operation is only to add a numeric prefix to the resource name such like
resource ``hello`` would become ``001_hello``.

.. _usage_overview:

Overview
********

.. _usage_overview_prefix:

Prefix
------

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
------

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

This document will use a sample structure for all command examples: ::

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

.. _usage_check:

'check' command
***************

This command will display a preview of possible renaming. Its usage is: ::

    miss_lemon check [OPTIONS] SOURCE

Where ``SOURCE`` is the required path to scan.

The command will output a preview tree for given path with all resources eligibles to
renaming: ::

    sample_structure
    ├── 01000_models (SAME)
    │   ├── 01100_managers <- 001_managers
    │   │   └── 01101_blog.py <- 001_blog.py
    │   ├── 01200_lookups <- 002_lookups
    │   └── 01001_category.py <- 0103_category.py
    ├── 02000_views <- 1000_views
    └── 00001_foo.py <- 020_foo.py

* The first part of each line is the destination preview of a resource;
* If the second part contains ``<-`` then the following part is the original resource
  name;
* Without ``<-``, the second part is the resource status that can be:

  * ``SAME`` when the destination leads to the same filename with original path;
  * ``IGNORED`` when the resource has been ignored from **prefix pattern** (on default
    they won't be displayed, see option ``--display-ignored``);

.. _usage_check_prefix:

Prefix step
-----------

On default, the prefix is computed with a step of ``100``.

.. Note::
    Concretely the **step** is the lowest prefix number for a leaf resource, each parent
    level resources will increment it with a decimal number such as 10, 100, 1000, etc..

    Computation of prefix is done so you can have ten directories and a hundred of files
    in a directory, guarented to be unique.

Here is an example with the step value ``10``: ::

    sample_structure
    ├── 0100_models <- 01000_models
    │   ├── 0110_managers <- 001_managers
    │   │   └── 0111_blog.py <- 001_blog.py
    │   ├── 0120_lookups <- 002_lookups
    │   └── 0101_category.py <- 0103_category.py
    ├── 0200_views <- 1000_views
    └── 0001_foo.py <- 020_foo.py

Or with step 10 and a structure with less levels: ::

    sample_structure/01000_models
    ├── 010_managers <- 001_managers
    │   └── 011_blog.py <- 001_blog.py
    ├── 020_lookups <- 002_lookups
    └── 001_category.py <- 0103_category.py

.. _usage_check_output:

Output
------

The output is a tree, either as plain text or as JSON, the latter includes more
information but is is less readable, commonly you will prefer the plain text tree which
is the default output.

On default the option ``--output`` allows for value ``json`` and ``tree``. With the
extra requirements ``rich`` installed, another value ``rich`` will be available.


.. _usage_check_without_prefix:

Process resources without prefix
--------------------------------

On default, Miss lemon don't process resources that don't have a valid numeric prefix.
It is because the main purpose is to maintain an existing prefix structure.

However you are able to also process resource without prefix using option
``--unprefixed``: ::

    sample_structure
    ├── 01000_models (SAME)
    │   ├── 01100_managers <- 001_managers
    │   │   └── 01101_blog.py <- 001_blog.py
    │   ├── 01200_lookups <- 002_lookups
    │   ├── 01001_category.py <- 0103_category.py
    │   └── 01002_nada.py <- nada.py
    ├── 02000_views <- 1000_views
    │   └── 02001_no.py <- no.py
    ├── 03000_non <- non
    │   └── 03001_bar.py <- 0300_bar.py
    ├── 04000_nope <- nope
    ├── 00001_foo.py <- 020_foo.py
    └── 00002_nein.py <- nein.py

.. _usage_check_excludes:

Excluding
---------

You may need also to exclude resources that you explicitely don't want to be processed
for renaming, it is especially common when processing resource without prefix.

The option ``--excludes PATTERN`` allows to exclude resources that match a pattern. It
can be defined multiple times to define many patterns to assert. The pattern is to be
defined as a "Unix filename patterns" (as supported from Python module ``fnmatch``).

With the following options
``--excludes "nein.py" --excludes "**/no.py" --excludes "01000_models"`` you will have
many resource excluded: ::

    sample_structure
    ├── 0100_views <- 1000_views
    ├── 0200_non <- non
    │   └── 0201_bar.py <- 0300_bar.py
    ├── 0300_nope <- nope
    └── 0001_foo.py <- 020_foo.py

.. _usage_check_exit_signal:

Exit signal code
----------------

On basic usage the command will exit with signal code 0 if it does not encount a
programmatic error.

There is an option ``--exit-1`` that will cause to exit with signal code 1 if command
find resources to rename in given path. When there is no resource found to rename, the
exit code will always be 0.

.. _usage_rename:

'rename' command
****************

This command output a shell script to rename a structure. For a new structure you should
preview renaming with :ref:`usage_check`.


.. _usage_rename_prefix:

Prefix step
-----------

This work the same as with :ref:`usage_check_prefix`.


.. _usage_rename_without_prefix:

Process resources without prefix
--------------------------------

This work the same as with :ref:`usage_check_without_prefix`.


.. _usage_rename_excludes:

Excluding
---------

This work the same as with :ref:`usage_check_excludes`.


.. _usage_rename_command:

Shell command
-------------

Shell script to rename structure resources can be either ``mv`` or ``git mv``.

.. Note::
    The latter does not use GIT to ensure resources are committed to repository so it
    can output a script with resources that are not under version control.


.. _usage_help:

Help
****

There is a base tool help for global arguments: ::

    miss_lemon -h

And if you use ``-h`` after command name, you will get its specific help: ::

    miss_lemon greet -h
