"""Provide settings for the skeletons project."""
from os import getenv

enc = {"encoding": "UTF-8"}
RAW_GH_URL = "https://raw.githubusercontent.com/"
GH_URL = "https://github.com/"
INDENT = getenv('SKELETONS_INDENT', '\t')
NEWLINE = getenv('SKELETONS_NEWLINE', '\n')
CURLY_OPEN = "{"
CURLY_CLOSE = "}"
