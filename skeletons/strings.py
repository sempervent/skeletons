#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Allow imports from this directory."""
from string import Formatter
from typing import Callable
from inspect import getfullargspec


class FString:
    """A class for formatting an Fstr."""

    def __init__(self, *args, fstr: str, **kwargs):
        """Expects an fstr: str, and either args or kwargs."""
        self.fstr = fstr
        if kwargs and args:
            raise ValueError('both *args and **kwargs specified')
        if args:
            self.fmt = self._assign_args_to_fmt(*args) 
        elif kwargs:
            self.fmt = kwargs
        else:
            self.fmt = None
        print(self.fmt)

    def _assign_args_to_fmt(self, *args) -> dict:
        # pylint: disable=invalid-name
        sf = Formatter()
        keys = [x[1] for x in list(sf.parse(self.fstr))]
        # pylint: enable=invalid-name
        return dict(zip(keys, args))

    def __repr__(self):
        return self.fstr.format(**self.fmt)

    def __str__(self):
        return self.fstr.format(**self.fmt)

    def render(self, *args, **kwargs) -> str:
        if kwargs and args:
            raise ValueError('both *args and **kwargs specified')
        if args:
            self.fmt = self._assign_args_to_fmt(*args)
        if kwargs:
            self.fmt = kwargs
        return self.fstr.format(**self.fmt)


class LString:
    """Assign a string from a lambda expression."""

    def __init__(self, *args, exp: Callable, **kwargs):
        if not callable(exp):
            raise TypeError('exp argument should be Callable')
        self.exp = exp
        if kwargs and args:
            raise ValueError('both *args and **kwargs specified')
        if args:
            self.fmt = self._assign_args_to_fmt(*args)
        elif kwargs:
            self.fmt = kwargs
        else:
            self.fmt = None

    def _assign_args_to_fmt(self, *args) -> dict:
        keys = getfullargspec(self.exp).args
        if len(keys) != len(args):
            raise ValueError(
                f'length of keys and args did not match: {keys=}, {args=}.')
        return dict(zip(keys, args))

    def __repr__(self):
        return self.exp(**self.fmt)

    def __str__(self):
        return self.exp(**self.fmt)

    def render(self, *args, **kwargs):
        if kwargs and args:
            raise ValueError('both *args and **kwargs specified')
        if args:
            self.fmt = self._assign_args_to_fmt(*args)
        if kwargs:
            self.fmt = kwargs
        return self.exp(**self.fmt)

