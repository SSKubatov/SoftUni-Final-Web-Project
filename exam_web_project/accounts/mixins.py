from enum import Enum

from core.mixins.custom_mixins import ChoicesEnumMixin


class Gender(ChoicesEnumMixin, Enum):
    MALE = 'Male'
    FEMALE = 'Female'
    DO_NOT_SHOW = 'Do Not Show'
