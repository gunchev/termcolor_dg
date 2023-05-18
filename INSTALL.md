# INSTALL

Refer to the official [Installing Python Modules](https://docs.python.org/3/installing/index.html) documentation for
proper installation for now.

If you are using Fedora Linux 36+ or similar RPM-based distribution,
you should be able to build an RPM package with `rpmbuild -ta termcolor_dg-\*.tar.gz`.

There is a quick and dirty and ... but working method - just copy src/termcolor_dg.py next to your script.

To run tests - `make test`, for other help on other Makefile targets just type **make**.
