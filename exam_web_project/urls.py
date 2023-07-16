from django.conf import settings
from django.conf.urls import handler404

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('exam_web_project.common.urls')),
    path('account/', include('exam_web_project.accounts.urls')),
    path('courses/', include('exam_web_project.courses.urls')),
    path('payments/', include('exam_web_project.payments.urls')),
    path('newsletter/', include('exam_web_project.newsletter.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
