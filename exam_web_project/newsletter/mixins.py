from enum import Enum

from exam_web_project.core.mixins.custom_mixins import ChoicesEnumMixin


class EmailStatus(ChoicesEnumMixin, Enum):
    PUBLISH = "Publish"
    DRAFT = 'Draft'
