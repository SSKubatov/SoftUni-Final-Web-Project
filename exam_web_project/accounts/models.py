from django.contrib.auth import models as auth_models
from django.core import validators

from django.db import models

from exam_web_project.accounts.mixins import Gender
from core.custom_validators.validators import validate_letters_only, validate_email, validate_image_max_size


class AppUser(auth_models.AbstractUser):
    FIRST_NAME_MAX_LENGTH = 30
    FIRST_NAME_MIN_LENGTH = 2
    LAST_NAME_MAX_LENGTH = 30
    LAST_NAME_MIN_LENGTH = 2

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(
            validators.MinLengthValidator(FIRST_NAME_MIN_LENGTH),
            validate_letters_only,
        )
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        validators=(
            validators.MinLengthValidator(LAST_NAME_MIN_LENGTH),
            validate_letters_only,
        )
    )

    email = models.EmailField(
        unique=False,
        validators=(
            validate_email,
        )

    )

    gender = models.CharField(
        choices=Gender.choices(),
        max_length=Gender.max_length(),
        default=Gender.DO_NOT_SHOW.value
    )

    profile_picture = models.ImageField(
        upload_to='files/user_images',
        null=True,
        blank=True,
        validators=(
            validate_image_max_size,
        )
    )
