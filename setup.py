#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create template-able projects quickly."""
from os import access, X_OK
from pathlib import Path
from re import sub as resub
from sys import modules

from setuptools import setup, find_packages


_HERE = Path(__file__).resolve().parent
_ek = {'encoding': 'utf-8'}
_url = f'https://github.com/sempervent/{_HERE.name}.git'
# include all executable files in scripts directory
_scripts = [str(f) for f in (_HERE / 'bin').rglob('*')
            if access(f, X_OK) and f.is_file()]


def _strip(file_name: str):
    """Strip text from a file."""
    return (_HERE / file_name).read_text(**_ek).strip()


_package_data = {
    _HERE.name: [
        'templates/*.j2',
    ],
}

_SETUP = {
    'name': _HERE.name,
    'version': _strip('VERSION'),
    'description': resub(r'\s+', ' ', modules[__name__].__doc__),
    'long_description': _strip('README.md'),
    'long_description_content_type': 'text/markdown',
    'url': _url,
    'author': 'Joshua N. Grant',
    'author_email': 'jngrant@live.com',
    'packages': find_packages(include=['skeletons'], 
                              exclude=['tests', 'scripts']),
    'classifiers': [
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Programming Lagunage :: Python 3.7",
        "Programming Lagunage :: Python 3.8",
        "Programming Lagunage :: Python 3.9",
        "Programming Lagunage :: Python 3.10",
        "Programming Lagunage :: Python 3.11",
    ],
    'install_requires': _strip('requirements.txt').split(),
    'package_data': _package_data,
    'scripts': _scripts,
    'extras_require': {
        'dev': _strip('requirements-dev.txt').split(),
    },
}

setup(**_SETUP)
