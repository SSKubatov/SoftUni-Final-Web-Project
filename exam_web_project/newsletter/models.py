from django.core import validators
from django.db import models

from exam_web_project.core.mixins.custom_mixins import TimestampMixin
from exam_web_project.newsletter.mixins import EmailStatus


# Create your models here.
class NewsletterUser(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Newsletter(TimestampMixin, models.Model):
    SUBJECT_MAX_LEN = 255
    SUBJECT_MIN_LEN = 5

    subject = models.CharField(
        max_length=SUBJECT_MAX_LEN,
        validators=[validators.MinLengthValidator(SUBJECT_MIN_LEN)]
    )

    message = models.TextField()

    email = models.ManyToManyField(
        NewsletterUser,
    )

    status = models.CharField(
        max_length=EmailStatus.max_len(),
        choices=EmailStatus.choices(),
    )

    def __str__(self):
        return self.subject
