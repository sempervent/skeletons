"""Define pre-built projects."""
from typing import Union, Optional, List

from pydantic import BaseModel, validator

from skeletons.gitignore import write_gitignore
from skeletons.validation import ensure_list
from skeletons.models import (
    FileModel, ResourceModel, TemplateModel
)


class Project(BaseModel):
    """A project ties skeletons together for a coheisve narrative."""
    name: str
    files: Optional[Union[FileModel, List[FileModel]]] = None
    templates: Optional[Union[TemplateModel, List[TemplateModel]]] = None
    resources: Optional[Union[ResourceModel, List[ResourceModel]]] = None
    langs: Optional[List[str]] = None

    @validator('files')
    def _files_validator(
        cls,
        files: Optional[Union[FileModel, List[FileModel]]],
    ) -> List[FileModel]:
        """Always return a list of FileModels or an empty list."""
        return ensure_list(obj=files, typ=FileModel)

    @validator('templates')
    def _templates_validator(
        cls,
        templates: Optional[Union[TemplateModel, List[TemplateModel]]],
    ) -> List[TemplateModel]:
        """Always return a list of TemplateModels or an empty list."""
        return ensure_list(obj=templates, typ=FileModel)

    @validator('resources')
    def _resources_validator(
        cls,
        resources: Optional[Union[ResourceModel, List[ResourceModel]]],
    ) -> List[ResourceModel]:
        return ensure_list(obj=resources, typ=ResourceModel)

    def create(self):
        """Create a Project."""
        languages = []
        for file, template, resource in zip(
                self.files, self.templates, self.resources):
            languages.append(file.lang())
            render = resource.parse(**template.render_args)
            file.contents(do='write', data=render)
        write_gitignore(lang=languages)

    def lang(self) -> list:
        """Get the languages used."""
        if self.langs:
            return self.langs if isinstance(self.langs, list) else [self.langs]

