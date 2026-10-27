
=========
Changelog
=========

Version 0.3.0 - 2026/10/27
**************************

* Fixed order of tree output in 'check' command;
* Fixed 'rename' command to not output resources that lead to the same path;
* Ensure tests are working if Rich is not installed and update Tox configuration to
  cover with or without Rich;
* Changed 'check' command so the ignored resources does not display anymore on default,
  a new option allows to show them again;
* Added new option to 'check' command to abort with a signal code 1 if there is some
  resource eligible to renaming (this can be used in quality task to validate a
  structure does not need to be renamed);
* Changed 'check' command output to add an ending slash on directory resource nodes;
* Changed 'rename' command so it return a message and exist with signal code 1 if there
  is no resource found to rename;
* Improved test coverage;
* Improved documentation;


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


Version 0.1.0 - 2026/09/25
**************************

* First commit.
