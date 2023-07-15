from enum import Enum

from exam_web_project.core.mixins.custom_mixins import ChoicesEnumMixin


class Gender(ChoicesEnumMixin, Enum):
    male = 'Male'
    female = 'Female'
    DoNotShow = 'Do not show'
