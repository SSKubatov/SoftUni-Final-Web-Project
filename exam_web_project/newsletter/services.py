from django.conf import settings
from django.core.mail import send_mail

from exam_web_project.newsletter.models import NewsletterUser, Newsletter


class NewsletterSubscriber:
    @staticmethod
    def subscribe(email):
        NewsletterUser.objects.create(email=email)

    @staticmethod
    def unsubscribe(email):
        try:
            subscriber = NewsletterUser.objects.get(email=email)
            subscriber.delete()
        except Newsletter.DoesNotExist:
            pass

    @staticmethod
    def is_subscribed(email):
        return NewsletterUser.objects.filter(email=email).exists()


class EmailService:
    @staticmethod
    def send_email(subject, message, recipient_list, status):
        Newsletter.objects.create(
            subject=subject,
            message=message,
            status=status
        )

        from_email = settings.EMAIL_HOST_USER

        for user_email in recipient_list:
            send_mail(subject, message, from_email, [user_email])

    @staticmethod
    def send_subscription_confirmation(email):
        subject = 'Newsletter Subscription Confirmation'
        message = 'Thank you for subscribing to our newsletter.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)

    @staticmethod
    def send_unsubscription_confirmation(email):
        subject = 'Newsletter Unsubscription Confirmation'
        message = 'You have been unsubscribed from our newsletter.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)
