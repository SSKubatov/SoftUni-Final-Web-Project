from django.urls import path
from django.views.generic import TemplateView

from exam_web_project.newsletter.views import NewsletterSubscribeView, SendNewsletterEmailView

urlpatterns = (
    path('', NewsletterSubscribeView.as_view(), name='newsletter subscribe'),
    path('success/', TemplateView.as_view(template_name="newsletter/newsletter_subscribe_success.html"),
         name='newsletter subscribe success'),
    path('send/', SendNewsletterEmailView.as_view(), name='send newsletter'),
)
