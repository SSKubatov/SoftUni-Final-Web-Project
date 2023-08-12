from django.contrib import admin

from core.utils.payments_utils import get_discounted_price_rounded_to_thousands
from exam_web_project.courses.models import Course, Lesson, Video, Resource, FileProperty, URLProperty


class LessonAdmin(admin.TabularInline):
    model = Lesson


class VideoAdmin(admin.StackedInline):
    model = Video


class FileAdmin(admin.TabularInline):
    model = FileProperty
    verbose_name_plural = 'Files'


class URLAdmin(admin.TabularInline):
    model = URLProperty
    verbose_name_plural = 'URLs'


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = (LessonAdmin, VideoAdmin, FileAdmin, URLAdmin)
    list_display = ('name', 'normal_price', 'discount_price', 'price_after_discount')
    list_filter = ('name',)
    ordering = ['created_at']
    prepopulated_fields = {'slug': ('name',)}

    def discount_price(self, course):
        return f'{course.discount}%'

    def normal_price(self, course):
        return f'{course.price} лв.'

    def price_after_discount(self, course):
        return f'{get_discounted_price_rounded_to_thousands(course.price, course.discount) / 100} лв.'


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    ordering = ('id',)
    list_display = ('serial_number', 'course', 'title')
    list_filter = ('course',)


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('display_resource', 'file_property', 'url_property')
    fields = ('video', 'file_property', 'url_property')

    def display_video(self, obj):
        return obj.video.title

    def display_resource(self, obj):
        return str(obj)

    display_video.short_description = 'Video'
