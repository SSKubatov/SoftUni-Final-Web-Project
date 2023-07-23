from enum import Enum

from core.mixins.custom_mixins import ChoicesEnumMixin


class EmailStatus(ChoicesEnumMixin, Enum):
    PUBLISH = "Publish"
    DRAFT = 'Draft'
