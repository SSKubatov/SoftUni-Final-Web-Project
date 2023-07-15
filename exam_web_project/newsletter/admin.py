from django.contrib import admin

from exam_web_project.newsletter.models import Newsletter, NewsletterUser


# Register your models here.
@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    pass


@admin.register(NewsletterUser)
class NewsletterUserAdmin(admin.ModelAdmin):
    pass
