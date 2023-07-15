from django.contrib.auth import get_user_model
from django.db import models

from exam_web_project.courses.models import Course

UserModel = get_user_model()


class UserCourseEnroll(models.Model):
    user = models.ForeignKey(
        UserModel,
        null=False,
        on_delete=models.CASCADE,
    )

    course = models.ForeignKey(
        Course,
        null=False,
        on_delete=models.CASCADE,
    )

    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.name}"


class Payment(models.Model):
    order_id = models.CharField(
        max_length=250,
        null=False
    )
    user = models.CharField(
        max_length=50,
        null=False
    )

    user_course = models.ForeignKey(
        UserCourseEnroll,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    created_on = models.DateTimeField(auto_now_add=True)

    status = models.BooleanField(default=False)


