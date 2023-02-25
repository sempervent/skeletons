"""Pydantic models for skeletons."""
from os import getenv
from io import BytesIO, StringIO
from typing import Union, Optional, Literal
from pathlib import Path

from pydantic import BaseModel, validator

from skeletons.settings import enc


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

