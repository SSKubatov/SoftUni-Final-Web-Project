from django.urls import path

from exam_web_project.payments.views import checkout, success, cancel, webhook

urlpatterns = (
    path('checkout/<str:slug>/', checkout, name='checkout'),
    path('success/', success, name='success'),
    path('cancel/', cancel, name='cancel'),
    path('webhook/', webhook, name='webhook'),
)
