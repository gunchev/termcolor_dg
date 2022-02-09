#!/usr/bin/python
# -*- coding: utf-8 -*-

"""termcolor_dg setup"""

from os.path import abspath, dirname, join as pjoin

from setuptools import setup


HERE = abspath(dirname(__file__))


if __name__ == '__main__':
    # https://github.com/pypa/sampleproject, https://stackoverflow.com/a/58534041/1136400
    # Any encoding works, all is latin-1 and allows for python2 compatibility.
    with open(pjoin(HERE, 'src', 'termcolor_dg.py'), 'r') as src:
        DATA = [i for i in src.readlines() if i.startswith('__')]
    META = dict((i[0].strip(), i[1].strip().strip("'\"")) for i in (ln.split('=', 1) for ln in DATA))
    setup(
        author=META['__author__'],
        author_email=META['__email__'],
        maintainer=META['__maintainer__'],
        maintainer_email=META['__maintainer_email__'],
    )
