"""Write in python."""
from typing import Optional, Union, List


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


