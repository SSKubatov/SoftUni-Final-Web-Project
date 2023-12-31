from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django import views
from django.urls import reverse_lazy

import time

from exam_web_project.newsletter.forms import NewsletterUserSubscriberForm
from exam_web_project.newsletter.models import NewsletterUser
from exam_web_project.newsletter.services import NewsletterSubscriber, NewsletterEmailService


class NewsletterSubscribeView(views.View):
    SUBSCRIBE_MESSAGE = "Subscribed Successful."
    ERROR_SUBSCRIBE_MESSAGE = "You are already subscribed to our newsletter."

    def post(self, request, *args, **kwargs):
        emails = request.POST.get('email')
        newsletter_subscriber = NewsletterSubscriber()

        if not newsletter_subscriber.is_subscribed(emails):
            newsletter_subscriber.subscribe(emails)

            email_service = NewsletterEmailService()
            email_service.send_subscription_confirmation(emails)
            messages.success(request, self.SUBSCRIBE_MESSAGE)
            return redirect('home')

        messages.error(request, self.ERROR_SUBSCRIBE_MESSAGE)
        return redirect('home')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class SendNewsletterEmailView(LoginRequiredMixin, UserPassesTestMixin, views.View):
    SEND_MESSAGE_SUCCESS = "Newsletter are send successful."
    SEND_MESSAGE_FAIL = "Fail to send the message."

    form_class = NewsletterUserSubscriberForm
    template_name = 'newsletter/send_newsletter.html'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            status = form.cleaned_data['status']
            subscribers = NewsletterUser.objects.values_list('email', flat=True)

            newsletter_email_services = NewsletterEmailService()

            newsletter_email_services.send_newsletter_email(subject, message, subscribers, status)

            messages.success(request, self.SEND_MESSAGE_SUCCESS)
            return redirect('home')

        context = {
            'form': form,
        }

        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        form = self.form_class

        context = {
            'form': form
        }

        return render(request, self.template_name, context)
