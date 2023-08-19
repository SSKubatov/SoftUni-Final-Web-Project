from django.conf import settings
from django.contrib.auth import views as auth_views, get_user_model, login

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views

from exam_web_project.accounts.forms import UserCreateForm, UserLoginForm, ChangePasswordForm, UserEditForm

UserModel = get_user_model()


class SignUpView(views.CreateView):
    template_name = 'accounts/sing-up-page.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result


class SignInView(auth_views.LoginView):
    template_name = 'accounts/sing-in-page.html'
    form_class = UserLoginForm

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url or reverse_lazy('home')


class SignOutView(auth_views.LogoutView):
    next_page = reverse_lazy('home')


class UserProfileView(views.DetailView):
    template_name = 'accounts/profile-details-page.html'
    model = UserModel


class UserEditProfileView(views.UpdateView):
    template_name = 'accounts/profile-edit-page.html'
    model = UserModel
    fields = ('profile_picture', 'first_name', 'last_name', 'gender')
    form_class = UserEditForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={
            'pk': self.request.user.pk
        })


class ChangePasswordView(auth_views.PasswordChangeView):
    template_name = "accounts/password/password-change.html"
    form_class = ChangePasswordForm
    success_url = reverse_lazy('password success')


class ChangePasswordDoneView(auth_views.PasswordChangeDoneView):
    template_name = 'accounts/password/password-change-done.html'


class ResetPasswordView(auth_views.PasswordResetView):
    template_name = 'accounts/password/password-reset.html'


class ResetPasswordDoneView(auth_views.PasswordResetDoneView):
    pass


class ResetPasswordConfirmView(auth_views.PasswordResetConfirmView):
    pass


class ResetPasswordComplete(auth_views.PasswordResetCompleteView):
    pass
