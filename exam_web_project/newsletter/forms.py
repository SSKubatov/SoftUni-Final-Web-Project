from django import forms

from exam_web_project.newsletter.models import NewsletterUser, Newsletter


class NewsletterUserSubscriberForm(forms.ModelForm):
    class Meta:
        model = NewsletterUser
        fields = ['email']


class NewsletterBaseForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = '__all__'


# class CustomNewsletterForm(NewsletterBaseForm):
#     class Meta(NewsletterBaseForm.Meta):
#         exclude = ['email', ]
