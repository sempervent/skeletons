"""Utility functions."""
from os import getenv
from typing import Optional

BOOLS = {
    'false': ['0', 'false', 'f'],
    'true': ['1', 'true', 't'],
}


def boolify(var: str) -> bool:
    """Convert a possible value to True or False."""
    if var.lower() in BOOLS['false']:
        return False
    if var.lower() in BOOLS['true']:
        return True
    exc_msg = f'{var} was not found in any "True" values '
    exc_msg += f'{", ".join(BOOLS["false"])} or '
    exc_msg += f'"False" values {", ".join(BOOLS["false"])}'
    raise ValueError(exc_msg)


def check_environment(
    envar: str,
    default: Optional[str] = None,
    raise_on_missing: bool = False,
    check_globals: bool = True,
) -> str:
    """Check if an envar exists and optionally raise an error."""
    value = getenv(key=envar, default=default)
    if value is None and check_globals is True:
        if envar in globals():
            return globals()[envar]
    if value is None and raise_on_missing is True:
        raise ValueError(f'{envar} is not in environment!')
    if isinstance(default, bool):
        return boolify(var=envar)
    return value
