from django.contrib import admin

from core.utils.payments_utils import get_discounted_price
from exam_web_project.courses.models import Course, Lesson, Video, Resource, FileProperty, URLProperty


class LessonAdmin(admin.TabularInline):
    model = Lesson


class VideoAdmin(admin.StackedInline):
    model = Video


class ResourceAdmin(admin.TabularInline):
    model = Resource


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = (LessonAdmin, VideoAdmin)
    list_display = ('name', 'normal_price', 'discount_price', 'price_after_discount')
    list_filter = ('name',)
    ordering = ['created_at']
    prepopulated_fields = {'slug': ('name',)}

    @staticmethod
    def discount_price(course):
        return f'{course.discount}%'

    @staticmethod
    def normal_price(course):
        return f'{course.price} лв.'

    @staticmethod
    def price_after_discount(course):
        return f'{get_discounted_price(course.price, course.discount)} лв.'


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    inlines = (ResourceAdmin,)
    ordering = ('id',)
    list_display = ('title', 'course', 'serial_number')
    list_filter = ('course',)


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('display_resource', 'file_property', 'url_property')
    fields = ('video', 'file_property', 'url_property')

    @staticmethod
    def display_resource(obj):
        return str(obj)


@admin.register(FileProperty)
class FileAdmin(admin.ModelAdmin):
    list_display = ('custom_file_property_name', 'course',)

    def custom_file_property_name(self, obj):
        return f"File: {str(obj)}"


@admin.register(URLProperty)
class URLAdmin(admin.ModelAdmin):
    pass
