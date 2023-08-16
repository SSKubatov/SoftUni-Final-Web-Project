from django.contrib.auth import get_user_model

from django.core import validators
from django.db import models

UserModel = get_user_model()


# Create your models here.
class Course(models.Model):
    NAME_MAX_LEN = 40
    NAME_MIN_LEN = 2

    PRICE_MIN = 1
    PRICE_MAX = 100

    SLUG_MAX_LEN = 40
    SLUG_MIN_LEN = 2

    name = models.CharField(
        max_length=NAME_MAX_LEN,
        validators=(
            validators.MinLengthValidator(NAME_MIN_LEN),
        )
    )

    slug = models.CharField(
        max_length=SLUG_MAX_LEN,
        validators=(
            validators.MinLengthValidator(SLUG_MIN_LEN),
        ),
        unique=True,
    )

    price = models.FloatField(
        validators=(
            validators.MaxValueValidator(PRICE_MAX),
            validators.MinValueValidator(PRICE_MIN),
        )
    )

    discount = models.IntegerField(null=True)

    description = models.TextField()

    thumbnail = models.ImageField(
        upload_to="files/thumbnails",
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def price_in_leva(self):
        return f"{self.price:.2f} лв."

    def __str__(self):
        return self.name


class CourseProperty(models.Model):
    class Meta:
        abstract = True

    TITLE_MAX_LEN = 50
    TITLE_MIN_LEN = 4

    title = models.CharField(
        max_length=TITLE_MAX_LEN,
        validators=(
            validators.MinLengthValidator(TITLE_MIN_LEN),
        ),
        null=False,
        blank=False,
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        null=False,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"


class Lesson(CourseProperty):
    CONTENT_MAX_LEN = 100

    content = models.CharField(
        max_length=CONTENT_MAX_LEN,

    )


class Video(CourseProperty):
    VIDEO_ID_MAX_LEN = 50

    serial_number = models.IntegerField(
        null=False,
        blank=False,
    )

    video_id = models.CharField(
        max_length=VIDEO_ID_MAX_LEN,
        null=False,
    )

    is_preview = models.BooleanField(default=False)


class FileProperty(CourseProperty):
    file = models.FileField(
        upload_to="files/resources",
        null=False,
        blank=False,
    )


class URLProperty(CourseProperty):
    url_link = models.URLField(
        blank=False,
    )


class Resource(models.Model):
    video = models.OneToOneField(
        Video,
        on_delete=models.CASCADE,
        related_name='resources',
    )

    file_property = models.OneToOneField(
        FileProperty,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    url_property = models.OneToOneField(
        URLProperty,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Resource for {self.video.title}"
