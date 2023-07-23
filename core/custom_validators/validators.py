import re

from django.core.exceptions import ValidationError

from core.utils.common_utils import convert_to_megabytes


def validate_username(value):
    pattern = r'^[A-Za-z][A-Za-z0-9_]{4,15}$'
    if not re.match(pattern, value):
        raise ValidationError(
            "Username must start with a letter and can contain only letters, numbers, and underscores."
            " It should be between 5 and 15 characters long."
        )


def validate_email(value):
    if not re.match(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", value):
        raise ValidationError("Please enter a valid email address.")


def validate_letters_only(value):
    if not value.isalpha():
        raise ValidationError("Only letters are allowed.")


def validate_image_max_size(value):
    file_size = value.file.size
    mb_limit = 5.00
    if file_size > convert_to_megabytes(mb_limit):
        raise ValidationError(f'Max file size is {mb_limit}sMB.')
