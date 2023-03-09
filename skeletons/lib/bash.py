"""Bash settings."""
from typing import Union, Optional

from skeletons.settings import INDENT, NEWLINE, CURLY_OPEN, CURLY_CLOSE

ENVAR = "{key}={value}"
DIR_OF_SCRIPT = '"$( cd "$( dirname "${BASH_SOURCE[0]}" )"'
DIR_OF_SCRIPT += ' >/dev/null 2>&1 && pwd )"'
SRC_IF_FILE = 'if [ -f "${file}" ]; then{NEWLINE}'
SRC_IF_FILE += '{INDENT}source "${file}"{NEWLINE}fi'
BASH_COLORS = {
    'black': r'\033[0;30m',
    'red': r'\033[0;31m',
    'green': r'\033[0;32m',
    'yellow':  r'\033[0;33m',
    'blue': r'\033[0;34m',
    'purple': r'\033[0;35m',
    'cyan': r'\033[0;36m',
    'light_gray': r'\033[37m',
    'dark_gray': r'\033[38m',
    'white': r'\033[0;37m',
    'bold_purple': r'\033[1;34m',
    'light_red': r'\033[91m',
    'light_yellow': r'\033[93m',
    'light_green': r'\033[92m',
    'light_blue': r'\033[94m',
    'nc': r"\033[0m",
    'default': r'\033[39m',
}
BASH_FUNCTION = '{name}() {CURLY_OPEN}{NEWLINE}'
BASH_FUNCTION += "{NEWLINE.join([INDENT + line for line in commands.splitlines()])}"
BASH_FUNCTION += "{CURLY_CLOSE}{NEWLINE}"


def make_bash_function(
    name: str, 
    commands: Optional[Union[list, str]]
) -> str:
    """Make bash function (name) full of (commands)."""
    if commands is None:
        commands = '\n'
    elif isinstance(commands, list):
        commands = '\n'.join(commands)
    if not isinstance(commands, str):
        raise TypeError(f'Expected str, got {type(commands)}')
    fxn = BASH_FUNCTION.format(name=name, CURLY_OPEN=CURLY_OPEN,
                               NEWLINE=NEWLINE, INDENT=INDENT,
                               commands=commands, CURLY_CLOSE=CURLY_CLOSE)
    return fxn


def _add_fxn_to_bf(name: str, commands: Union[list, str]):
    """Add a fxn to BASH_FUNCTIONS."""
    return {'name': name, 'commands': commands,
            'fxn': make_bash_function(name, commands),
            }


BASH_FUNCTIONS = {
    'info': _add_fxn_to_bf(
        name='info',
        commands=[
            'echo -e "' + BASH_COLORS['green'] + 'INFO $(date -Ins)' +
            BASH_COLORS['default'] + ' $1"',
        ]),
    'warn': _add_fxn_to_bf(
        name='warn',
        commands=[
            'echo -e "' + BASH_COLORS['yellow'] + 'WARNING $(date -Ins)' +
            BASH_COLORS['default'] + ' $1"',
        ]),
    'die': _add_fxn_to_bf(
        name='die',
        commands=[
            'echo -e "' + BASH_COLORS['red'] + 'FAILURE $(date -Ins)' +
            BASH_COLORS['default'] + ' $1"',
            'if [ -z "$2" ]; then',
            INDENT + 'exit "$2"',
            'fi',
            'exit 1',
        ]),
    'usage': _add_fxn_to_bf(
        name='usage',
        commands=[
            "grep '^#/' \"${BASH_SOURCE[0]}\" | cut -c4- || \\",
            'die "Failed to display usage information."'
            ]),
}
