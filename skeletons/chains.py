"""Chains are special classes that will "chain" together commands."""
from typing import Union, List, Optional
from warnings import warn


class Chain:
    """A chain is a serious of strings in a list append with tags.
    """
    
    def __init__(
        self,
        cmds: List[str],
        tags: Optional[Union[List[str], str]] = None,
        chain_string: str = "&&",
    ):
        """Initialize a Chain object.
        Args:
            cmds: a list of commands to chain
            tags: a str or list of strs to apply after each cmd
            chain_string: a str denoting how to separate cmds
        """
        if isinstance(cmds, list) and isinstance(tags, list):
            if len(cmds) != len(tags):
                warn("Lengths of cmds do not match tags.")
        self.cmds = cmds
        self.tags = tags
        self.chain_string = chain_string
        self.string = ""

    def chain(self):
        """Chain the commands together and return the string."""
        output = []
        if isinstance(self.tags, list):
            for cmd, tag in zip(self.cmds, self.tags):
                cmd += " " + tag
                output.append(cmd)
        else:
            for cmd in self.cmds:
                if isinstance(self.tags, str):
                    cmd += " " + self.tags
                output.append(cmd)
        return f" {self.chain_string} ".join(output)
