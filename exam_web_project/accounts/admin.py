from django.contrib import admin
from django.contrib.auth import get_user_model, admin as auth_admin

from exam_web_project.accounts.forms import UserEditForm, UserAdminCreateForm

UserModel = get_user_model()


@admin.register(UserModel)
class AppUserAdmin(auth_admin.UserAdmin):
    form = UserEditForm
    add_form = UserAdminCreateForm

    fieldsets = (
        (
            None, {
                "fields": (
                    "username",
                    "password",
                ),
            },
        ),
        (
            "Personal info", {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    'gender',
                    'profile_picture',
                ),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Important dates", {
                "fields": (
                    "last_login",
                    "date_joined",
                ),
            },
        ),
    )

