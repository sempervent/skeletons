"""Docker based examples."""


LAYER_INSTRUCTIONS = {
    'run': 'RUN {cmd}',
    'from': 'FROM {image}',
    'from_as': 'FROM {image} AS {name}',
    'env': 'ENV {key}={value}',
    'arg': 'ARG {arg}',
    'arg_default': 'ARG {arg}={default}',
}



class Dockerfile:
    """Make a Dockerfile from a j2 Dockerfile."""

    def __init__(self, image: str, instructions: str):
        """"""
