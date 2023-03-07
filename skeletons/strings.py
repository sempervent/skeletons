#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Allow imports from this directory."""
from string import Formatter
from typing import Callable
from inspect import getfullargspec


def split_line(
    txt: str, nchar: int = 79, flag: str = "&&", newline: str = "\n",
    indent: str = "\t",
):
    """Split a line at over 79 characters, but only after following an &&, but
    escape the newline character."""
    parts = txt.split(flag)
    output = []
    current_line = ""
    for part in parts:
        words = part.strip().split()
        if not words:
            continue
        if len(current_line) + len(words[0]) + 4 <= nchar:
            current_line += " ".join([words[0], flag, '/'])
            words = words[1:]
        for word in words:
            if len(current_line) + len(word) + 1 <= nchar:
                current_line += word + " "
            else:
                output.append(" ".join([current_line[:-1], flag, '\\']))
                current_line = f"{indent}{word} "
        current_line = " ".join([indent, current_line[:-1], flag, '\\'])
    if current_line:
        output.append(current_line[:-4])
    return newline.join(output)


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
        """Render the string itself."""
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
        """Render the string."""
        if kwargs and args:
            raise ValueError('both *args and **kwargs specified')
        if args:
            self.fmt = self._assign_args_to_fmt(*args)
        if kwargs:
            self.fmt = kwargs
        return self.exp(**self.fmt)
