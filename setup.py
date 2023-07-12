#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""termcolor_dg setup"""

from os.path import abspath, dirname, join as pjoin

from setuptools import setup


def main():
    """setuptools setup"""
    # https://github.com/pypa/sampleproject, https://stackoverflow.com/a/58534041/1136400
    # Any encoding works, all is latin-1 and allows for python2 compatibility.
    here = abspath(dirname(__file__))
    name = 'termcolor_dg'
    with open(pjoin(here, 'src', name + '.py'), 'r') as src:
        data = [i for i in src.readlines() if i.startswith('__')]
    meta = dict((i[0].strip(), i[1].strip().strip("'\"")) for i in (ln.split('=', 1) for ln in data))
    setup(
        name=name,
        version=meta['__version__'],
        author=meta['__author__'],  # Optional
        author_email=meta['__email__'],  # Optional
        maintainer=meta['__maintainer__'],  # Optional
        maintainer_email=meta['__maintainer_email__'],  # Optional
        test_suite=name + '_tests',
    )


if __name__ == '__main__':
    main()
