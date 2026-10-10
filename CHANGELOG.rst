
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
* [ ] Test on 'check' command;

* [ ] Update README;
* [ ] Update documentation;
* [ ] Option to directly perform resource renaming with Python (but it won't be git)?
* [ ] Tox configuration should test both with or without Rich package;


Development
***********

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
