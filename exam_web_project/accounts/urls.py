from django.urls import path, include
from django.contrib.auth import views as auth_views

from exam_web_project.accounts.views import SignUpView, SignInView, SignOutView, UserProfileView, UserEditProfileView, \
    ChangePasswordView, ChangePasswordDoneView, ResetPasswordView, ResetPasswordDoneView, ResetPasswordConfirmView, \
    ResetPasswordComplete

urlpatterns = (
    path('sing-up/', SignUpView.as_view(), name='sign up'),
    path('sing-in/', SignInView.as_view(), name='sign in'),
    path('sing-out/', SignOutView.as_view(next_page='/'), name='logout'),
    path('profile/<int:pk>/', include([
        path('', UserProfileView.as_view(), name='profile details'),
        path('edit/', UserEditProfileView.as_view(), name='edit profile'),
    ])),
    path('password-change/', include([
        path('', ChangePasswordView.as_view(), name='change password'),
        path('done/', ChangePasswordDoneView.as_view(), name='password success'),
    ])),
    path('password-reset/', include([
        path('', ResetPasswordView.as_view(), name='password_reset'),
        path('done/', ResetPasswordDoneView.as_view(), name='password_reset_done'),
        path('confirm/<uidb64>/<token>/', ResetPasswordConfirmView.as_view(), name='password_reset_confirm'),
        path('complete/', ResetPasswordComplete.as_view(), name='password_reset_complete'),
    ])),

)
