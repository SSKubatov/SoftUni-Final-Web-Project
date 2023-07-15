from django.contrib import admin

from exam_web_project.payments.models import UserCourseEnroll, Payment


# Register your models here.
@admin.register(UserCourseEnroll)
class AdminUserCourseEnroll(admin.ModelAdmin):
    pass


@admin.register(Payment)
class AdminPayment(admin.ModelAdmin):
    list_display = ('order_id', 'get_user', 'user_course', 'status')
    list_filter = ('user_course__course',)

    def get_user(self, payment):
        return f'{payment.user_course.user}'
