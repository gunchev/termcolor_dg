# coding: utf-8
# Copyright (c) 2008-2011 Volvox Development Team
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Author: Konstantin Lepa <konstantin.lepa@gmail.com>

"""ANSII Color formatting for output in terminal."""

from __future__ import print_function
import os
import re
import sys


__all__ = [ 'colored', 'cprint' ]

VERSION = (1, 2, 0)

ATTRIBUTES = {
    'bold': 1,
    'dark': 2,
    'underline': 4,
    'blink': 5,
    'reverse': 7,
    'concealed': 8,
}

ATTRIBUTES_RE = '\033\[(?:%s)m' % '|'.join(['%d' % v for v in ATTRIBUTES.values()])

HIGHLIGHTS = {
    'on_black': 40,
    'on_grey': 40, # is actually black
    'on_red': 41,
    'on_green': 42,
    'on_yellow': 43,
    'on_blue': 44,
    'on_magenta': 45,
    'on_cyan': 46,
    'on_light_grey': 47,
    'on_dark_grey': 100,
    'on_light_red': 101,
    'on_light_green': 102,
    'on_light_yellow': 103,
    'on_light_blue': 104,
    'on_light_magenta': 105,
    'on_light_cyan': 106,
    'on_white': 107,
}

HIGHLIGHTS_RE = '\033\[(?:%s)m' % '|'.join(['%d' % v for v in HIGHLIGHTS.values()])

COLORS = {
    'black': 30,
    'grey': 30, # is actually black
    'red': 31,
    'green': 32,
    'yellow': 33,
    'blue': 34,
    'magenta': 35,
    'cyan': 36,
    'light_grey': 37,
    'dark_grey': 90,
    'light_red': 91,
    'light_green': 92,
    'light_yellow': 93,
    'light_blue': 94,
    'light_magenta': 95,
    'light_cyan': 96,
    'white': 97,
}

COLORS_RE = '\033\[(?:%s)m' % '|'.join(['%d' % v for v in COLORS.values()])

RESET = '\033[0m'
RESET_RE = '\033\[0m'


def colored(text, color=None, on_color=None, attrs=None):
    """Colorize text, while stripping nested ANSI color sequences.

    Available text colors:
        red, green, yellow, blue, magenta, cyan, white, black, light_grey,
        dark_grey, light_red, light_green, light_yellow, light_blue,
        light_magenta, light_cyan. Additionally, if 256 colors are supported,
        any integer between 1 and 255 can be provided.

    Available text highlights:
        on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan, on_black,
        on_white, on_light_grey, on_dark_grey, on_light_red, on_light_green,
        on_light_yellow, on_light_blue, on_light_magenta, light_cyan.
        Additionally, if 256 colors are supported, any integer between 1 and
        255 can be provided.

    Available attributes:
        bold, dark, underline, blink, reverse, concealed.

    Example:
        colored('Hello, World!', 'red', 'on_black', ['bold', 'blink'])
        colored('Hello, World!', 191, 182)
    """
    if os.getenv('ANSI_COLORS_DISABLED') is None and sys.stdout.isatty():
        fmt16_str = '\033[%sm%s'
        fmt256_str = '\033[%d;5;%dm%s'

        if color is not None:
            text = re.sub(COLORS_RE + '(.*?)' + RESET_RE, r'\1', text)
            if color in COLORS:
                text = fmt16_str % (COLORS[color], text)
            elif isinstance(color, int):
                text = fmt256_str % (38, color, text)
        if on_color is not None:
            text = re.sub(HIGHLIGHTS_RE + '(.*?)' + RESET_RE, r'\1', text)
            if on_color in HIGHLIGHTS:
                text = fmt16_str % (HIGHLIGHTS[on_color], text)
            elif isinstance(on_color, int):
                text = fmt256_str % (48, on_color, text)
        if attrs is not None:
            text = re.sub(ATTRIBUTES_RE + '(.*?)' + RESET_RE, r'\1', text)
            for attr in attrs if hasattr(attrs, '__iter__') else [attrs]:
                text = fmt16_str % (ATTRIBUTES[attr], text)
        return text + RESET
    else:
        return text


def cprint(text, color=None, on_color=None, attrs=None, **kwargs):
    """Print colorize text.

    It accepts arguments of print function.
    """

    print((colored(text, color, on_color, attrs)), **kwargs)


if __name__ == '__main__':
    print('Current terminal type: %s' % os.getenv('TERM'))
    print('Test colors:')
    cprint('Black color', 'black')
    cprint('Red color', 'red')
    cprint('Green color', 'green')
    cprint('Yellow color', 'yellow')
    cprint('Blue color', 'blue')
    cprint('Magenta color', 'magenta')
    cprint('Cyan color', 'cyan')
    cprint('White color', 'white')
    cprint('Light grey color', 'light_grey')
    cprint('Dark grey color', 'dark_grey')
    cprint('Light red color', 'light_red')
    cprint('Light green color', 'light_green')
    cprint('Light yellow color', 'light_yellow')
    cprint('Light blue color', 'light_blue')
    cprint('Light magenta color', 'light_magenta')
    cprint('Light cyan color', 'light_cyan')
    print(('-' * 78))

    print('Test highlights:')
    cprint('On black color', on_color='on_black')
    cprint('On red color', on_color='on_red')
    cprint('On green color', on_color='on_green')
    cprint('On yellow color', on_color='on_yellow')
    cprint('On blue color', on_color='on_blue')
    cprint('On magenta color', on_color='on_magenta')
    cprint('On cyan color', on_color='on_cyan')
    cprint('On white color', color='grey', on_color='on_white')
    print('-' * 78)

    print('Test attributes:')
    cprint('Bold black color', 'black', attrs=['bold'])
    cprint('Dark red color', 'red', attrs=['dark'])
    cprint('Underline green color', 'green', attrs=['underline'])
    cprint('Blink yellow color', 'yellow', attrs=['blink'])
    cprint('Reversed blue color', 'blue', attrs=['reverse'])
    cprint('Concealed Magenta color', 'magenta', attrs=['concealed'])
    cprint('Bold underline reverse cyan color', 'cyan',
            attrs=['bold', 'underline', 'reverse'])
    cprint('Dark blink concealed white color', 'white',
            attrs=['dark', 'blink', 'concealed'])
    print(('-' * 78))

    print('Test mixing:')
    cprint('Underline red on black color', 'red', 'on_black', ['underline'])
    cprint('Reversed green on red color', 'green', 'on_red', ['reverse'])
    print(('-' * 78))

    print('Test 256 colors:')
    for i in range(1,256):
        lb = '' if i % 16 != 0 else '\n'
        cprint(format(i, '3'), on_color=i, end=lb)
    print()
