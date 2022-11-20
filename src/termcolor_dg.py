#!/usr/bin/python
# -*- coding: utf-8 -*-

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
# Original author: Konstantin Lepa <konstantin.lepa@gmail.com>

'''ANSI Color formatting for terminal output and logging coloring.

Run `python -m termcolor_dg` for color demo

Run `python -m termcolor_dg logs` for colored logs demo
'''

from __future__ import absolute_import, print_function, division

import logging
import os
import shutil
import sys
import time


__all__ = ['always_colored', 'colored', 'cprint', 'rainbow_color', 'monkey_patch_logging', 'logging_basic_color_config',
           'COLOR_RESET_STR']

__version__ = '0.9.3.1'
__copyright__ = 'Copyright (c) 2008-2011 Volvox Development Team'
__license__ = 'MIT'

__author__ = 'Konstantin Lepa'
__email__ = 'konstantin.lepa@gmail.com'

__maintainer__ = 'Doncho N. Gunchev'
__maintainer_email__ = 'dgunchev@gmail.com'

__credits__ = ['Edmund Huber', 'Lukasz Balcerzak', 'Hendrik Buschmeier', 'Nat Meysenburg', 'Iulian PAUN']


# Python 2 and 3 compatibility
if sys.version_info >= (3, 0):  # pragma: no cover
    # raw_input = input  # @ReservedAssignment pylint: disable=C0103,redefined-builtin
    # unicode = str  # @ReservedAssignment pylint: disable=C0103,redefined-builtin
    basestring = str  # @ReservedAssignment pylint: disable=C0103,redefined-builtin
    # long = int  # @ReservedAssignment pylint: disable=C0103,redefined-builtin

DISABLED = os.getenv('ANSI_COLORS_DISABLED') is not None \
    or not sys.stdout.isatty() and os.getenv('ANSI_COLORS_FORCE') is None

COLOR_RESET_STR = '\033[0m'
ERASE_EOL_STR = '\033[2K'
RESET_STR = '\033c'

ATTRIBUTES = {
    'bold': '1',
    'dark': '2',
    'underline': '4',
    'blink': '5',
    'reverse': '7',
    'concealed': '8',
}

COLORS = {
    'black': '30',
    'red': '31',
    'green': '32',
    'yellow': '33',
    'blue': '34',
    'magenta': '35',
    'cyan': '36',
    'light_grey': '37',
    'dark_grey': '90',
    'light_red': '91',
    'light_green': '92',
    'light_yellow': '93',
    'light_blue': '94',
    'light_magenta': '95',
    'light_cyan': '96',
    'white': '97',
}

HIGHLIGHTS = dict((i[0], str(int(i[1]) + 10)) for i in COLORS.items())


def color_fmt(color, colors16, cnum):
    '''Format the color/background escape sequence chunk'''
    if isinstance(color, basestring):
        if color.startswith('on_'):  # backwards compatibility
            color = color[3:]
        if color in colors16:
            return colors16[color]
        raise ValueError("Invalid color %r" % color)

    if isinstance(color, int):
        if 0 <= color <= 255:
            return "%d;5;%d" % (cnum, color)
        raise ValueError("Invalid color %d" % color)

    if isinstance(color, (list, tuple)):
        if len(color) == 3 and 0 <= color[0] <= 255 and 0 <= color[1] <= 255 and 0 <= color[2] <= 255:
            return '%d;2;%d;%d;%d' % (cnum, color[0], color[1], color[2])
        raise ValueError("Invalid color %r" % (color,))

    raise TypeError("Unsupported color type %s" % type(color).__name__)


def always_colored(text, color=None, on_color=None, attrs=None, reset=True):
    '''Color text with ANSI escape codes

    color (text color): 'black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'light_grey', 'dark_grey',
        'light_red', 'light_green', 'light_yellow', 'light_blue', 'light_magenta', 'light_cyan', 'white'.

    on_color (text background): same as color but with 'on_' or 'on ' prefix.

    attributes: 'bold', 'dark', 'underline', 'blink', 'reverse', 'concealed'.

    reset: if set to false do not emit reset sequence at the end.

    Additionally, if 256 colors are supported, any integer between 1 and 255 can be provided for both foreground
    and background. A tuple/list with three integers (R, G, B) can be provided for 24 bit color.

    Examples:
        always_colored('Hello, World!', 'red', 'on_black', ['bold', 'blink'])
        always_colored('Hello, World!', 191, 182)
        always_colored('24bit color!', (255, 127, 127), (127, 127, 255), ['bold'])
    '''
    pfx = []
    if color is not None:
        pfx.append(color_fmt(color, COLORS, 38))

    if on_color is not None:
        pfx.append(color_fmt(on_color, HIGHLIGHTS, 48))

    if attrs is not None:
        for attr in [attrs] if isinstance(attrs, basestring) else attrs:
            if attr in ATTRIBUTES:
                pfx.append(ATTRIBUTES[attr])
            else:
                raise ValueError("Invalid attribute %r" % attr)

    if pfx:
        return '\033[' + ';'.join(pfx) + 'm' + text + (COLOR_RESET_STR if reset else '')

    return text


def colored(text, color=None, on_color=None, attrs=None, reset=True):
    '''Color text with ANSI escape codes if running on terminal (or overridden).

    Environment variables:
        - **ANSI_COLORS_FORCE**: any value (even empty) will force colorizing the text.
        - **ANSI_COLORS_DISABLED** any value (even empty) will disable colorization. Takes precedence.

    Available text colors:
        red, green, yellow, blue, magenta, cyan, white, black, light_grey, dark_grey, light_red, light_green,
        light_yellow, light_blue, light_magenta, light_cyan.

    Available text highlights:
        on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan, on_black, on_white, on_light_grey, on_dark_grey,
        on_light_red, on_light_green, on_light_yellow, on_light_blue, on_light_magenta, light_cyan.

    Additionally, if 256 colors are supported, any integer between 1 and 255 can be provided for both
    foreground and background. A tuple/list with three elements (R, G, B) can be used for 24 bit color.

    Available attributes:
        bold, dark, underline, blink, reverse, concealed.

    Examples:
        colored('Hello, World!', 'red', 'on_black', ['bold', 'blink'])
        colored('Hello, World!', 191, 182)
        colored('24bit color!', (255, 127, 127), (127, 127, 255), ['bold'])
    '''
    if DISABLED:
        return text

    return always_colored(text, color, on_color, attrs, reset)


def cprint(text='', color=None, on_color=None, attrs=None, reset=True, **kwargs):
    '''
    Print colorized text.

    It accepts arguments of print function.
    '''
    print(colored(text, color, on_color, attrs, reset), **kwargs)


def rainbow_color(n, steps, nmax=255):
    '''Calculate rainbow color'''
    if not isinstance(n, int) and isinstance(steps, int):
        raise TypeError('Arguments must be integers')
    if steps < 6:
        raise ValueError('Total must be at least 6')

    n %= steps
    progress = float(n) / steps
    r_value = max(0, min(nmax, abs(3 * nmax - 6 * progress * nmax) - nmax))

    n = (n - float(steps) / 3) % steps
    progress = float(n) / steps
    g_value = max(0, min(nmax, abs(3 * nmax - 6 * progress * nmax) - nmax))

    n = (n - float(steps) / 3) % steps
    progress = float(n) / steps
    b_value = max(0, min(nmax, abs(3 * nmax - 6 * progress * nmax) - nmax))

    return round(r_value), round(g_value), round(b_value)


def monkey_patch_logging_format():
    '''Monkey patches the logging module format error report'''
    if getattr(logging.LogRecord, 'distGetMessage', None) is not None:
        return

    logging.LogRecord.distGetMessage = logging.LogRecord.getMessage

    def print_log_record_on_error(func):
        '''Monkeypatch for logging.LogRecord.getMessage

        Credits: https://stackoverflow.com/questions/2477934/'''

        def wrap(self, *args, **kwargs):
            '''Generate wrapper function for logging.LogRecord.getMessage'''
            try:
                return func(self, *args, **kwargs)
            except Exception as exc:  # pylint: disable=broad-except
                return 'Error logging msg=%r, args=%r: %r' \
                    % (getattr(self, 'msg', '?'), getattr(self, 'args', '?'), exc)

        return wrap

    # Monkeypatch the logging library for more informative formatting errors
    logging.LogRecord.getMessage = print_log_record_on_error(logging.LogRecord.getMessage)


def monkey_unpatch_logging_format():
    '''Undo monkey_patch_logging_format'''
    if getattr(logging.LogRecord, 'distGetMessage', None) is None:
        return
    logging.LogRecord.getMessage = logging.LogRecord.distGetMessage  # @UndefinedVariable
    delattr(logging.LogRecord, 'distGetMessage')


def monkey_patch_logging(color_on_terminal=True):
    '''Monkey patches the logging module and add colors if enabled'''

    if getattr(logging, 'DistFormatter', None) is not None:
        return True

    monkey_patch_logging_format()

    if color_on_terminal and not DISABLED:
        # Monkey patches the logging module to print in color'

        def get_formatter(logging_formatter=logging.Formatter):
            '''Get it? ;-)'''

            class ColoredFormatter(logging_formatter):
                '''Color console formatter'''

                def format(self, record):
                    output = logging_formatter.format(self, record)
                    tail = None
                    comment_pos = output.find('  # ')  # Intentionally require two spaces before
                    if comment_pos >= 0:
                        output, tail = output[:comment_pos], output[comment_pos:]

                    if record.levelno < logging.DEBUG:  # pylint: disable=fixme
                        output = colored(text=output, color='black', on_color='on_blue', attrs=['dark'])
                    elif record.levelno <= logging.DEBUG:  # pylint: disable=fixme
                        output = colored(text=output, color='blue', on_color=None, attrs=['dark'])
                    elif record.levelno <= logging.INFO:
                        output = colored(text=output, color='green', on_color=None, attrs=['bold'])
                    elif record.levelno <= logging.WARNING:
                        output = colored(text=output, color='yellow', on_color=None, attrs=['bold'])
                    elif record.levelno <= logging.ERROR:
                        output = colored(text=output, color='red', on_color=None, attrs=['bold'])
                    elif record.levelno <= logging.CRITICAL:
                        output = colored(text=output, color='white', on_color='on_red', attrs=['bold'])
                    else:
                        output = colored(text=output, color='yellow', on_color='on_red',
                                         attrs=['bold', 'underline'])
                    if tail:
                        output += colored(text=tail, color='black', attrs=['dark'])

                    return output

                def formatException(self, ei):
                    '''Format and return the specified exception information as a string.'''
                    text = logging_formatter.formatException(self, ei)
                    text = '\n'.join(ERASE_EOL_STR + i for i in text.splitlines())
                    return colored(text=text, color='white', on_color='on_magenta', attrs=('bold'))

            return ColoredFormatter

        logging.DistFormatter = logging.Formatter
        logging.Formatter = get_formatter()

    return True


def monkey_unpatch_logging():
    '''Undo monkey_patch_logging'''

    monkey_unpatch_logging_format()

    if getattr(logging, 'DistFormatter', None) is not None:
        logging.Formatter = logging.DistFormatter  # @UndefinedVariable
        delattr(logging, 'DistFormatter')


def logging_basic_color_config(level='DEBUG', fmt='%(asctime)s %(message)s  # %(filename)s:%(lineno)d %(name)s',
                               color_on_terminal=True):
    '''Setup basic logging with fancy format and colors if running on terminal

    a very fancy fmt would be "%(asctime)s %(levelname)-8s: %(message)s  # %(filename)s:%(lineno)d %(name)s"
    '''
    monkey_patch_logging(color_on_terminal=color_on_terminal)
    try:
        logging.basicConfig(level=level, format=fmt, disable_existing_loggers=False)
    except ValueError:
        logging.basicConfig(level=level, format=fmt)


def termcolor_demo_16():
    '''Base 16 color demo'''
    colors = ('black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'light_grey', 'dark_grey', 'light_red',
              'light_green', 'light_yellow', 'light_blue', 'light_magenta', 'light_cyan', 'white')
    max_len = max(len(color) for color in colors)

    print(RESET_STR, end='')
    print(('--- 16 color mode test on TERM=%r ' % os.getenv('TERM')).ljust(119, '-'))

    for i, color in enumerate(colors):
        print(' ', end='')
        cprint(color.replace('_', ' ').center(max_len), color=color,
               on_color='on_black' if color != 'black' else 'on_dark_grey', end='' if i != 7 else '\n')
    print()

    for i, color in enumerate(colors):
        print(' ', end='')
        cprint(color.replace('_', ' ').center(max_len), color='black' if color != 'black' else 'dark_grey',
               on_color='on_' + color, end='' if i != 7 else '\n')
    print()

    print('Attributes:')
    all_attrs = ('bold', 'dark', 'underline', 'blink', 'reverse', 'concealed')
    attr_max_len = max(len(attr) for attr in all_attrs)

    print(' [' + colored('None'.center(attr_max_len), color='light_green', on_color='on_black') + ']', end='')
    for attr in all_attrs:
        print(' [' + colored(attr.center(attr_max_len), color='light_green', on_color='on_black', attrs=[attr]) + ']',
              end='')
    print(' last one should be invisible')

    print()
    print(' [' + '   Bold black on black    ', end=']')
    print(' [' + '       Dark white         ', end=']')
    print(' [' + '     Underline green      ', end=']')
    print(' [' + '      Blink yellow        ', end=']\n')
    print(' [' + colored('   Bold black on black    ', 'black', 'on_black', attrs=['bold']), end=']')
    print(' [' + colored('       Dark white         ', 'white', attrs=['dark']), end=']')
    print(' [' + colored('     Underline green      ', 'green', attrs=['underline']), end=']')
    print(' [' + colored('      Blink yellow        ', 'yellow', attrs=['blink']), end=']\n')

    print(' [' + colored('      Reversed blue       ', 'blue', attrs=['reverse']), end=']')
    print(' [' + colored('    Concealed Magenta     ', 'magenta', attrs=['concealed']), end=']')
    print(' [' + colored('Bold underline reverse red', 'red', attrs=['bold', 'underline', 'reverse']), end=']')
    print(' [' + colored('Dark blink concealed white', 'white', attrs=['dark', 'blink', 'concealed']), end=']\n')
    print(' [' + '      Reversed blue       ', end=']')
    print(' [' + '    Concealed Magenta     ', end=']')
    print(' [' + 'Bold underline reverse red', end=']')
    print(' [' + 'Dark blink concealed white', end=']\n')

    def all_combos(values):
        '''Generate all combinations'''
        values = tuple(values)
        if values:
            for i in all_combos(values[1:]):
                yield i
                yield [values[0]] + i
        else:
            yield []

    print('\nAttribute salad (Bold, Dark, Underline, blinK, Reverse, Concealed):')
    for idx, attrs in enumerate(all_combos(all_attrs)):
        code = 'B' if 'bold' in attrs else 'b'
        code += 'D' if 'dark' in attrs else 'd'
        code += 'U' if 'underline' in attrs else 'u'
        code += 'K' if 'blink' in attrs else 'k'
        code += 'R' if 'reverse' in attrs else 'r'
        code += 'C' if 'concealed' in attrs else 'c'
        print(' [' if idx % 16 == 0 else ' ' + colored(code, attrs=attrs), end='' if idx % 16 != 15 else ' ]\n')


def termcolor_demo_256():
    '''256 color demo'''
    print('\n--- 256 color mode test '.ljust(120, '-'))
    print(' First 16: [', end='')
    for i in range(16):
        cprint('%3d ' % i, color=15 - i, on_color=i, end='', reset=i == 15)
    print(']')

    print()

    print('6*6*6 cube:')
    for y in range(6):
        for x in range(6):
            print(' ', end='')
            for i in range(6):
                background = 16 + y * 6 * 6 + x * 6 + i
                cprint('%3x' % background, color='white' if y < 3 else 'black', on_color=background, end='')
        print()

    print()

    print(' 24 grayscale test:  [', end='')
    for i in range(232, 256):
        # cprint('%4d' % i, color='white' if i < 244 else 'black', on_color=i, end='')
        cprint('%4d' % i, color=(232 + 255) - i, on_color=i, end='')
    print(']\n')


def termcolor_demo_24bit():
    '''24 bit color demo'''
    data = '=== 24 bit color mode test '.ljust(114, '=')
    for i in range(2 * len(data), -1, -1):
        print('\r   ', end='')
        grey = abs(i * 8 % 510 - 255)
        print(
            colored(
                ''.join(colored(char, on_color=rainbow_color(step + i, len(data)), reset=False)
                        for step, char in enumerate(data)),
                color=(grey, grey, grey)
            ), end='')

        sys.stdout.flush()
        time.sleep(0.02)

    print('\r   ', end='')
    for step, char in enumerate(data):
        print(colored(char,
                      rainbow_color(step - len(data) // 3, len(data)),
                      on_color=rainbow_color(step, len(data)), reset=False), end='')
        sys.stdout.flush()
        time.sleep(0.02)
        print(COLOR_RESET_STR, end='')

    print()


def get_term_width():
    '''Get terminal width, there is https://gist.github.com/mr700/c73af70357ff8bcfc3250ee6c84e164d but it is overkill'''
    try:
        return shutil.get_terminal_size(fallback=(80, 32)).columns  # @UndefinedVariable
    except AttributeError:  # pragma: no cover
        return 120          # pragma: no cover


def termcolor_demo():
    '''Demonstrate this module's capabilities'''
    termcolor_demo_16()
    termcolor_demo_256()
    if get_term_width() >= 120:
        termcolor_demo_24bit()
    else:
        print("Need terminal width of 120 or more for this part...")  # pragma: no cover


def color_log_demo():
    '''Test color logging on terminal and logging format error'''
    # monkey_patch_logging(color_on_terminal=True)
    logging_basic_color_config()

    log = logging.getLogger('logger')
    print('Logging test... levels and exception:')

    # Hack to skip the log level test
    log._log(logging.NOTSET, 'Not set, below DEBUG, normally not show...', [])  # pylint: disable=W0212
    log.debug('Debug')
    log.info('Info')
    log.warning('Warning')
    log.error('Error')
    log.critical('Critical')
    log.error('x', 1)  # the mistake is intentional pylint: disable=logging-too-many-args
    log.info('%d', 1, 2)  # the mistake is intentional pylint: disable=logging-too-many-args
    log.debug('%d %d', 'a', 2)
    try:
        raise TypeError('msg')
    except TypeError:
        log.exception('Exception')
    log.log(51, 'ABOVE CRITICAL!')
    log.info('Done.')


def main():
    '''Main demo entry point, if no arguments - color demo, if any - colored logs demo'''
    if len(sys.argv) == 1:       # pragma: no cover
        return termcolor_demo()  # pragma: no cover
    return color_log_demo()      # pragma: no cover


if __name__ == '__main__':
    sys.exit(main())
