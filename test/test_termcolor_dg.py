#!/usr/bin/python
# -*- coding: utf-8 -*-

'''termcolor_dg unit tests'''

from __future__ import absolute_import, print_function, division

import io
import logging
import sys
import time
import unittest

import termcolor_dg


# Python 2 and 3 compatibility
if sys.version_info[0] == 3:
    raw_input = input  # @ReservedAssignment pylint: disable=C0103,redefined-builtin
    unicode = str  # @ReservedAssignment pylint: disable=C0103,redefined-builtin
    basestring = str  # @ReservedAssignment pylint: disable=C0103,redefined-builtin
    long = int  # @ReservedAssignment pylint: disable=C0103,redefined-builtin


class CapturedOutput:
    '''Temporary replace sys.stdout and sys.stderr with io.StringIO or io.BytesIO'''

    def __init__(self):
        self._buf = io.BytesIO() if sys.version_info < (3, 0) else io.StringIO()
        self._stdout, self._stderr = sys.stdout, sys.stderr

    def __enter__(self):
        sys.stdout, sys.stderr = self._buf, self._buf
        return self

    def __exit__(self, ex_type, ex_value, ex_traceback):  # @UnusedVariable
        sys.stderr, sys.stdout = self._stderr, self._stdout
        return False  # return True  # To stop any exception from propagating

    def get_output(self):
        '''Get what was written so far'''
        return self._buf.getvalue()


class Coffeine:
    '''Temporary replace time.sleep() with pass'''

    def __init__(self):
        self._sleep = time.sleep

    def __enter__(self):
        time.sleep = lambda _: None
        return self

    def __exit__(self, ex_type, ex_value, ex_traceback):  # @UnusedVariable
        time.sleep = self._sleep
        return False  # return True  # To stop any exception from propagating


class TestTermcolorDg(unittest.TestCase):
    '''Test the termcolor_dg module'''

    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName=methodName)
        self._disabled = termcolor_dg.DISABLED

    def setUp(self):
        unittest.TestCase.setUp(self)
        termcolor_dg.DISABLED = False

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        termcolor_dg.DISABLED = self._disabled

    def test_main_exists(self):
        '''Check if main is defined in the module'''
        for fname in ('always_colored', 'colored', 'cprint', 'rainbow_color', 'monkey_patch_logging',
                      'logging_basic_color_config', 'monkey_unpatch_logging', 'monkey_unpatch_logging_format'):
            self.assertIn(fname, termcolor_dg.__dict__.keys(), '%r not defined?!?' % fname)

    def test_cprint_no_color(self):
        '''Check if main is printing the proper string'''
        with CapturedOutput() as out:
            termcolor_dg.cprint('test')
            output = out.get_output()
        self.assertEqual(output, 'test\n')

    # @unittest.skipIf(not sys.stdout.isatty(), 'Not testing on non-tty')
    def test_cprint(self):
        '''Check if main is printing the proper string'''
        with CapturedOutput() as out:
            termcolor_dg.cprint('test')
            output = out.get_output()
        self.assertEqual(output, 'test\n')

    def test_colored(self):
        '''Basics'''
        self.assertEqual(termcolor_dg.colored('test', 'red'), '\x1b[31mtest\x1b[0m')
        self.assertEqual(termcolor_dg.colored('test', color='red'), '\x1b[31mtest\x1b[0m')
        self.assertEqual(termcolor_dg.colored('test', 2), '\x1b[38;5;2mtest\x1b[0m')
        self.assertEqual(termcolor_dg.colored('test', (0, 0, 255)), '\x1b[38;2;0;0;255mtest\x1b[0m')

        self.assertEqual(termcolor_dg.colored('test', on_color='on_red'), '\x1b[41mtest\x1b[0m')
        self.assertEqual(termcolor_dg.colored('test', on_color=2), '\x1b[48;5;2mtest\x1b[0m')
        self.assertEqual(termcolor_dg.colored('test', None, (0, 0, 255)), '\x1b[48;2;0;0;255mtest\x1b[0m')

        self.assertEqual(termcolor_dg.colored('test', 'red', 'on_blue', ['bold']), '\x1b[31;44;1mtest\x1b[0m')
        self.assertEqual(termcolor_dg.colored('test', 'red', 'on_blue', ['bold'], reset=False), '\x1b[31;44;1mtest')

        termcolor_dg.DISABLED = True
        self.assertEqual(termcolor_dg.colored('test', 'red'), 'test')

    def test_always_colored(self):
        '''Basics'''
        self.assertEqual(termcolor_dg.always_colored('test', 'red'), '\x1b[31mtest\x1b[0m')
        self.assertEqual(termcolor_dg.always_colored('test', color='red'), '\x1b[31mtest\x1b[0m')
        self.assertEqual(termcolor_dg.always_colored('test', 2), '\x1b[38;5;2mtest\x1b[0m')
        self.assertEqual(termcolor_dg.always_colored('test', (0, 0, 255)), '\x1b[38;2;0;0;255mtest\x1b[0m')

        self.assertEqual(termcolor_dg.always_colored('test', on_color='on_red'), '\x1b[41mtest\x1b[0m')
        self.assertEqual(termcolor_dg.always_colored('test', on_color=2), '\x1b[48;5;2mtest\x1b[0m')
        self.assertEqual(termcolor_dg.always_colored('test', None, (0, 0, 255)), '\x1b[48;2;0;0;255mtest\x1b[0m')

        self.assertEqual(termcolor_dg.always_colored('test', 'red', 'on_blue', ['bold']), '\x1b[31;44;1mtest\x1b[0m')
        self.assertEqual(termcolor_dg.always_colored('test', 'red', 'on_blue', ['bold'], reset=False),
                         '\x1b[31;44;1mtest')

    def test_rainbow_color(self):
        '''Test rainbow_color'''
        self.assertEqual(termcolor_dg.rainbow_color(0, 18), (255, 0, 0))
        self.assertEqual(termcolor_dg.rainbow_color(1, 18), (255, 85, 0))
        self.assertEqual(termcolor_dg.rainbow_color(2, 18), (255, 170, 0))
        self.assertEqual(termcolor_dg.rainbow_color(3, 18), (255, 255, 0))
        self.assertEqual(termcolor_dg.rainbow_color(4, 18), (170, 255, 0))
        self.assertEqual(termcolor_dg.rainbow_color(5, 18), (85, 255, 0))
        self.assertEqual(termcolor_dg.rainbow_color(6, 18), (0, 255, 0))
        self.assertEqual(termcolor_dg.rainbow_color(7, 18), (0, 255, 85))
        self.assertEqual(termcolor_dg.rainbow_color(8, 18), (0, 255, 170))
        self.assertEqual(termcolor_dg.rainbow_color(9, 18), (0, 255, 255))
        self.assertEqual(termcolor_dg.rainbow_color(10, 18), (0, 170, 255))
        self.assertEqual(termcolor_dg.rainbow_color(11, 18), (0, 85, 255))
        self.assertEqual(termcolor_dg.rainbow_color(12, 18), (0, 0, 255))
        self.assertEqual(termcolor_dg.rainbow_color(13, 18), (85, 0, 255))
        self.assertEqual(termcolor_dg.rainbow_color(14, 18), (170, 0, 255))
        self.assertEqual(termcolor_dg.rainbow_color(15, 18), (255, 0, 255))
        self.assertEqual(termcolor_dg.rainbow_color(16, 18), (255, 0, 170))
        self.assertEqual(termcolor_dg.rainbow_color(17, 18), (255, 0, 85))
        with self.assertRaises(TypeError):
            termcolor_dg.rainbow_color('17', 18)
        with self.assertRaises(TypeError):
            termcolor_dg.rainbow_color(17, '18')
        with self.assertRaises(ValueError):
            termcolor_dg.rainbow_color(5, 2)

    def test_log_demo(self):
        '''Check the log demo output'''
        with CapturedOutput() as out:
            termcolor_dg.color_log_demo()
            output = out.get_output()

        self.assertTrue(termcolor_dg.monkey_patch_logging())

        head_expected = 'Logging test... levels and exception:\n\x1b[30;44;2m'
        self.assertEqual(output[:len(head_expected)], head_expected)
        tail_expected = ' logger\x1b[0m\n'
        self.assertEqual(output[-len(tail_expected):], tail_expected)
        output_len = 1574
        if sys.version_info[:2] == (3, 10):
            output_len = 1579
        elif sys.version_info[:2] == (3, 6):
            output_len = 1577
        elif sys.version_info[:2] == (2, 7):
            output_len = 1577
        self.assertEqual(len(output), output_len)  # Well...
        split_chunks = (
            (10, 'DEBUG,'),
            (88, "TypeError('%d"),
            (89, 'format:'),
            (90, 'a'),
            (-4, 'Done.\x1b[0m\x1b[30;2m'),
            (-1, 'logger\x1b[0m')
        )
        output_split = output.split()
        for chunk_no, chunk_value in split_chunks:
            self.assertEqual(output_split[chunk_no], chunk_value)

        # cover the "no tail" logging case
        log_record = logging.LogRecord('name', logging.INFO, 'pathname', 1, 'test', [], None)
        out = logging.Formatter('%(message)s').format(log_record)
        self.assertEqual(out, '\x1b[32;1mtest\x1b[0m')
        # Cover the disabled ...
        termcolor_dg.monkey_unpatch_logging()
        termcolor_dg.monkey_unpatch_logging()
        termcolor_dg.DISABLED = True
        self.assertTrue(termcolor_dg.monkey_patch_logging())
        self.assertTrue(termcolor_dg.monkey_patch_logging())
        termcolor_dg.DISABLED = False

    def test_color_demo(self):
        '''Check the log demo output'''
        with CapturedOutput() as out, Coffeine() as a_stimulant:  # @UnusedVariable pylint: disable=unused-variable
            termcolor_dg.termcolor_demo()
            output = out.get_output()

        self.assertEqual(len(output), 477595, "Unexpected output size")
        self.assertEqual(output[:33], '\x1bc--- 16 color mode test on TERM=', 'Bad output start')
        tail = ';40m=\x1b[0m\x1b[38;2;0;27;255;48;2;255;0;27m=\x1b[0m\x1b[38;2;0;13;255;48;2;255;0;13m=\x1b[0m\n'
        self.assertEqual(output[-80:], tail, 'Bad output tailing 80 chars')

    def test_errors(self):
        '''Check exceptions are thrown'''
        # Color exceptions
        with self.assertRaises(ValueError):
            termcolor_dg.always_colored('', 'invalid_color')
        with self.assertRaises(ValueError):
            termcolor_dg.always_colored('', 256)
        with self.assertRaises(ValueError):
            termcolor_dg.always_colored('', -1)
        with self.assertRaises(ValueError):
            termcolor_dg.always_colored('', (1, 2))
        with self.assertRaises(ValueError):
            termcolor_dg.always_colored('', (1, 2, -1))
        with self.assertRaises(ValueError):
            termcolor_dg.always_colored('', (1, 2, 256))
        with self.assertRaises(TypeError):
            termcolor_dg.always_colored('', {})
        # Background exceptions
        with self.assertRaises(ValueError):
            termcolor_dg.always_colored('', on_color='invalid_color')
        with self.assertRaises(ValueError):
            termcolor_dg.always_colored('', on_color=256)
        with self.assertRaises(ValueError):
            termcolor_dg.always_colored('', on_color=-1)
        with self.assertRaises(ValueError):
            termcolor_dg.always_colored('', on_color=(1, 2))
        with self.assertRaises(ValueError):
            termcolor_dg.always_colored('', on_color=(1, 2, -1))
        with self.assertRaises(ValueError):
            termcolor_dg.always_colored('', on_color=(1, 2, 256))
        with self.assertRaises(TypeError):
            termcolor_dg.always_colored('', on_color={})
        # Attribute exceptions
        with self.assertRaises(ValueError):
            termcolor_dg.always_colored('', attrs='invalid_attribute')
        with self.assertRaises(ValueError):
            termcolor_dg.always_colored('', attrs=['invalid_attribute'])


if __name__ == '__main__':
    unittest.main()
