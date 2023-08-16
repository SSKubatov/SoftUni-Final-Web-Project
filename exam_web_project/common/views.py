from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views import generic as views

UserModel = get_user_model()


class HomeView(views.TemplateView):
    template_name = 'index.html'


class ShowcaseSectionView(views.TemplateView):
    template_name = 'sections/showcase_section.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        user = request.user
        context['user'] = user
        return self.render_to_response(context)


class InfoSectionView(views.TemplateView):
    template_name = 'sections/info_section.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        user = request.user
        context['user'] = user
        return self.render_to_response(context)


class CommunitySectionView(views.TemplateView):
    template_name = 'sections/community_section.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        user = request.user
        context['user'] = user
        return self.render_to_response(context)


def handler404(request, exception):
    return render(request, '404.html', status=404)
