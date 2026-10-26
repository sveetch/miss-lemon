.. _rename_intro:

======
Rename
======

This command output a shell script to rename a structure. For a new structure you should
preview renaming with :ref:`check_intro`.


.. _rename_prefix:

Prefix step
***********

This work the same as with :ref:`check_prefix`.


.. _rename_without_prefix:

Process resources without prefix
********************************

This work the same as with :ref:`check_without_prefix`.


.. _rename_excludes:

Excluding
*********

This work the same as with :ref:`check_excludes`.


.. _rename_command:

Shell command
*************

Shell script command to rename structure resources can be either ``mv`` or ``git mv``.

.. Note::
    The latter does not use GIT to ensure resources are committed to repository so it
    can output a script with resources that are not under version control.

The default used command is ``mv`` and would result with something like this: ::

    # This shell script will 'cd' into the source directory then apply renaming of resources.
    cd '/home/foo/sample_structure';
    mv '01000_models/001_managers/001_blog.py' '01000_models/001_managers/01101_blog.py';
    mv '01000_models/0103_category.py' '01000_models/01001_category.py';
    mv '020_foo.py' '00001_foo.py';
    mv '01000_models/001_managers' '01000_models/01100_managers';
    mv '01000_models/002_lookups' '01000_models/01200_lookups';
    mv '1000_views' '02000_views';
    echo "Finished all tasks!";

With command ``git mv`` selected it will result like this: ::

    # This shell script will 'cd' into the source directory then apply renaming of resources.
    cd '/home/foo/sample_structure';
    git mv '01000_models/001_managers/001_blog.py' '01000_models/001_managers/01101_blog.py';
    git mv '01000_models/0103_category.py' '01000_models/01001_category.py';
    git mv '020_foo.py' '00001_foo.py';
    git mv '01000_models/001_managers' '01000_models/01100_managers';
    git mv '01000_models/002_lookups' '01000_models/01200_lookups';
    git mv '1000_views' '02000_views';
    echo "Finished all tasks!";
