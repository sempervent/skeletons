"""Write in python."""
from typing import Optional, Union, List

from skeletons.settings import NEWLINE, INDENT


class PyArgumentObject:
    """Define a class for a python argument."""

    def __init__(
        self, 
        name: str, 
        default: Optional[str],
        typ: Optional[str],
    ):
        """Initialize a PyArgumentObject."""
        self.name = name
        self.default = default
        self.type = typ

    def __str__(self):
        return self.value()

    def value(self):
        """Return a string representation."""
        string = f'{self.name}'
        if self.type:
            string += f': {self.type}'
        if self.default:
            string += f' = {self.default}'
        return string


def make_import_statement(
    module: str,
    obj: Optional[Union[List[str], str]],
    alias: Optional[str],
) -> str:
    """Make an import statement."""
    statement = ""
    if obj:
        if isinstance(obj, str):
            statement += f'from {module} import {obj}'
        elif isinstance(obj, list):
            objs = ', '.join(obj)
            statement += f'from {module} import {objs}'
    else:
        statement += f'import {module}'
    if alias:
        statement += f' as {alias}'
    return statement


def make_function(
    name: str,
    args: Optional[Union[PyArgumentObject, List[PyArgumentObject]]] = None,
    docstring: Optional[str] = None,
    logic: Optional[str, list] = None,
) -> str:
    """Make a python function."""
    string = f'def {name}('
    if isinstance(args, PyArgumentObject):
        string += args.value()
    elif isinstance(args, list):
        string += ', '.join(x.value() for x in args)
    string += f'):{NEWLINE}'
    if docstring:
        # TODO would split_string be good here?
        string += f'"""{docstring}"""\n'
    if logic:
        if isinstance(logic, str):
            string += f'{INDENT}{logic}'
        elif isinstance(logic, list):
            string += '\n'.join(INDENT + x for x in logic)
