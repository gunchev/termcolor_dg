termcolor_dg changes
====================

1.0.0 (2023-05-25)
------------------

- fix DISABLED detection
- logging.basicConfig has no disable_existing_loggers argument.
- move back to GitHub, workflows does work and is free.

0.9.3.1 (2022-02-14)
--------------------

- Adjust the log color scheme.
- pylint fixes in the color demo.

0.9.3 (2022-02-14)
------------------

- Adjust the log color scheme.
- pylint fixes in the color demo.

0.9.2 (2022-02-07)
------------------

- Combine color, background and attributes in a single escape sequence.
- Minor enhancements.

0.9.1 (2022-02-05)
------------------

- Rename to termcolor_dg (termcolor2 is taken).

0.9.0 (2022-02-05)
------------------

- Fork to termcolor2.
- Add 24-bit colors support.
- Add logging and color demos.
- Add ANSI_COLORS_DISABLED and ANSI_COLORS_FORCE environment variables.
- Add always_colored, rainbow_color.
- Add monkey_patch_logging and logging_basic_color_config utility functions.
- Better cprint and print compatibility (no arguments = new line).
- Drop 'gray' and 'on_gray' (it was an alias for black, bad idea?).
- Make the trailing reset sequence optional for colored.
- Use `python -m build` to build the project.
- Remove regex usage, the following would have not been stripped but works: `echo -e '(\e[01;32mx\e[1;0033mx\e[m)'`.
- Remove PKG-INFO.
- README.md instead of README.rst.
- ... unit tests, INSTALL ...

---

termcolor changes
=================

1.9.1 (2021-12-15)
------------------

- python 2 and 3 compatibility, avoid KeyError
- make pylint happy
- fix character escapes
- better .gitignore
- fix __ALL__ to __all__

1.1.0 (2011-01-13)
------------------

- Added cprint function.

1.0.1 (2011-01-13)
------------------

- Updated README.rst.

1.0.0 (2011-01-13)
------------------

- Changed license to MIT.
- Updated copyright.
- Refactored source code.

0.2 (2010-09-07)
------------------

- Added support for Python 3.x.

0.1.2 (2009-06-04)
------------------

- Fixed bold characters. (Thanks Tibor Fekete)

0.1.1 (2009-03-05)
------------------

- Some refactoring.
- Updated copyright.
- Fixed reset colors.
- Updated documentation.

0.1 (2008-06-09)
----------------

- Initial release.
