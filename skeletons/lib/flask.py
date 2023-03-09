"""Strings for creating a basic flask app."""

from skeletons.lib.python import (
    make_import_statement,
)


_FLASK_IMPORTS = [
    ['logging', ],
    ['logging.config', ],
    ['datetime', 'datetime', 'dt'],
    ['requests', ],
    ['flask', ['Flask', 'jsonify', 'abort', 'make_response', 'request'], ],
    ['werkzeug.utils', 'secure_filename'],
]
FLASK_IMPORTS = '\n'.join(
        [make_import_statement(*flask_import) for flask_import
         in _FLASK_IMPORTS])
