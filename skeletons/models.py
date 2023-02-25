"""Pydantic models for skeletons."""
from os import getenv
from io import BytesIO, StringIO
from typing import Union, Optional, Literal
from pathlib import Path
from pkg_resources import resource_filename

from pydantic import BaseModel, validator
from jinja2 import Template

from skeletons.settings import enc


class CLXN(BaseModel):
    name: str
    lang: Union[str, list]
    description: Optional[str] = None
    ext: Union[list, str]
    tag: Union[list, str]

    @validator('ext', 'lang', 'tag')
    def _ext_validator(cls, ext: Union[list, str]) -> list:
        """Always store ext attribute as list."""
        if isinstance(ext, str):
            return [ext]
        return ext


class FileModel(BaseModel):
    name: Optional[str] = None
    path: Union[Path, str]
    use_bytes: bool = False
    encoding: str = enc.get('encoding', 'utf-8').lower()

    @validator('path')
    def _path_validator(cls, path: Union[Path, str]) -> Path:
        """Ensure path is a Path object."""
        if isinstance(path, str):
            if path.startswith('~'):
                path = path.replace('~', getenv('HOME', '.'))
            path = Path(path)
        return path

    def contents(
            self, 
            do: Literal['get', 'write', 'append'] = 'get',
            data: Optional[Union[str, bytes, BytesIO, StringIO]] = None,
    ) -> Optional[Union[str, bytes]]:
        """Perform action on contents.
        Args:
            action: one of 'get', 'write', 'append' 
        """
        if do[1] == 'g' or do == 'get':
            if self.use_bytes:
                return self.path.read_bytes(encoding=self.encoding)
            return self.path.read_text(encoding=self.encoding)
        if isinstance(data, (StringIO, BytesIO)):
            data = data.getvalue()
        if do[1] == 'w' or do == 'write':
            if self.use_bytes:
                self.path.write_bytes(data)
            else:
                self.path.write_text(data, encoding=self.encoding)
            return None
        if do[1] == 'a' or do == 'append':
            contents = self.contents(do='get')
            data = contents + '\n' + data
            self.path.write_text(data, encoding=self.encoding)
            return None
        return None


class ResourceModel(BaseModel):
    name: str
    resource: Union[str, Path]

    @validator('resource')
    def _resource_validator(
            cls, resource: Union[str, Path]
    ) -> Path:
        """Ensure a Path to resource is available."""
        if isinstance(resource, Path):
            return resource
        if isinstance(resource, str):
            if not resource.endswith('.j2'):
                resource += '.j2'
            if not resource.startswith('templates/'):
                resource = 'templates/' + resource
            try:
                resource = Path(resource_filename('skeletons', resource))
                if resource.is_file():
                    return resource
                raise ValueError(
                        f'{resource} could not be identified as an ' +
                        'existing file'
                )
            except ModuleNotFoundError as uhoh:
                print('Wow, this is truly an incredible moment.')
                raise uhoh
        return Path(resource)

    def parse(self, **kwargs):
        """Parse the resource with jinja2.
        Args:
            kwargs: passed to jinja2.Template.render()
        """
        template = Template(self.resource.read_text(**enc))
        return template.render(**kwargs)


class TemplateModel(BaseModel):
    name: str
    dest: Union[str, FileModel]
    resource: Optional[Union[str, ResourceModel]] = None

    @validator('dest')
    def _dest_validator(
            cls, dest: Union[str, FileModel], **kwargs
    ) -> FileModel:
        """Make sure dest is FileModel.
        files.
        """
        if isisntance(dest, str):
            return FileModel(path=dest, **kwargs)
        return dest

