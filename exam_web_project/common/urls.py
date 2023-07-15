from django.conf.urls import handler404
from django.urls import path

from exam_web_project.common.views import HomeView, handler404

urlpatterns = (
    path('', HomeView.as_view(), name='home'),
)

handler404 = handler404
