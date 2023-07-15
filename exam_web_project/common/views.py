from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views import generic as views


class HomeView(views.TemplateView):
    template_name = 'index.html'


def handler404(request, exception):
    return render(request, '404.html', status=404)
