"""Docker based examples."""
from typing import Optional, Callable, Union
from string import Formatter
from inspect import getfullargspec

_LAYER_ORDER = ['from', 'from_as', 'env', 'arg', 'arg_default', 'workdir', 
                'copy',  'apt', 'pip', 'pip_reqs', 'pipenv', 'run', 'expose', 
                'entrypoint',
                'cmd']


class Layer:
    """A class for defining a layer."""

    def __init__(self, *args, fstr: Union[str, Callable], **kwargs):
        self.fstr = fstr
        self.string = None
        self.fmt = None
        if args:
            self._assign_args_to_fmt(*args)
        elif kwargs:
            self.fmt = kwargs
        if self.fmt and isinstance(self.fstr, str):
            self.string = self.fstr.format(**self.fmt)
        elif self.fmt and callable(self.fstr):
            self.string = self.fstr(**self.fmt)

    def _assign_args_to_fmt(self, *args):
        if args and isinstance(self.fstr, str):
            sf = Formatter()
            sf.parse(self.fstr)
            keys = [x[1] for x in list(sf.parse(self.fstr))]
            self.fmt = dict(zip(keys, args))
        if args and callable(self.fstr):
            fargs = getfullargspec(self.fstr).args
            self.fmt = dict(zip(fargs, args))

    def __repr__(self):
        if self.string:
            return self.string
        return self.fstr(**self.fmt)

    def __str__(self):
        if self.string:
            return self.string
        return self.fstr(**self.fmt)

    def build(self, *args, **kwargs) -> Optional[str]:
        if args:
            self._assign_args_to_fmt(*args)
        if kwargs:
            self.fmt == kwargs
        if isinstance(self.fmt, dict):
            if isinstance(self.fstr, str):
                return self.fstr.format(**self.fmt)
            if callable(self.fstr):
                return self.fstr(**self.fmt)
        return None


_def_to = '.'
_def_from = '.'
_reqsfile = 'requirements.txt'

_LAYER_FSTRINGS = {
    'run': 'RUN {cmd}\n',
    'from': 'FROM {image}\n',
    'from_as': 'FROM {image} AS {name}\n',
    'env': 'ENV {key}={value}\n',
    'arg': 'ARG {arg}\n',
    'arg_default': 'ARG {arg}={default}\n',
    'workdir': 'WORKDIR {workdir}\n',
    'copy': 'COPY {_from or _def_from} {to or def_to}\n',
    'apt': '''RUN apt-update -yqq && apt-upgrade -yqq && \\
\tapt-get-install -yqq {pkgs} && \\
\tapt-get-clean -yqq
''',
    'pip': '''RUN pip update --no-cache-dir && \\
\tpip install --no-cache-dir install {pkgs}
''',
    'pip_reqs': '''RUN pip update --no-cache-dir && \\
\tpip install -r {reqsfile or _reqsfile}
''',
    'pipenv': 'RUN pipenv install --system --deploy\n',
    'expose': 'EXPOSE {port}\n',
    'entrypoint': 'ENTRYPOINT {entrypoint}\n',
    'cmd': 'CMD {cmd}\n'
}

_LAYER_INSTRUCTIONS = {
        'from': lambda image: f'FROM {image}\n',
        'from_as': lambda image, name: f'FROM {image} AS {name}\n',
        'env': lambda key, value: 'ENV {key}={value}\n',
        'arg': lambda arg: 'ARG {arg}\n',
        'arg_default': lambda arg, default: 'ARG {arg}={default}\n',
        'workdir': lambda wdir: f'WORKDIR {wdir}\n',
        'copy': lambda _from, to: f'COPY {_from or _def_from} {to or _def_to}\n',
        'apt': lambda pkgs: f''''RUN apt-update -yqq && apt-upgrade -yqq && \\
\tapt-get install -yqq {pkgs} && \\
\tapt-get clean -yqq\n''',
        'pip': lambda pkgs: f'''RUN pip update --no-cache-dir && \\
\tpip install --no-cache-dir install {pkgs}''',
        'pip_reqs': lambda reqsfile: f'''RUN pip update --no-cache-dir && \\
\tpip install -r {reqsfile or _reqsfile}
''',
    'pipenv': 'RUN pipenv install --system --deploy\n',
        'run': lambda cmd: f'RUN {cmd}\n',
    'expose': lambda port: f'EXPOSE {port}\n',
    'entrypoint': lambda entrypoint: f'ENTRYPOINT {entrypoint}\n',
    'cmd': lambda cmd: f'CMD {cmd}\n',
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
        self.file = ""
        self.image = image
        if kwargs:
            intersection = \
                set(kwargs.keys()).intersection(LAYERS.keys())
            if intersection:
                for value in intersection:
                    l = LAYERS[value].build(**{value: kwargs.pop(value)})
                    print(value)
                    print(l)
                    self.file += l

    def build(self, **kwargs):
        """Build a dockerfile from self or kwargs."""
        if kwargs:
            intersection = \
                set(kwargs.keys()).intersection(LAYERS.keys())
            if intersection:
                for value in intersection:
                    setattr(self, value, 
                            LAYERS[value].build(**{value: kwargs.pop(value)}))
        file = ""
        for layer in LAYERS:
            if hasattr(self, layer):
                file = getattr(self, layer).build()
        return file

    def add(self, *args, **kwargs):
        """Add an entry to the file object."""
        for arg, key, item in zip(args, kwargs.items()):
            if arg == key and isinstance(item, dict):
                self.file += LAYERS[arg](**item)

    def construct(self, *args, replace: bool = False, **kwargs) -> str:
        """Construct the header of the Dockerfile."""
        if replace:
            self.file = ""
        if hasattr(self, 'from_as'):
            self.file += getattr(self, 'from_as')
        elif hasattr(self, 'from'):
            self.file += getattr(self, 'from')
        else:
            self.file += self.add(*args, **kwargs)
        return self.file + '\n'
