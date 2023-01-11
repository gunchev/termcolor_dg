termcolor_dg
============

📦 [pypi/termcolor_dg](https://pypi.python.org/pypi/termcolor_dg) |
📑 [ANSI escape code](https://en.wikipedia.org/wiki/ANSI_escape_code) |
📑 [Color codes cheatsheet](https://delameter.github.io/termcolor)

ANSI Color formatting for terminal output and log coloring. Supports 16 color, 256 color and 24-bit color modes.

Python 2 support is present for legacy projects and because it is not too much work and I have to use it for now.


Example
-------

```python
>>> from termcolor_dg import colored, cprint
>>>
>>> print(colored('Hello, World!', 'light_red', 'on_blue'))
>>> cprint('Hello, World!', 'blue', 'on_light_red', ['reverse', 'blink'])
>>>
>>> print_red_on_cyan = lambda x: cprint(x, 'red', 'on_cyan')
>>> print_red_on_cyan('Hello, World!')
>>>
>>> for i in range(10):
>>>     cprint(str(i), 'magenta', end=' ' if i != 9 else '\n')
>>>
>>> import sys
>>> cprint("Attention!", 196, attrs=('bold'), file=sys.stderr)  # 256 color mode
>>> cprint("Attention!", (255, 0, 0), attrs=('bold'), file=sys.stderr)  # 24 bit color mode
>>>
>>> import logging
>>> from termcolor_dg import logging_basic_color_config
>>> logging_basic_color_config()
>>> logging.log(logging.INFO, 'test')
```


Colors demo screenshot (`python -m termcolor_dg`):
--------------------------------------------------

![colors.png](colors.png "Colors demo")


Colored logs demo screenshot (`python -m termcolor_dg logs`):
-------------------------------------------------------------

![color_logs.png](color_logs.png "Colorized logs demo")


Environment variables
---------------------

**ANSI_COLORS_FORCE**
  if set to anything, even empty string, color escape sequences will be added.

**ANSI_COLORS_DISABLED**
  if set to anything no coloring will be performed, overrides **ANSI_COLORS_FORCE**.

**NO_COLOR**
  if set to anything no coloring will be performed, overrides **ANSI_COLORS_FORCE**.
  see https://no-color.org/

If none of the environment variables is set the colors are used
only if the ``stdout`` is attached to a terminal: ``sys.stdout.isatty()``.


Text properties
---------------

| Text colors   | Text highlights | Alt Text highlights  | Attributes |
| ------------- | --------------- | -------------------- | ---------- |
| black         | black           | on_black             | bold       |
| red           | red             | on_red               | dark       |
| green         | green           | on_green             | underline  |
| yellow        | yellow          | on_yellow            | blink      |
| blue          | blue            | on_blue              | reverse    |
| magenta       | magenta         | on_magenta           | concealed  |
| cyan          | cyan            | on_cyan              |            |
| light_grey    | light_grey      | on_light_grey        |            |
| dark_grey     | dark_grey       | on_dark_grey         |            |
| light_red     | light_red       | on_light_red         |            |
| light_green   | light_green     | on_light_green       |            |
| light_yellow  | light_yellow    | on_light_yellow      |            |
| light_blue    | light_blue      | on_light_blue        |            |
| light_magenta | light_magenta   | on_light_magenta     |            |
| light_cyan    | light_cyan      | on_light_cyan        |            |
| white         | white           | on_white             |            |


Functions
---------

### Adding ANSI colors

**always_colored(text, color=None, on_color=None, attrs=None, reset=True)**
:   Returns the text with ANSI color code in front and ANSI color reset after. Arguments:
:   - **text** is the text to add color to
:   - **color** and **on_color** define the character and background color. Each can be a name for 16 color mode, number for the 256 color variant and list/tuple of R, G and B for the 24 bit color support. The following all define light red: **'light_red'**, **9**, **196** and **(255, 0, 0)**.
:   - **attrs** attributes, single attribute name, list or tuple of attributes.
:   - **reset** if set to **False** will suppress adding of the reset ANSI sequence at the end. Useful if you are joining another colored string, only the last reset is really needed.

**colored(text, color=None, on_color=None, attrs=None, reset=True)**
:   same as always_colored but checks if the app is running on a terminal and if the colors have been forced or disabled. The boolean **termcolor_dg.DISABLED** is the variable checked.


### Utility functions

**cprint(text='', color=None, on_color=None, attrs=None, \*\*kwargs)**
:   same as colored, but prints the resulting string instead of returning it.

**rainbow_color(n, steps, nmax=255)**
:   calculates the color at step **n** needed to produce a rainbow in **steps** steps with intensity up to **nmax**. Ex: **rainbow_color(0, 120)** returns **(255, 0, 0)**, **rainbow_color(30, 120)** returns **(128, 255, 0)**.

**monkey_patch_logging**
:   Monkeypatch **logging.Formatter** to add colors to the logs on a terminal, not customizable for now. Monkeypatch **logging.LogRecord.getMessage** to log formatting errors in the log format instead of throwing useless exception.

**logging_basic_color_config(level='DEBUG', fmt='%(asctime)s %(message)s  # %(filename)s:%(lineno)d %(name)s', color_on_terminal=True)**
:   Basic logging configuration, coloring and report formatting errors (**monkey_patch_logging**). Coloring code relies on '  # ' to determine the section to print in pale dark blue (comment).

**monkey_unpatch_logging**
:   Undo the monkeypatching done by **monkey_patch_logging** and remove coloring and error handling.

**COLOR_RESET_STR**
:   The color and attribute ANSI reset code.


## Similar projects

You may want to check out:

- 📦 [pypi/termcolor](https://pypi.python.org/pypi/termcolor) - the original project
- 📦 [delameter/termcolor](https://github.com/delameter/termcolor) - fork of the original termcolor_dg extends
- 📦 [pypi/colorama](https://pypi.org/project/colorama/) for more advanced options.


## Interesting links

- 📑 [Terminal Colors](https://github.com/termstandard/colors) discussion with examples
- 📑 [ANSI/VT100 Terminal Control Escape Sequences](https://www2.ccs.neu.edu/research/gpc/VonaUtils/vona/terminal/vtansi.htm)
- 📑 [ANSI escape code](https://en.wikipedia.org/wiki/ANSI_escape_code)
- 📑 [Color codes cheatsheet](https://delameter.github.io/termcolor)
- 📑 [MarkdownGuide - Basic Syntax](https://www.markdownguide.org/basic-syntax)


Terminal properties support
---------------------------
Assume this information is outdated.

| Terminal         |  bold  | dark | underline |  blink  | reverse | concealed | 256 colors | 24-bit color |
| :--------------- | :----: | :--: | :-------: | :-----: | :-----: | :-------: | :--------: | :----------: |
| **linux**        | ❌[^3] |❌[^3]|   ✅[^3]  |  ✅[^3] |    ✅   |     ❌    |     ❌     |      ❌      |
| **konsole**      |   ✅   |  ✅  |     ✅    |    ✅   |    ✅   |     ✅    |     ✅     |      ✅      |
| **terminator**   |   ✅   |  ✅  |     ✅    |    ✅   |    ✅   |     ✅    |     ✅     |      ✅      |
| **kitty**        |   ✅   |  ✅  |     ✅    |    ✅   |    ✅   |     ❌    |     ✅     |      ✅      |
| **xterm**        |   ✅   |  ❌  |     ✅    |    ✅   |    ✅   |     ✅    |     ✅     |      ✅      |
| **rxvt**         |   ✅   |  ❌  |     ✅    |    ✅   |    ✅   |     ❌    |     ✅     |      ❌      |
| **dtterm**       |   ✅   |  ✅  |     ✅    | reverse |    ✅   |     ✅    |     ❓     |      ❓      |
| **teraterm**     | reverse|  ❌  |     ✅    | rev/red |    ✅   |     ❌    |     ❓     |      ❓      |
| **aixterm**      | normal |  ❌  |     ✅    |    ❌   |    ✅   |     ✅    |     ❓     |      ❓      |
| **Windows**      |   ❌   |  ❌  |     ❌    |    ❌   |    ✅   |   ✅[^4]  |     ❓     |      ✅      |
| **PuTTY**        | ✅[^2] |  ✅  |     ✅    |  ✅[^1] |    ✅   |     ❌    |     ✅     |      ✅      |
| **Cygwin SSH**   |   ✅   |  ❌  |    color  |  color  |  color  |     ✅    |     ❓     |      ❓      |
| **Mac Terminal** |   ✅   |  ❓  |     ✅    |    ✅   |    ✅   |     ✅    |     ✅     |      ❓      |
| **iTerm2**       |   ✅   |  ❓  |     ✅    |    ✅   |    ✅   |     ✅    |     ✅     |      ✅      |

[^1]: Disabled by default

[^2]: Supports color change, bold text or both.

[^3]: See [VGA text mode](https://en.wikipedia.org/wiki/VGA_text_mode)

[^4]: See [Add support for the "concealed" graphic rendition attribute #6876 ](https://github.com/microsoft/terminal/issues/6876)

