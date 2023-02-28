"""Docker based examples."""

_LAYER_ORDER = ['from', 'from_as', 'env', 'arg', 'arg_default', 'apt', 'pip', 
               'pipenv', 'run', 'expose', 'entrypoint', 'cmd']


class Layer:
    """A class for defining a layer."""
    
    def __init__(self, *args, fstr: str, **kwargs):
        self.fstr = fstr
        self.string = None
        if args or kwargs:
            self.string = fstr.format(*args, **kwargs)

    def __repr__(self):
        if self.string:
            return self.string
        return self.fstr

    def __str__(self):
        if self.string:
            return self.string
        return self.fstr

    def build(self, *args, **kwargs):
        return self.fstr.format(*args, **kwargs)



_LAYER_INSTRUCTIONS = {
    'run': 'RUN {cmd}\n',
    'from': 'FROM {image}\n',
    'from_as': 'FROM {image} AS {name}\n',
    'env': 'ENV {key}={value}\n',
    'arg': 'ARG {arg}\n',
    'arg_default': 'ARG {arg}={default}\n',
    'apt': 'RUN apt-update -yqq && apt-upgrade -yqq && \\\n'
        '\tapt-get install {pkgs} -yqq && \\\n'
        '\tapt-get clean -yqq\n',
    'pip': 'RUN pip update --no-cache-dir  && \\\n'
        '\tpip install --no-cache-dir install {pkgs}\n',
    'pipenv': 'RUN pipenv install --system --deploy\n',
    'expose': 'EXPOSE {port}\n',
    'entrypoint': 'ENTRYPOINT {entrypoint}\n',
    'cmd': 'CMD {cmd}\n',
}
LAYER_INSTRUCTIONS = dict(
        sorted(
            _LAYER_INSTRUCTIONS.items(),
            key=lambda x: _LAYER_ORDER.index(x[0])
            )
        )

LAYERS = {}
for layer, instruction in _LAYER_INSTRUCTIONS.items():
    LAYERS[layer] = Layer(fstr=instruction)



class Dockerfile:
    """Make a Dockerfile from a j2 Dockerfile."""

    def __init__(self, image: str, **kwargs):
        """Initialize a dockerfile with a set of instructions."""
        if kwargs:
            intersection = \
                set(kwargs.keys()).intersection(LAYERS.keys())
            if interesction:
                for key, value in interesction.items():
                    setattr(self, key, LAYERS[key].format(**value))
        self.image = image

    def build(self, **kwargs):
        """Build a dockerfile from self or kwargs."""
        if kwargs:
            intersection = \
                set(kwargs.keys()).intersection(LAYERS.keys())
            if intersection:
                for key, value in interesection.items():
                    setattr(self, key, LAYERS[key].build(**value))
        file = ""
        for layer in LAYERS:
            if hasattr(self, layer):
                file = getattr(self, layer).build()
        return file
