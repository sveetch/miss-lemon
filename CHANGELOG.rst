
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
* [ ] CRITICAL: Resources resulting in the same name must never be in the output. While
  'mv' would not say anything, for 'git-mv' it is an error to do 'git mv foo.py foo.py';
* [ ] Even the collector seems to collect in order on 'path.name', ignoring original
  included prefix, which is a part of the original order to take care;
* [ ] There is a failure with git-mv: all resources are collected according to user
  options, even resources not registered in repository, which will be in final output,
  and then git will refuse to process them;

* [ ] Conditionnate tests around Rich to its effective installation;

* [x] Update README;
* [x] Update documentation;

* [ ] Tox configuration should test both with or without Rich package;
* [ ] Better "Usage" documentation for commands;

* [ ] Option to directly perform resource renaming with Python (but it won't be git)?


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
