from django.urls import path

from exam_web_project.common.views import HomeView

urlpatterns = (
    path('', HomeView.as_view(), name='home'),
)
