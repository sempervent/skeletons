"""Provide validation and type ensurance."""
from typing import Union, Any


def ValidationError(Exception):
    """Raise an error because a validation cannot be done."""


def ensure_list(
        obj: Any, typ: Any, raises: bool = False, warns: bool = False,
) -> list:
    """Ensure that obj is a list of typ objects."""
    if isinstance(obj, typ):
        return [obj]
    if isinstance(obj, list):
        if all([isinstance(o, typ) for o in obj]:
               return obj
        problem = f'Expected {typ} in all {obj}.' 
        if warns:
           from warnings import warn
           warn(problem)
        if raises:
           raise ValidationError(problem)
    return []
