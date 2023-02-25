"""Gitignore generation for projects."""
from typing import Union
from pathlib import Path

import requests

from skeletons.settings import enc, RAW_GH_URL


_url = RAW_GH_URL + "github/gitignore/main/{lang}.gitignore"


def _call_gitignore(lang: Union[str, list]) -> str:
    """Call the gitignore repo for the specified language.
    Args:
        lang: str or list of languages to git ignore
    Returns:
        a str of gitignores
    """
    gitignore = ""
    if isinstance(lang, list):
        for l in lang:
            try:
                gitignore += f"# {l} gitignore\n"
                gitignore += _call_gitignore(lang=l)
            except Exception as excp:
                print(f'error processing: {l}, skipped.')
                print(f'{str(excp)}')
                gitignore += f"# {l} raised {excp}\n"
    response = requests.get(
        url=_url.format(lang=lang.capitalize()),
        timeout=60,
    )
    if response.status == 200:
        return response.text + "\n"
    return ""


def write_gitignore(lang: Union[str, list]):
    """Write a gitignore in the current directory."""
    gitignore = _call_gitignore(lang=lang)
    Path('.gitignore').write_text(gitignore, **enc)
