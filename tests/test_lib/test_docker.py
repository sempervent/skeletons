"""Test docker file creation."""
import pytest

from skeletons.lib.docker import Dockerfile, LAYERS


TEXLIVE_DEBIAN = """FROM debian:latest
RUN apt-get update -yqq && apt-upgrade -yqq && \\
\tapt-get install -yqq texlive-full poppler && \\
\tapt-get clean -yqq
"""
FLASK_APP = """FROM python:3.11-slim
WORDKIR /app
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
RUN pip update --no-cache-dir && \\\n
\tpip install --no-cache-dir install flask sqlalchemy
COPY . .
EXPOSE 8000
CMD ["flask", "run", "--config=config.py"]
"""
PYTEST_PKG = """FROM python:3.8 AS base
WORKDIR /app
COPY . .
RUN pip update --no-cache-dir && \\\n
\tpip install --no-cache-dir pipenv
RUN pipenv install --dev --system --deploy

FROM base AS linter
RUN flake8 .
RUN pylint --html-cov $(pwd)
WORKDIR /app/htmlcov/
EXPOSE 8888
CMD ["python3", "-m", "http.server"]

FROM base AS tester
CMD ["pytest", "tests/"]
"""
ISO_FROM_DIR = """FROM debian:latest
WORKDIR /isodir
RUN apt-get update -yqq && apt-get upgrade && \\
\tapt-get install -yqq cdrkit tar
CMD ["genisoimage", "-o", "file.iso", "-V", "my iso file",
     "-R", "-J", "./file"]
"""


# pylint: disable=invalid-name
def test_Dockerfile():
    """Test the Dockerfile class creates expected dockerfiles."""
    # pylint: enable=invalid-name
    texlive_debian = Dockerfile(
        image='debian:latest',
        apt={'pkgs': 'texlive-full poppler'},
    )
    assert texlive_debian.file == TEXLIVE_DEBIAN
    flask_app = Dockerfile(
        image="python:3.11-slim",
        workdir='/app',
        copy=True,
        pip='flask sqlachemy',
        expose="8000",
        cmd='"flask", "run", "--config=config.py"',
    )
    flask_app.add(env=('FLASK_APP', 'app.py'))
    flask_app.add(env=('FLASK_ENV', 'development'))
    assert flask_app.build() == FLASK_APP
