
=========
Changelog
=========

TODO
****

* [x] Option to allow to collect also files without prefix;
* [x] Option to define excluded unix filename patterns;
* [ ] Implement option in both commands;

* [ ] Option to directly perform resource renaming with Python (but it won't be git)?


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


Version 0.1.0 - Unreleased
**************************

* First commit.
