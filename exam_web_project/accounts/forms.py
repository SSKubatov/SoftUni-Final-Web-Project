from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model

from core.custom_validators.validators import validate_username

UserModel = get_user_model()


class BaseUserCreateForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ("username", "email", 'password1', 'password2')
        field_classes = {
            "username": auth_forms.UsernameField,
        }


class UserCreateForm(BaseUserCreateForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-floating'}),
        label='Username'
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='Email',
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Password',
        help_text='Required 8-20 characters without spaces.'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Confirm Password'
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')

        validate_username(username)

        return username


class UserEditForm(auth_forms.UserChangeForm):
    class Meta:
        model = UserModel
        fields = '__all__'
        field_classes = {
            "username": auth_forms.UsernameField,
        }


class UserLoginForm(auth_forms.AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Username'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )


class ChangePasswordForm(auth_forms.PasswordChangeForm):
    old_password = forms.CharField(
        label='Old Password',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'type': 'password'}),
    )

    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}),
    )
    new_password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}),
    )


# <---------------- ADMIN ------------->
class UserStaffCreateForm(BaseUserCreateForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password1',
            'password2',
            Submit('submit', 'Create')
        )
