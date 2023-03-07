"""Apt-get instructions."""
from typing import Optional, Union, List

APT_TAGS = '-yqq'
APT_UPDATE = 'apt-get update'
APT_UPGRADE = 'apt-get upgrade'
APT_INSTALL = 'apt-get install'
APT_CLEAN = 'apt-get clean'
APT_INSTRUCTIONS = [
    APT_UPDATE, APT_UPGRADE, APT_INSTALL, APT_CLEAN,
]


def generate_apt_installation(
    pkgs: Union[str, List[str]],
    tags: Optional[Union[list, str]],
    upgrade: bool = True,
):
    """Generate APT installation commands."""
    if tags is None:
        tags = APT_TAGS
    if isinstance(tags, list):
        tags = " ".join(tags)
    cmds = []
    for cmd in APT_INSTRUCTIONS:
        if not upgrade and cmd == APT_UPGRADE:
            continue
        cmd += f" {tags}"
        if cmd.startswith(APT_INSTALL):
            if isinstance(pkgs, str):
                cmd += " " + pkgs
            elif isinstance(pkgs, list):
                cmd += " " + " ".join(pkgs)
        cmds.append(cmd)
