
=========
Changelog
=========

TODO
****

* [x] Option to allow to collect also files without prefix;
* [x] Option to define excluded unix filename patterns;
* [x] Implement collect options in both commands;
* [x] DiffTree to improve 'check' command to display a tree of the current structure
  from path annotated with computing status (new name, ignored/excluded);
* [x] 'check' dynamic choices for '--output', 'rich' should be allowed only if rich
  stack is available;
* [x] Test on 'check' command;

* [x] Order of tree with 'check' is often bad, it is descending (9->1) while we expecte
  ascending and is order on name (without prefix) but visually it would be expected to
  be order on the final full name;
* [x] CRITICAL: Resources resulting in the same name must never be in the output. While
  'mv' would not say anything, for 'git-mv' it is an error to do 'git mv foo.py foo.py';
* [x] Conditionnate tests around Rich to its effective installation;
* [x] 'DiffTree' is never tested directly, only through the 'check' command;
* [x] Tree display should not display children of ignored resource, and options may
  allows to display them anyway;

  * [x] hidden_status management in 'DiffTree.build_bigtree()'
  * [x] Test 'check' cli for hidden_status options;

* [x] When there is no resources to rename:

  * [x] check command: Output a simple message.
  * [x] check command: Add an option to return sys.exit error when there is a resource
    to rename (for quality usage);
  * [x] rename command: Output an error and sys.exit error.

* [x] In 'check' output trees, directory resources should ends with a ``/``;
* [ ] There is a failure with git-mv: all resources are collected according to user
  options, even resources not registered in repository, which will be in final output,
  and then git will refuse to process them;

  * [ ] 'git ls-files --error-unmatch <file name>' can help to diagnosize a resource GIT
    status HOWEVER it would work only if command is done inside the Git repository;
  * [ ] Or via https://pypi.org/project/GitPython/ , it would allows to run git command
    outside the repository;

* [ ] Look at https://trees.software/#git-status for possible improvement of 'check' tree ?

* [x] Update README;
* [x] Update documentation;
* [x] Tox configuration should test both with or without Rich package;

* [ ] Better "Usage" documentation for commands;

* [ ] Option to directly perform resource renaming with Python (but it won't be git)?


Development
***********

* Fixed order of tree output in 'check' command;
* Fixed 'rename' command to not output resources that lead to the same path;
* Ensure tests are working if Rich is not installed and update Tox configuration to
  cover with or without Rich;
* Changed 'check' command so the ignored resources does not display anymore on default,
  a new option allows to show them again;
* Added new option to 'check' command to abort with a signal code 1 if there is some
  resource eligible to renaming (this can be used in quality task to validate a
  structure does not need to be renamed);
* Changed 'rename' command so it return a message and exist with signal code 1 if there
  is no resource found to rename;
* Improved test coverage;


Version 0.2.0 - 2026/10/11
**************************

* Implemented resource collect;
* Implemented resource prefix computation;
* Test coverage;
* Added 'check' command to collect resources, compute their prefix and display
  them for a simple human check;
* Added 'rename' command to collect resources, compute their prefix and output commands
  to apply renaming with new prefix. Command lines can use either 'mv' or 'git mv'
  depending option '--output';
* Added both "Big Tree" and "Rich Tree" support for preview from 'check' command;


Version 0.1.0 - Unreleased
**************************

* First commit.
