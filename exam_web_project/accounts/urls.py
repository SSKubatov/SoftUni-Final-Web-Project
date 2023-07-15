from django.urls import path, include
from django.contrib.auth import views as auth_views

from exam_web_project.accounts.views import SignUpView, SignInView, SignOutView, UserProfileView, UserEditProfileView, \
    ChangePasswordView, ChangePasswordDoneView

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
        path('', auth_views.PasswordResetView.as_view(template_name='accounts/password/password-reset.html'),
             name='password_reset'),
        path('done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
        path('confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
             name='password_reset_confirm'),
        path('complete/', auth_views.PasswordResetCompleteView.as_view(),
             name='password_reset_complete'),
    ]))

)
