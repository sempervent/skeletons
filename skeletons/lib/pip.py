
"""Pip instructions."""
from typing import Union, List, Optional

PIP_TAGS = "--no-cache-dir"
PIP_UPDATE = "pip update"
PIP_UPGRADE = "pip upgrade"
PIP_INSTALL = "pip install"
PIP_INSTRUCTIONS = [
    PIP_UPDATE, PIP_UPGRADE, PIP_INSTALL,
]


def generate_pip_install(
    pkgs: Union[str, List[str]],
    tags: Optional[Union[list, str]] = None,
    upgrade: Optional[Union[bool, List[str], str]] = None,
) -> str:
    """Generate a pip install instruction."""
    if tags is None:
        tags = PIP_TAGS
    if isinstance(tags, list):
        tags = " ".join(tags)
    if upgrade:
        if isinstance(upgrade, bool) and upgrade is True:
            cmd = " ".join([])
    cmds = []
    for cmd in PIP_INSTRUCTIONS:
        if not upgrade and cmd == PIP_UPGRADE:
            continue
        if isinstance(tags, list):
        cmd += f" {tags}"
