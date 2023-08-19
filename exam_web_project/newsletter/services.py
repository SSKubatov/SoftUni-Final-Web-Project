from django.conf import settings
from django.core.mail import send_mail

from exam_web_project.newsletter.models import NewsletterUser, Newsletter


class NewsletterSubscriber:
    @staticmethod
    def subscribe(email):
        NewsletterUser.objects.create(email=email)

    @staticmethod
    def is_subscribed(email):
        return NewsletterUser.objects.filter(email=email).exists()


class NewsletterEmailService:
    SUBJECT_GREETINGS = 'Newsletter Subscription Confirmation'
    MESSAGE_GREETINGS = 'Thank you for subscribing to our newsletter.'

    def send_newsletter_email(self, subject, message, recipient_list, status):
        Newsletter.objects.create(
            subject=subject,
            message=message,
            status=status
        )

        from_email = settings.EMAIL_HOST_USER
        for email in recipient_list:
            send_mail(subject, message, from_email, [email])

    def send_subscription_confirmation(self, email):
        subject = self.SUBJECT_GREETINGS
        message = self.MESSAGE_GREETINGS
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)
